"ECDHE-ECDSA-AES128-GCM-SHA256:"
"ECDHE-RSA-AES128-GCM-SHA256:"
"ECDHE-ECDSA-AES256-GCM-SHA384:"
"ECDHE-RSA-AES256-GCM-SHA384:"
"ECDHE-ECDSA-CHACHA20-POLY1305:"
"ECDHE-RSA-CHACHA20-POLY1305:"
"DHE-RSA-AES128-GCM-SHA256:"
"DHE-RSA-AES256-GCM-SHA384:"
"DHE-RSA-CHACHA20-POLY1305:"
"ECDHE-ECDSA-AES128-SHA256:"
"ECDHE-RSA-AES128-SHA256:"
"ECDHE-ECDSA-AES128-SHA"
":ECDHE-RSA-AES128-SHA:"
"ECDHE-ECDSA-AES256-SHA384:"
"ECDHE-RSA-AES256-SHA384:"
"ECDHE-ECDSA-AES256-SHA:"
"ECDHE-RSA-AES256-SHA:"
"DHE-RSA-AES128-SHA256:"
"DHE-RSA-AES256-SHA256:"
"AES128-GCM-SHA256:"
"AES256-GCM-SHA384:"
"AES128-SHA256:"
"AES256-SHA256:"
"AES128-SHA:"
"AES256-SHA:"
"DES-CBC3-SHA"

















/*
    SSL_CTX_set_cipher_list(downstream_tls_ctx, "ALL:eNULL");
    printf("ssl here -1\n");

    if (SSL_CTX_load_verify_locations(downstream_tls_ctx, "test.crt", "test.key") == 1)
        printf("I find files\n");

    if (SSL_CTX_set_default_verify_paths(downstream_tls_ctx) == 1)
        printf("I find files\n");

    */



/*
    if (SSL_CTX_use_certificate_file(sdata->downstream_tls_ctx, "test.pem", SSL_FILETYPE_PEM) <= 0) {
        printf("crt error\n");
    }
    if (SSL_CTX_use_PrivateKey_file(sdata->downstream_tls_ctx, "test.pem", SSL_FILETYPE_PEM) <= 0) {
        printf("key error\n");
    }

    printf("ssl init finished\n");
*/


// printf("check finished\n");
/*
 *
// must send what is recognize here, any failure results
// in blocking
// client hello
if ((data->toremote_bytes >= 5) &&
(data->toremote_msg[0] == 0x16) &&
(data->toremote_msg[1] == 0x03) &&
(data->toremote_msg[2] >= 0x00) &&
(data->toremote_msg[2] <= 0x03)) {
    data->is_TLS = 1;
    // SSL_CTX_use_certificate_file(ssl_context, "/serverCertificate.pem" , SSL_FILETYPE_PEM);
    // SSL_CTX_use_PrivateKey_file(ssl_context, "/serverCertificate.pem", SSL_FILETYPE_PEM);
    data->SSL_connection = SSL_new(SSL_CTX_new(TLS_server_method()));
    SSL_set_fd(data->SSL_connection, clientSock);
    // should be able to directly accept since read, otherwise check next time?
    SSL_accept(data->SSL_connection);
}
*/


// data->toremote_bytes = recv(clientSock, data->toremote_msg, 5, MSG_PEEK);
// printf("I peek %d bytes\n", data->toremote_bytes);


/*
int use_cert = SSL_CTX_use_certificate_file(sslctx, "/serverCertificate.pem" , SSL_FILETYPE_PEM);
int use_prv = SSL_CTX_use_PrivateKey_file(sslctx, "/serverCertificate.pem", SSL_FILETYPE_PEM);
*/





/*
if (data->toremote_bytes > record_length)
    printf("the next record ver %x %x %x %c %c %c\n", data->toremote_msg[record_length],
           data->toremote_msg[record_length+1], data->toremote_msg[record_length+2], data->toremote_msg[record_length],
           data->toremote_msg[record_length+1], data->toremote_msg[record_length+2]);
*/
// data->toremote_bytes = SSL_read(data->downstream_tls_conn, data->toremote_msg, LIMIT);

}


