#include <stdio.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <linux/netfilter_ipv4.h>
#include <linux/netfilter_ipv6/ip6_tables.h>
#include <event.h>


#include "openssl/ssl.h"
#include <openssl/x509v3.h>


#define CA_key_location "/temp/transproxy_CA.key"
#define CA_cert_location "/temp/transproxy_CA.crt"
// LIMIT is one byte smaller than 65536 for '\0'
#define LIMIT 65535



struct shared_data {
    struct event_base *evbase;
    SSL_CTX *client_tls_ctx;
    SSL_CTX *remote_tls_ctx;
    EVP_PKEY *CA_key;
    X509 *CA_cert;
    unsigned char* recognized_cipher[LIMIT];
    unsigned int cipher_length[LIMIT];
};



// 1. assume that http/http2/sslrecord header, if exist, always appear at the beginning
// 2. assume that each sslrecord can be read in one time

struct sock_data {
    // struct event_base *evbase;
    unsigned char up_msg[65536];
    int up_bytes;
    unsigned char down_msg[65536];
    int down_bytes;
    struct event *up_read;
    struct event *up_write;
    struct event *down_read;
    struct event *down_write;


    char remote_tls_status;
    char client_tls_status;
    char is_freeing;


    SSL_CTX* client_tls_ctx;
    SSL *client_tls_conn;
    SSL_CTX* remote_tls_ctx;
    SSL *remote_tls_conn;
    unsigned char** recognized_cipher;
    unsigned int* cipher_length;
    unsigned char available_cipher[LIMIT];

    // const char* selected_cipher;

    X509 *fake_remote_cert;
    X509 *real_remote_cert;

    EVP_PKEY *CA_key;
    X509 *CA_cert;

    unsigned char* sni;

    // alpn[0] -> whether h2 support,  alpn[1] -> whethr http1.1 support
    unsigned char* available_alpn;
    unsigned int alpn_length;

    const unsigned char** selected_alpn;
    unsigned int* selected_alpn_length;
};







void generate_CA_cert(EVP_PKEY *pkey, X509 *x509) {
    pkey = EVP_PKEY_new();
    RSA *rsa = RSA_generate_key(2048, RSA_F4, NULL, NULL);
    EVP_PKEY_assign_RSA(pkey, rsa);

    // https://stackoverflow.com/questions/256405/programmatically-create-x509-certificate-using-openssl
    x509 = X509_new();

    X509_set_version(x509, 2);
    ASN1_INTEGER_set(X509_get_serialNumber(x509), 1);
    X509_gmtime_adj(X509_get_notBefore(x509), 0);
    X509_gmtime_adj(X509_get_notAfter(x509), 315360000L);

    X509_set_pubkey(x509, pkey);

    X509_NAME *name = X509_get_subject_name(x509);
    // country
    X509_NAME_add_entry_by_txt(name, "C", MBSTRING_ASC,
                               (unsigned char *) "US", -1, -1, 0);
    X509_NAME_add_entry_by_txt(name, "O", MBSTRING_ASC,
                               (unsigned char *) "transproxy", -1, -1, 0);
    X509_NAME_add_entry_by_txt(name, "CN", MBSTRING_ASC,
                               (unsigned char *) "transproxy", -1, -1, 0);

    X509_set_issuer_name(x509, name);


    X509_EXTENSION *ex;
    /* Add various extensions: standard extensions */
    ex = X509V3_EXT_conf_nid(NULL, NULL, NID_basic_constraints, "critical,CA:TRUE");
    X509_add_ext(x509, ex, -1);
    X509_EXTENSION_free(ex);

    ex = X509V3_EXT_conf_nid(NULL, NULL, NID_netscape_cert_type, "sslCA");
    X509_add_ext(x509, ex, -1);
    X509_EXTENSION_free(ex);


    ex = X509V3_EXT_conf_nid(NULL, NULL, NID_key_usage, "critical,keyCertSign,cRLSign");
    X509_add_ext(x509, ex, -1);
    X509_EXTENSION_free(ex);


    ex = X509V3_EXT_conf_nid(NULL, NULL, NID_ext_key_usage,
                             "serverAuth,clientAuth,emailProtection,timeStamping,msCodeInd,msCodeCom,msCTLSign,msSGC,msEFS,nsSGC");
    X509_add_ext(x509, ex, -1);
    X509_EXTENSION_free(ex);

    ex = X509V3_EXT_conf_nid(NULL, NULL, NID_subject_key_identifier, "hash");
    X509_add_ext(x509, ex, -1);
    X509_EXTENSION_free(ex);

    // use sha256 for fingerprint
    // https://stackoverflow.com/questions/27039489/difference-between-signing-with-sha256-vs-signing-with-rsa-sha256/27041297
    // https://stackoverflow.com/questions/2883164/openssl-certificate-lacks-key-identifiers
    X509_sign(x509, pkey, EVP_sha256());


    FILE *f = fopen(CA_key_location, "w");
    PEM_write_PrivateKey(f, pkey,  // file handle and key
                         NULL,  // default cipher for encrypting the key on disk
                         NULL,       // passphrase required for decrypting the key on disk
                         0,                 // length of the passphrase string
                         NULL,              // callback for requesting a password
                         NULL               // data to pass to the callback
    );
    fclose(f);


    f = fopen(CA_cert_location, "w");
    PEM_write_X509(f, x509);
    fclose(f);


    // X509_free(x509);
    // EVP_PKEY_free(pkey);
}