// printf("%d %d %d\n", data->toremote_msg[0], data->toremote_msg[1], data->toremote_msg[2]);
// printf("read finished\n");
// cannot read, the other side disconnected

// printf("finish reading from client.\n");

// need multithreading -> use epoll instead

// case 1. ssl handshake -> establish using openssl
// case 2. (if is_TLS = 1), ssl encrypted flow in forms of
// tcp packet -> decrypt (openssl) and reduce to case 3
// case 3. (else) http flow in forms of tcp packets (filter
// default. unrecognized by case 1 or 3, remove connection

// in case 3,
// if has a http header (need to recognize it and need a parser)
//      analyze content and make a decision
// else (data)
//      let it go (and re-encrypt (openssl) if coming from case 2)

// TLS record/HTTP header may also be (especially mix TLS record
// and plain HTTP header)
// concat at the end of some other record and appear not
// at the beginning of a packet??????? (especially HTTP header
// does not give length in raw bytes?)

// !!! GET cannot trust hostname? -> use info from the actual
// server, for example, certificate field.
// use the host name provided and check if it is trust
// worthy by making an DNS request, get an ip from it and compare
// with the ip of current request (obtained in struct sockaddr_storage)
// but plain http may not?

// or start with if (data->is_TLS), then in else decide whether
// it is a special handshake


// in case 3,
// given a successful read, (we have length)
//


-------------------------------------------------------------------------




#include <stdio.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <linux/netfilter_ipv4.h>
#include <linux/netfilter_ipv6/ip6_tables.h>
#include <event.h>
#include <arpa/inet.h>



//#include <openssl/crypto.h>
//#include <openssl/engine.h>
//#include <openssl/err.h>
//#include <openssl/rand.h>
//#include <openssl/x509.h>
//#include <openssl/x509v3.h>
#include <openssl/ssl.h>


/*
struct sock_state {
    unsigned char buffer[65535];
    struct sockaddr_storage clientAddr;
    struct sockaddr_storage remoteAddr;
    struct event *client_read;
    struct event *client_write;
    struct event *remote_read;
    struct event *remote_write;
};
*/
struct sock_data {
    // struct event_base *evbase;
    unsigned char toremote_msg[65535];
    int toremote_bytes;
    unsigned char toclient_msg[65535];
    int toclient_bytes;
    struct event *client_read;
    struct event *remote_write;
    struct event *remote_read;
    struct event *client_write;

    unsigned char url[65535];
    unsigned char* url_offset;

    char is_TLS;
    char is_freeing;


    SSL* SSL_connection;
    // SSL_CTX * SSL_context;
};




void remove_connection(struct sock_data *data) {

    if (data->is_freeing == 0) {
        data->is_freeing = 1;
        event_free(data->client_read);
        event_free(data->remote_write);
        event_free(data->remote_read);
        event_free(data->client_write);
        free(data);
        printf("connection ended\n");
    }
}



void client_read_cb(int clientSock, short event, struct sock_data *data)
{
    /*
    int use_cert = SSL_CTX_use_certificate_file(sslctx, "/serverCertificate.pem" , SSL_FILETYPE_PEM);
    int use_prv = SSL_CTX_use_PrivateKey_file(sslctx, "/serverCertificate.pem", SSL_FILETYPE_PEM);
*/



    data->toremote_bytes = read(clientSock, data->toremote_msg, 65535);

    // cannot read, the other side disconnected
    if (data->toremote_bytes == 0) {
        remove_connection(data);
        return;
    }

    /*
    // must send what is recognize here, any failure results
    // in blocking
    // client hello
    if ((data->toremote_bytes >= 5) &&
    (data->toremote_msg[0] == 0x16) &&
    (data->toremote_msg[1] == 0x03) &&
    (data->toremote_msg[2] >= 0x00) &&
    (data->toremote_msg[2] <= 0x03)) {
        data->is_TLS = 1;
        // SSL_CTX_use_certificate_file(ssl_context, "/serverCertificate.pem" , SSL_FILETYPE_PEM);
        // SSL_CTX_use_PrivateKey_file(ssl_context, "/serverCertificate.pem", SSL_FILETYPE_PEM);
        data->SSL_connection = SSL_new(SSL_CTX_new(TLS_server_method()));
        SSL_set_fd(data->SSL_connection, clientSock);
        // should be able to directly accept since read, otherwise check next time?
        SSL_accept(data->SSL_connection);
    }
    */
    data->toremote_msg[data->toremote_bytes] = '\0';


    // url = [start, end)
    unsigned char *start = data->toremote_msg;
    unsigned char *end;

    do {
        char url_complete = 0;

        // try to find a new request line
        if (data->url_offset == data->url)
            // no request line in this packet
            if (!(start = strstr(start, "GET")))
                continue;

        if (end = strchr(start, ' '))
            url_complete = 1;
        else
            end = data->toremote_msg + data->toremote_bytes;


        if ((end - start) + (data->url_offset - data->url) <= 65535) {
            memcpy(data->url_offset, start, end - start);
            data->url_offset += end - start;
            // do analysis and clean up
            if (url_complete) {
                // terminate the string
                *(data->url_offset + 1) = 0;
                printf("%s", data->url);
                data->url_offset = data->url;
            }
        } else
            remove_connection(data);
    } while(end != data->toremote_msg + data->toremote_bytes);
    /*
    if (data->url_offset != data->url)
        if (end = strchr(start, ' '))
            memcpy(data->url_offset, start, end-start);
            // url analysis
    else
        while (start = strstr(start, "GET")) {
            if (end = strchr(start, ' ')) {
                memcpy(data->url, start, end - start);
                // url analysis

            }
            else {
                end = data->toremote_msg + data->toremote_bytes;
                // not fully read yet, wait for next packet
                memcpy(data->url, start, end - start);
           }


    }

    */


    // printf("message %s\n", data->toremote_msg);
    // event_del to deactivate, event_free is deallocate
    event_del(data->client_read);
    event_add(data->remote_write, NULL);

    // printf("finish reading from client.\n");

    // need multithreading -> use epoll instead

    // case 1. ssl handshake -> establish using openssl
    // case 2. (if is_TLS = 1), ssl encrypted flow in forms of
    // tcp packet -> decrypt (openssl) and reduce to case 3
    // case 3. (else) http flow in forms of tcp packets (filter
    // default. unrecognized by case 1 or 3, remove connection

    // in case 3,
    // if has a http header (need to recognize it and need a parser)
    //      analyze content and make a decision
    // else (data)
    //      let it go (and re-encrypt (openssl) if coming from case 2)

    // TLS record/HTTP header may also be (especially mix TLS record
    // and plain HTTP header)
    // concat at the end of some other record and appear not
    // at the beginning of a packet??????? (especially HTTP header
    // does not give length in raw bytes?)

    // !!! GET cannot trust hostname? -> use info from the actual
    // server, for example, certificate field.
    // use the host name provided and check if it is trust
    // worthy by making an DNS request, get an ip from it and compare
    // with the ip of current request (obtained in struct sockaddr_storage)
    // but plain http may not?

    // or start with if (data->is_TLS), then in else decide whether
    // it is a special handshake


    // in case 3,
    // given a successful read, (we have length)
    //

}



void remote_write_cb(int remoteSock, short event, struct sock_data *data) {
    if (write(remoteSock, data->toremote_msg, data->toremote_bytes) != data->toremote_bytes) {
        remove_connection(data);
        return;
    }
    event_del(data->remote_write);
    event_add(data->client_read, NULL);

    // printf("finish writing to remote.\n");
}