void generate_fake_remote_cert(struct sock_data* data) {

    // https://stackoverflow.com/questions/256405/programmatically-create-x509-certificate-using-openssl
    data->fake_remote_cert = X509_new();

    // X509_set_version(data->fake_remote_cert, 2);
    ASN1_INTEGER_set(X509_get_serialNumber(data->fake_remote_cert), 1);
    X509_gmtime_adj(X509_get_notBefore(data->fake_remote_cert), 0);
    X509_gmtime_adj(X509_get_notAfter(data->fake_remote_cert), 31536000L);

    //

    X509_set_issuer_name(data->fake_remote_cert, X509_get_subject_name(data->CA_cert));

    /*
    X509_NAME *name = X509_get_subject_name(data->fake_remote_cert);
    X509_NAME_add_entry_by_txt(name, "CN", MBSTRING_ASC,
                               (unsigned char *) common_name, -1, -1, 0);
    */
    X509_set_subject_name(data->fake_remote_cert, X509_get_subject_name(data->real_remote_cert));



    X509_EXTENSION *ex = X509V3_EXT_conf_nid(NULL, NULL, NID_ext_key_usage,
                                             "serverAuth,clientAuth");
    X509_add_ext(data->fake_remote_cert, ex, -1);
    X509_EXTENSION_free(ex);

    X509_set_pubkey(data->fake_remote_cert, data->CA_key);
    // use sha256 for fingerprint
    // https://stackoverflow.com/questions/27039489/difference-between-signing-with-sha256-vs-signing-with-rsa-sha256/27041297
    // https://stackoverflow.com/questions/2883164/openssl-certificate-lacks-key-identifiers
    X509_sign(data->fake_remote_cert, data->CA_key, EVP_sha256());


}


void remove_connection(struct sock_data *data) {

    if (data->is_freeing == 0) {
        data->is_freeing = 1;
        event_free(data->up_read);
        event_free(data->up_write);
        event_free(data->down_read);
        event_free(data->down_write);
        free(data);
        printf("connection ended\n");
    }
}


// strlen does not count the null terminator
void add_cipher(unsigned char** recognized_cipher, unsigned int* cipher_length, int code, char* cipher_str) {

    int length = strlen(cipher_str);
    recognized_cipher[code] = malloc(length);
    cipher_length[code] = length;
    memcpy(recognized_cipher[code], cipher_str, length);
}