void remote_read_cb(int remoteSock, short event, struct sock_data *data)
{
    data->toclient_bytes = read(remoteSock, data->toclient_msg, 65535);

    // cannot read, the other side disconnected
    if (data->toclient_bytes == 0) {
        remove_connection(data);
        return;
    }
    // printf("message %s\n", data->toremote_msg);
    // event_del to deactivate, this one is deallocate
    event_del(data->remote_read);
    event_add(data->client_write, NULL);

    // printf("finish reading from remote.\n");
}

void client_write_cb(int clientSock, short event, struct sock_data *data) {
    if (write(clientSock, data->toclient_msg, data->toclient_bytes) != data->toclient_bytes) {
        remove_connection(data);
        return;
    }
    event_del(data->client_write);
    event_add(data->remote_read, NULL);

    // printf("finish reading to client.\n");
}

void accept_cb(int listenSock, short event, struct event_base *evbase)
{
    struct sockaddr_storage clientAddr;
    socklen_t addrlen = sizeof(struct sockaddr_storage);
    int clientSock = accept(listenSock, (struct sockaddr*)&clientAddr, &addrlen);
    evutil_make_socket_nonblocking(clientSock);




    char name[100];
    getnameinfo(&clientAddr, sizeof(struct sockaddr_storage), name, 100, NULL, NULL, NI_NUMERICHOST);



    int remoteSock;
    struct sockaddr_storage remoteAddr;
    addrlen = sizeof(struct sockaddr_storage);


    if (strlen(name) >= 7 && (strncmp("::ffff:",name,7) == 0)) {
        remoteSock = socket(AF_INET, SOCK_STREAM, 0);
        getsockopt(clientSock, SOL_IP, SO_ORIGINAL_DST, &remoteAddr, &addrlen);
    }
    else {
        remoteSock = socket(AF_INET6, SOCK_STREAM, 0);
        getsockopt(clientSock, SOL_IPV6, IP6T_SO_ORIGINAL_DST, &remoteAddr, &addrlen);
    }

    int opt = 1;
    setsockopt(remoteSock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(int));

    if (connect(remoteSock, (struct sockaddr *) &remoteAddr, sizeof(struct sockaddr_storage)) < 0) {
        printf("failed to connect to remote\n");
        close(remoteSock);
    }


    // evutil_make_socket_nonblocking(remoteSock);


    struct sock_data *data = malloc(sizeof(struct sock_data));
    data->is_freeing = 0;

    data->client_read = event_new(evbase, clientSock, EV_READ|EV_PERSIST, client_read_cb, data);
    event_add(data->client_read, NULL);

    data->remote_write = event_new(evbase, remoteSock, EV_WRITE|EV_PERSIST, remote_write_cb, data);

    data->remote_read = event_new(evbase, remoteSock, EV_READ|EV_PERSIST, remote_read_cb, data);
    event_add(data->remote_read, NULL);

    data->client_write = event_new(evbase, clientSock, EV_WRITE|EV_PERSIST, client_write_cb, data);

    char name0[100], port0[100], name1[100], port1[100];
    getnameinfo(&clientAddr, sizeof(struct sockaddr_storage), name0, 100, port0, 100, NI_NUMERICHOST|NI_NUMERICSERV);
    getnameinfo(&remoteAddr, sizeof(struct sockaddr_storage), name1, 100, port1, 100, NI_NUMERICHOST|NI_NUMERICSERV);


    printf("connection from %s:%s to %s:%s\n", name0, port0, name1, port1);


}







// switch to libuv or boost:async if needed
int main(int argc, char *argv[]) {




    struct addrinfo hint, *sockAddr;

    memset(&hint, 0, sizeof hint);
    hint.ai_family = AF_INET6;
    hint.ai_socktype = SOCK_STREAM;
    hint.ai_flags = AI_PASSIVE;

    if (getaddrinfo(NULL, "8080", &hint, &sockAddr) != 0) {
        fprintf(stderr, "getaddrinfo failed\n");
        exit(1);
    }



    // listenSock = socket(sockAddr->ai_family, sockAddr->ai_socktype | SOCK_NONBLOCK, sockAddr->ai_protocol);
    int listenSock = socket(AF_INET6, SOCK_STREAM, 0);
    if (listenSock == -1) {
        fprintf(stderr, "socket failed\n");
    }
    int opt[] = {1, 1, 0};
    setsockopt(listenSock, SOL_SOCKET, SO_REUSEADDR, &opt[0], sizeof(int));
    setsockopt(listenSock, SOL_SOCKET, SO_KEEPALIVE, &opt[1], sizeof(int));
    setsockopt(listenSock, IPPROTO_IPV6, IPV6_V6ONLY, &opt[2], sizeof(int));
    // check if this option can pass through transparent check?
    // setsockopt(listenSock, SOL_IP, IP_TRANSPARENT, &opt[3], sizeof(int));


    if (bind(listenSock, sockAddr->ai_addr, sockAddr->ai_addrlen) != 0)
        printf("bind failed\n");
    if (listen(listenSock, 20) != 0)
        printf("listen failed\n");

    freeaddrinfo(sockAddr);


    /*
    SSL_load_error_strings();
    SSL_library_init();
    OpenSSL_add_all_algorithms();
    */


    struct event_base *evbase = event_base_new();
    struct event *accept_ev = event_new(evbase, listenSock, EV_READ | EV_PERSIST, accept_cb, (void *) evbase);


    event_add(accept_ev, NULL);
    event_base_dispatch(evbase);





    return 0;

}























-----------------------------------------------------------------



//SSL-Client.c
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <malloc.h>
#include <string.h>
#include <sys/socket.h>
#include <resolv.h>
#include <netdb.h>
#include <openssl/ssl.h>
#include <openssl/err.h>

#define FAIL    -1

//Added the LoadCertificates how in the server-side makes.
void LoadCertificates(SSL_CTX* ctx, char* CertFile, char* KeyFile)
{
    /* set the local certificate from CertFile */
    if ( SSL_CTX_use_certificate_file(ctx, CertFile, SSL_FILETYPE_PEM) <= 0 )
    {
        ERR_print_errors_fp(stderr);
        abort();
    }
    /* set the private key from KeyFile (may be the same as CertFile) */
    if ( SSL_CTX_use_PrivateKey_file(ctx, KeyFile, SSL_FILETYPE_PEM) <= 0 )
    {
        ERR_print_errors_fp(stderr);
        abort();
    }
    /* verify private key */
    if ( !SSL_CTX_check_private_key(ctx) )
    {
        fprintf(stderr, "Private key does not match the public certificate\n");
        abort();
    }
}

int OpenConnection(const char *hostname, int port)
{   int sd;
    struct hostent *host;
    struct sockaddr_in addr;

    if ( (host = gethostbyname(hostname)) == NULL )
    {
        perror(hostname);
        abort();
    }
    sd = socket(PF_INET, SOCK_STREAM, 0);
    bzero(&addr, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = *(long*)(host->h_addr);
    if ( connect(sd, (struct sockaddr*)&addr, sizeof(addr)) != 0 )
    {
        close(sd);
        perror(hostname);
        abort();
    }
    return sd;
}

SSL_CTX* InitCTX(void)
{   SSL_METHOD *method;
    SSL_CTX *ctx;

    OpenSSL_add_all_algorithms();  /* Load cryptos, et.al. */
    SSL_load_error_strings();   /* Bring in and register error messages */
    method = SSLv3_client_method();  /* Create new client-method instance */
    ctx = SSL_CTX_new(method);   /* Create new context */
    if ( ctx == NULL )
    {
        ERR_print_errors_fp(stderr);
        abort();
    }
    return ctx;
}

void ShowCerts(SSL* ssl)
{   X509 *cert;
    char *line;

    cert = SSL_get_peer_certificate(ssl); /* get the server's certificate */
    if ( cert != NULL )
    {
        printf("Server certificates:\n");
        line = X509_NAME_oneline(X509_get_subject_name(cert), 0, 0);
        printf("Subject: %s\n", line);
        free(line);       /* free the malloc'ed string */
        line = X509_NAME_oneline(X509_get_issuer_name(cert), 0, 0);
        printf("Issuer: %s\n", line);
        free(line);       /* free the malloc'ed string */
        X509_free(cert);     /* free the malloc'ed certificate copy */
    }
    else
        printf("No certificates.\n");
}

int main()
{   SSL_CTX *ctx;
    int server;
    SSL *ssl;
    char buf[1024];
    int bytes;
    char hostname[]="127.0.0.1";
    char portnum[]="5000";
    char CertFile[] = "/home/myCA/cacert.pem";
    char KeyFile[] = "/home/myCA/private/cakey.pem";

    SSL_library_init();

    ctx = InitCTX();
    LoadCertificates(ctx, CertFile, KeyFile);
    server = OpenConnection(hostname, atoi(portnum));
    ssl = SSL_new(ctx);      /* create new SSL connection state */
    SSL_set_fd(ssl, server);    /* attach the socket descriptor */
    if ( SSL_connect(ssl) == FAIL )   /* perform the connection */
        ERR_print_errors_fp(stderr);
    else
    {   char *msg = "Hello???";

        printf("Connected with %s encryption\n", SSL_get_cipher(ssl));
        ShowCerts(ssl);        /* get any certs */
        SSL_write(ssl, msg, strlen(msg));   /* encrypt & send message */
        bytes = SSL_read(ssl, buf, sizeof(buf)); /* get reply & decrypt */
        buf[bytes] = 0;
        printf("Received: \"%s\"\n", buf);
        SSL_free(ssl);        /* release connection state */
    }
    close(server);         /* close socket */
    SSL_CTX_free(ctx);        /* release context */
    return 0;
}



























-------------------------------------------------------------------------------------------
if(inet_pton(AF_INET, name, binary_name)) {
getsockopt(clientSock, SOL_IP, SO_ORIGINAL_DST, (struct sockaddr *) &remoteAddr, &addrlen);
isIPV6 = 0;
}
else if(inet_pton(AF_INET6, name, binary_name)) {
getsockopt(clientSock, SOL_IPV6, IP6T_SO_ORIGINAL_DST, (struct sockaddr *) &remoteAddr, &addrlen);
isIPV6 = 1;
}
else {
printf("it is an is unknown address format\n");
return;
}











-----------------------------------------------
struct sock_state *state = malloc(sizeof(struct sock_state));


socklen_t addrlen = sizeof(struct sockaddr_storage);
int clientSock = accept(listenSock, (struct sockaddr*)&state->clientAddr, &addrlen);

if (clientSock == -1) {
perror("accept");
close(clientSock);
}

evutil_make_socket_nonblocking(clientSock);

addrlen = sizeof(struct sockaddr_storage);
if (state->clientAddr.ss_family == AF_INET)
getsockopt(clientSock, SOL_IP, SO_ORIGINAL_DST, (struct sockaddr *)&state->remoteAddr, &addrlen);
else
getsockopt(clientSock, SOL_IPV6, IP6T_SO_ORIGINAL_DST, (struct sockaddr *)&state->remoteAddr, &addrlen);





state->client_read = event_new(evbase, clientSock, EV_READ|EV_PERSIST, read_cb, state);
event_add(state->client_read, NULL);



// automatically generate a socket if we pass in -1
struct bufferevent* remote_connect = bufferevent_socket_new(evbase, -1, BEV_OPT_CLOSE_ON_FREE);
bufferevent_setcb(remote_connect, NULL, NULL, remote_connect_cb, NULL);
if (bufferevent_socket_connect(remote_connect,(struct sockaddr *)&state->remoteAddr, addrlen) < 0) {
bufferevent_free(remote_connect);
}

printf("finished adding socket \n");
// event_set(&state->write_event, clientSock, EV_WRITE | EV_PERSIST, write_cb, state);
















--------------------------------------------------------------

char buffer[100];

int returnVal = read(clientSock, buffer, 100);
if (returnVal <= 0) {
if (returnVal < 0)
fprintf(stdout, "Client error, disconnecting\n");
else
fprintf(stdout, "Client disconnected\n");
}


fprintf(stdout, "Message: %.*s destination:\n", returnVal, buffer);
close(clientSock);






--------------------------------------------

// struct sockaddr_storage clientAddr;
// socklen_t clientAddrlen = sizeof(clientAddr);

struct sockaddr_storage remoteAddr;
socklen_t remoteAddrlen = sizeof(remoteAddr);
// remoteAddr in readable format
char dst[100];

int clientSock;

------------------------------------------------------------
while (true)
{
clientSock = accept(listenSock, (struct sockaddr*)&clientAddr, &clientAddrlen);

if (-1 == clientSock)
{
close(clientSock);
continue;
}
// ?? really needed
// getsockname(clientSock, (struct sockaddr*)&remoteAddr, &remoteAddrlen);

if (clientAddr.ss_family == AF_INET) {
getsockopt(clientSock, SOL_IP, SO_ORIGINAL_DST, (struct sockaddr *)&remoteAddr, &remoteAddrlen);
}

else {
getsockopt(clientSock, SOL_IPV6, IP6T_SO_ORIGINAL_DST, (struct sockaddr *)&remoteAddr, &remoteAddrlen);
}

getnameinfo((sockaddr*)&remoteAddr, remoteAddrlen, dst, 100, NULL, 0, NI_NUMERICHOST);

// router dhcp/nat
// nat masquerading, port forwarding, and redirection
// recursive with self ip + range of ports


returnVal = read(clientSock, buffer, sizeof(buffer));
if (returnVal <= 0)
{
if (returnVal < 0)
fprintf(stdout, "Client error, disconnecting\n");
else
fprintf(stdout, "Client disconnected\n");

close(clientSock);


continue;
}

fprintf(stdout, "Message: %.*s destination: %s\n", returnVal, buffer, dst);

// write(clientSock, buffer, returnVal);

close(clientSock);

}




}


















-------------------------------------------------------------------

#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <poll.h>

#define MAX_SERVERS 10
#define MAX_CLIENTS 50
#define MAX_SOCKETS (MAX_SERVERS + MAX_CLIENTS)

int main(int argc, char *argv[])
{
    int simpleSocket, simplePort, returnStatus, n, m;
    char buffer[1024];
    pollfd simpleSockets[MAX_SOCKETS];
    int numSockets = 0, numServers = 0;

    struct addrinfo simpleServer, *res, *addr;

    if (2 != argc)
    {
        fprintf(stderr, "Usage: %s <port>\n", argv[0]);
        exit(1);
    }

    simplePort = atoi(argv[1]);

    memset(&simpleServer, 0, sizeof simpleServer);
    simpleServer.ai_family = AF_UNSPEC;  // use IPv4 and/or IPv6, whatever is available
    simpleServer.ai_socktype = SOCK_STREAM;
    simpleServer.ai_flags = AI_PASSIVE;     // fill in my IP for me

    if (0 != getaddrinfo(NULL, argv[1], &simpleServer, &res))
    {
        fprintf(stderr, "getaddrinfo failed\n");
        exit(1);
    }

    addr = res;
    while (NULL != addr)
    {
        simpleSocket = socket(res->ai_family, addr->ai_socktype, addr->ai_protocol);
        if (-1 == simpleSocket)
        {
            fprintf(stderr, "socket failed\n");
        }
        else
        {
            returnStatus = bind(simpleSocket, addr->ai_addr, addr->ai_addrlen);
            if (0 == returnStatus)
                returnStatus = listen(simpleSocket, 5);

            if (0 == returnStatus)
            {
                simpleSockets[numSockets].fd = simpleSocket;
                simpleSockets[numSockets].events = POLLIN;
                simpleSockets[numSockets].revents = 0;
                ++numSockets;
                ++numServers;
                if (MAX_SERVERS == numServers)
                    break;
            }
            else
            {
                fprintf(stderr, "bind/listen failed\n");
                close(simpleSocket);
            }
        }
        addr = addr->next;
    }

    freeaddrinfo(res);

    if (0 == numServers)
    {
        fprintf(stderr, "no servers are listening\n");
        exit(1);
    }

    struct sockaddr_storage clientName;
    int clientNameLength;

    while (1)
    {
        returnStatus = poll(simpleSockets, numSockets, -1);
        if (-1 == returnStatus)
        {
            fprintf(stderr, "poll failed\n");
            exit(1);
        }

        if (0 == returnStatus)
            continue;

        for (n = 0; n < numSockets; ++n)
        {
            if (simpleSockets[n].revents & POLLIN)
            {
                if (n < numServers)
                {
                    clientNameLength = sizeof(clientName);

                    simpleSocket = accept(simpleSockets[n].fd, (struct sockaddr *)&clientName, &clientNameLength);
                    if (-1 == simpleSocket)
                    {
                        fprintf(stderr, "accept failed\n");
                        continue;
                    }

                    for (m = numServers; m < numSockets; ++m)
                    {
                        if (-1 == simpleSockets[m].fd)
                        {
                            simpleSockets[m].fd = simpleSocket;
                            simpleSockets[m].events = POLLIN;
                            simpleSockets[m].revents = 0;
                            simpleSocket = -1;
                            break;
                        }
                    }

                    if ((-1 != simpleSocket) && (MAX_SOCKETS > numSockets))
                    {
                        simpleSockets[numSockets].fd = simpleSocket;
                        simpleSockets[numSockets].events = POLLIN;
                        simpleSockets[numSockets].revents = 0;
                        ++numSockets;
                        simpleSocket = -1;
                    }

                    if (-1 != simpleSocket)
                    {
                        fprintf(stderr, "Too many clients connected\n");
                        close(simpleSocket);
                    }
                    else
                        fprintf(stdout, "Client connected\n");
                }
                else
                {
                    returnStatus = read(simpleSockets[n].fd, buffer, sizeof(buffer));
                    if (0 >= returnStatus)
                    {
                        if (0 > returnStatus)
                            fprintf(stdout, "Client error, disconnecting\n");
                        else
                            fprintf(stdout, "Client disconnected\n");

                        close(simpleSockets[n].fd);
                        simpleSockets[n].fd = -1;
                        simpleSockets[n].events = 0;
                        simpleSockets[n].revents = 0;

                        continue;
                    }

                    fprintf(stdout, "Message: %.*s\n", returnStatus, buffer);
                    write(simpleSockets[n].fd, buffer, returnStatus);
                }
            }

            if (simpleSockets[n].revents & (POLLERR|POLLHUP|POLLNVAL))
            {
                if (simpleSockets[n].revents & POLLHUP)
                    fprintf(stdout, "Client disconnected\n");
                else if (n >= numServers)
                    fprintf(stdout, "Client error, disconnecting\n");
                else
                    fprintf(stdout, "Server error, closing\n");

                close(simpleSockets[n].fd);
                simpleSockets[n].fd = -1;
                simpleSockets[n].events = 0;
                simpleSockets[n].revents = 0;
            }
        }
    }

    for (n = 0; n < numSockets; ++n)
    {
        if (-1 != simpleSockets[n].fd)
            close(simpleSockets[n].fd);
    }

    return 0;
}