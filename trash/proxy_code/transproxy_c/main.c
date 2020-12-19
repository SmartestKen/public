#include "main.h"



void parse_http1(struct sock_data *data) {
    // url = [start, end)
    unsigned char *end;

    unsigned char *url_start;
    int url_length;
    unsigned char *host_start;
    int host_length;
    int is_http = 0;

    if (url_start = strstr(data->up_msg, "GET ")) {
        url_start = url_start + 4;

        if (end = strchr(url_start, ' ')) {
            url_length = end - url_start;
            is_http = 1;
        }
        else {
            printf("cannot find the end of url, end connection");
            remove_connection(data);
            return;
        }
    }


    // printf("url check finished %d\n", is_http);
    if (is_http) {
        host_start = end;

        // + offset (length of the string) -> go to one byte right after the string
        // right after string - string start = length (offset)
        if (host_start = strstr(host_start, "Host: ")) {
            host_start = host_start + 6;
            // data->up_msg[data->up_bytes] = '\0';
            if (end = strchr(host_start, '\r')) {
                host_length = end - host_start;
                // is_http = 1;
                // printf("%*.*s\n", offset, offset, start);
            } else {
                printf("cannot find the end of url, end connection");
                remove_connection(data);
                return;
            }
        }
    }
    if (is_http)
        printf("%.*s%.*s\n", host_length, host_start, url_length, url_start);
}



void parse_tls_record(struct sock_data *data) {

    /*
    if ((data->up_bytes >= 5) &&
        (data->up_msg[0] >= 0x14) &&
        (data->up_msg[0] <= 0x17) &&
        (data->up_msg[1] == 0x03) &&
        (data->up_msg[2] >= 0x00) &&
        (data->up_msg[2] <= 0x03)) {


    */

    char* up_msg = data->up_msg;
    int record_length = 0x100 * up_msg[3] + up_msg[4] + 5;
    printf("tls record length %d %d %d, actual bytes %d\n", record_length, up_msg[3],
           up_msg[4], data->up_bytes);

    // client_hello -> find sni and alpn
    // sni for the correct certificate
    // alpn for application data later
    // alpn_to_remote = {h2,http1.1} - alpn_from_client;
    // and break if the LHS set is empty
    if (up_msg[5] == 0x01) {
        // header+handshake_type+length+version+random = 5+1+3+2+32 = 43
        int curIndex = 43;
        // sessionID length (one byte)
        curIndex += up_msg[curIndex]+1;

        // cipher suites
        // cipher suites length (two bytes)


        int cipher_endIndex = 0x100*up_msg[curIndex]+up_msg[curIndex+1]+2;
        curIndex += 2;

        unsigned char* available_cipher = data->available_cipher;
        char is_first_cipher = 1;
        while (curIndex < cipher_endIndex){
            int code = 0x100*up_msg[curIndex]+up_msg[curIndex+1];
            if (data->recognized_cipher[code] != NULL){
                if (is_first_cipher) {
                    memcpy(available_cipher, data->recognized_cipher[code], data->cipher_length[code]);
                    available_cipher += data->cipher_length[code];
                    is_first_cipher = 0;
                }
                else {
                    *available_cipher = ':';
                    available_cipher += 1;
                    memcpy(available_cipher, data->recognized_cipher[code], data->cipher_length[code]);
                    available_cipher += data->cipher_length[code];
                }
            }
            curIndex += 2;
        }
        *available_cipher = '\0';

        if (curIndex != cipher_endIndex){
            remove_connection(data);
            return;
        }


        // compression method length (one byte)
        curIndex += up_msg[curIndex]+1;
        // extension length (two bytes)
        curIndex += 2;

        char sni_pass_flag = 0;
        char alpn_pass_flag = 0;

        // each extension type two bytes, length two bytes
        while (curIndex < record_length) {
            // sni
            if ((! sni_pass_flag) &&
                (up_msg[curIndex] == 0) &&
                (up_msg[curIndex + 1] == 0)) {

                // stop connection if server name is too long (>255)
                if (up_msg[curIndex+2] != 0)
                {
                    remove_connection(data);
                    return;
                }

                data->sni = malloc(up_msg[curIndex+3]+1);
                memcpy(data->sni, up_msg+curIndex+4, up_msg[curIndex+3]);
                data->sni[up_msg[curIndex+3]] = '\0';

                sni_pass_flag = 1;

            }

            // alpn 0x00, 0x10
            if ((! alpn_pass_flag) &&
                (up_msg[curIndex] == 0) &&
                (up_msg[curIndex+1] == 0x10)) {

                // too many alpn options
                if (up_msg[curIndex+4] != 0)
                {
                    remove_connection(data);
                    return;
                }

                unsigned char alpn[2];
                int alpn_next = curIndex+6;
                int alpn_end = curIndex+6+up_msg[curIndex+5];
                while (alpn_next < alpn_end) {

                    if ((up_msg[alpn_next] == 2) &&
                        (strncmp(up_msg+alpn_next+1, "h2", up_msg[alpn_next]) == 0))
                        alpn[0] = 1;

                    if ((up_msg[alpn_next] == 8) &&
                        (strncmp(up_msg+alpn_next+1, "http/1.1", up_msg[alpn_next]) == 0))
                        alpn[1] = 1;


                    alpn_next += up_msg[alpn_next]+1;
                }
                if (alpn_next != alpn_end) {
                    remove_connection(data);
                    return;
                }

                // both
                if (alpn[0] && alpn[1]) {
                    data->alpn_length = 12;
                    data->available_alpn = malloc(12);
                    char temp_vector[12] = {
                        2, 'h', '2',
                        8, 'h', 't', 't', 'p', '/', '1', '.', '1'};
                    memcpy(data->available_alpn, temp_vector, 12);
                }
                // h2 only
                else if (alpn[0] && !alpn[1]){
                    data->alpn_length = 3;
                    data->available_alpn = malloc(3);
                    char temp_vector[3] = {
                        2, 'h', '2'};
                    memcpy(data->available_alpn, temp_vector, 3);
                }
                // http/1.1 only
                else if (!alpn[0] && alpn[1]){
                    data->alpn_length = 9;
                    data->available_alpn = malloc(9);
                    char temp_vector[9] = {
                        8, 'h', 't', 't', 'p', '/', '1', '.', '1'};
                    memcpy(data->available_alpn, temp_vector, 9);
                }
                else {
                    remove_connection(data);
                    return;
                }



                alpn_pass_flag += 1;
            }

            if (sni_pass_flag && alpn_pass_flag)
                break;

            curIndex += 4+0x100*up_msg[curIndex+2]+up_msg[curIndex+3];
        }
    }

    // SSL_set_accept_state(data->client_tls_conn);
    // if handshake, directly forward the package, TLS_start

}



int pass_selected_alpn_to_client(SSL *ssl, const unsigned char **out, unsigned char *outlen,
                                const unsigned char *in, unsigned int inlen, struct sock_data *data) {
    out = data->selected_alpn;
    outlen = data->selected_alpn_length;
    return 0;
}


void up_read_cb(int clientSock, short event, struct sock_data *data)
{


    if (data->client_tls_status == 1){
        SSL_use_certificate(data->client_tls_conn, data->fake_remote_cert);
        // which function to set alpn for client and remote connection respectively
        // set alpn and cipher then accept to establish client connection
        SSL_CTX_set_alpn_select_cb(data->client_tls_ctx, pass_selected_alpn_to_client, data);
        SSL_accept(data->client_tls_conn);

        data->client_tls_status = 2;
        // direct return and wait for actual data read
        return;
    }


    if (data->client_tls_status == 2) {
        data->up_bytes = SSL_read(data->client_tls_conn, data->up_msg, LIMIT);
        // cannot read, the other side disconnected
        if (data->up_bytes == 0) {
            remove_connection(data);
            return;
        }
    }
    else {
        data->up_bytes = recv(clientSock, data->up_msg, 3, MSG_PEEK);

        if ((data->up_bytes == 3) &&
            (data->up_msg[0] == 0x16) &&
            (data->up_msg[1] == 0x03) &&
            (data->up_msg[2] >= 0x00) &&
            (data->up_msg[2] <= 0x03)) {
            data->up_bytes = recv(clientSock, data->up_msg, LIMIT, MSG_PEEK);
            data->up_msg[data->up_bytes] = '\0';

            // get sni and alpn from client hello
            // to be ready for remote connection
            parse_tls_record(data);
            data->remote_tls_status = 1;
        }
        else {
            data->up_bytes = read(clientSock, data->up_msg, LIMIT);
            // cannot read, the other side disconnected
            if (data->up_bytes == 0) {
                remove_connection(data);
                return;
            }
        }
    }



    // event_del to deactivate, event_free is deallocate
    event_del(data->up_read);
    event_add(data->up_write, NULL);

    /*
    if ((data->up_bytes <= 0) || (data->up_bytes > LIMIT)) {
        printf("Exceed limit %d\n", data->up_bytes);
        remove_connection(data);
        return;
    }
    */
}



void up_write_cb(int remoteSock, short event, struct sock_data *data) {

    // = 1 means need to be established, = 2 means established
    if (data->remote_tls_status == 1)
    {
        
        // SSL_set_connect_state(data->remote_tls_conn);
        SSL_set_fd(data->remote_tls_conn, remoteSock);
        // SSL_set_options(data->remote_tls_conn, SSL_OP_ALL);
        SSL_set_alpn_protos(data->remote_tls_conn, data->available_alpn, data->alpn_length);
        if (data->sni != NULL) {
            SSL_set_tlsext_host_name(data->remote_tls_conn, data->sni);
            SSL_set1_host(data->remote_tls_conn, data->sni);
        }
        // ensure the cipher selected by remote is compatible with the actual data protocol
        SSL_set_cipher_list(data->remote_tls_conn, data->available_cipher);
        
        if (SSL_connect(data->remote_tls_conn) < 0) {
            remove_connection(data);
            printf("fail to connect\n");
            return;
        }
        printf("I connected\n");

        // verify remote certificate and get alpn to be ready for client tls connection
        if (SSL_get_verify_result(data->remote_tls_conn) != X509_V_OK) {
            remove_connection(data);
            return;
        }


        if (data->real_remote_cert = SSL_get_peer_certificate(data->remote_tls_conn)) {
            generate_fake_remote_cert(data);
            // auto checked as in https://www.openssl.org/docs/manmaster/man3/SSL_get0_peername.html
            // X509_check_host(data->real_remote_cert, data->sni, strlen(data->sni), 0, NULL);
            X509_free(data->real_remote_cert);
        }


        SSL_get0_alpn_selected(data->remote_tls_conn, data->selected_alpn, data->selected_alpn_length);
        // data->selected_cipher = SSL_get_cipher(data->remote_tls_conn);

        data->remote_tls_status = 2;
        data->client_tls_status = 1;
        event_del(data->up_write);
        event_add(data->up_read, NULL);
        return;
    }
    
    if (data->remote_tls_status == 2) {
        if (SSL_write(data->remote_tls_conn, data->up_msg, data->down_bytes) != data->up_bytes) {
            printf("I cannot SSL_write\n");
            remove_connection(data);
            return;
        }
    }
    else {
        if (write(remoteSock, data->up_msg, data->up_bytes) != data->up_bytes) {
            remove_connection(data);
            return;
        }
    }


    event_del(data->up_write);
    event_add(data->up_read, NULL);

}


void down_read_cb(int remoteSock, short event, struct sock_data *data)
{
    if (data->remote_tls_status == 2) {
        data->down_bytes = SSL_read(data->remote_tls_conn, data->up_msg, LIMIT);
        // cannot read, the other side disconnected
        if (data->down_bytes == 0) {
            remove_connection(data);
            return;
        }
    }
    else {
        data->down_bytes = read(remoteSock, data->down_msg, LIMIT);
        // cannot read, the other side disconnected
        if (data->down_bytes == 0) {
            remove_connection(data);
            return;
        }
    }


    // printf("message %s\n", data->up_msg);
    // event_del to deactivate, this one is deallocate
    event_del(data->down_read);
    event_add(data->down_write, NULL);
}

void down_write_cb(int clientSock, short event, struct sock_data *data) {

    if (data->client_tls_status == 2) {
        if (SSL_write(data->client_tls_conn, data->down_msg, data->down_bytes) != data->down_bytes) {
            printf("I cannot SSL_write\n");
            remove_connection(data);
            return;
        }
    }
    else {
        if (write(clientSock, data->down_msg, data->down_bytes) != data->down_bytes) {
            remove_connection(data);
            return;
        }
    }

    event_del(data->down_write);
    event_add(data->down_read, NULL);

    // printf("finish reading to client.\n");
}






void accept_cb(int listenSock, short event, struct shared_data* sdata)
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


    struct sock_data *data = calloc(1, sizeof(struct sock_data));
    data->is_freeing = 0;
    data->client_tls_ctx = sdata->client_tls_ctx;
    data->remote_tls_ctx = sdata->remote_tls_ctx;

    data->client_tls_conn = SSL_new(data->client_tls_ctx);
    data->remote_tls_conn = SSL_new(data->remote_tls_ctx);
    data->recognized_cipher = sdata->recognized_cipher;
    data->cipher_length = sdata->cipher_length;

    data->CA_cert = sdata->CA_cert;
    data->CA_key = sdata->CA_key;


    SSL_set_fd(data->client_tls_conn, clientSock);
    printf("try to ssl accept\n");


    data->up_read = event_new(sdata->evbase, clientSock, EV_READ|EV_PERSIST, up_read_cb, data);
    event_add(data->up_read, NULL);

    data->up_write = event_new(sdata->evbase, remoteSock, EV_WRITE|EV_PERSIST, up_write_cb, data);

    data->down_read = event_new(sdata->evbase, remoteSock, EV_READ|EV_PERSIST, down_read_cb, data);
    event_add(data->down_read, NULL);

    data->down_write = event_new(sdata->evbase, clientSock, EV_WRITE|EV_PERSIST, down_write_cb, data);

    char name0[100], port0[100], name1[100], port1[100];
    getnameinfo(&clientAddr, sizeof(struct sockaddr_storage), name0, 100, port0, 100, NI_NUMERICHOST|NI_NUMERICSERV);
    getnameinfo(&remoteAddr, sizeof(struct sockaddr_storage), name1, 100, port1, 100, NI_NUMERICHOST|NI_NUMERICSERV);


    printf("connection from %s:%s to %s:%s\n", name0, port0, name1, port1);


}







// switch to epoll if needed
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


    struct shared_data* sdata = calloc(1, sizeof(struct shared_data*));


    printf("ssl init begins\n");



    SSL_load_error_strings();   /* load all error messages */
    OpenSSL_add_all_algorithms();  /* load & register all cryptos, etc. */

    SSL_library_init();





    if ((access(CA_key_location, F_OK) == -1) || (access(CA_cert_location, F_OK) == -1)) {
        // something missing, regenerate private key and CA certificate
        generate_CA_cert(sdata->CA_key, sdata->CA_cert);
        printf("regenerate\n");
    }
    else {
        FILE *f = fopen(CA_key_location, "r");
        sdata->CA_key = PEM_read_PrivateKey(f, NULL, NULL, NULL);
        fclose(f);
        f = fopen(CA_cert_location, "r");
        sdata->CA_cert = PEM_read_X509(f, NULL, NULL, NULL);
        fclose(f);
        printf("use existing\n");
    }



    /*
    SSL_METHOD *tls_method = TLSv1_2_server_method();
    if (tls_method == NULL)
        printf("I died\n");
    */

    const long flags = SSL_OP_NO_SSLv2 | SSL_OP_NO_SSLv3 | SSL_OP_NO_COMPRESSION;

    sdata->remote_tls_ctx = SSL_CTX_new(TLS_client_method());
    SSL_CTX_set_options(sdata->remote_tls_ctx, flags);
    SSL_CTX_set_verify(sdata->remote_tls_ctx, SSL_VERIFY_PEER, NULL);
    SSL_CTX_set_verify_depth(sdata->remote_tls_ctx, 4);
    SSL_CTX_load_verify_file(sdata->remote_tls_ctx, "/etc/ssl/certs/ca-certificates.crt");



    sdata->client_tls_ctx = SSL_CTX_new(TLS_server_method());


    SSL_CTX_set_options(sdata->client_tls_ctx, flags);
    // should use the fake_remote_cert rather than the CAcert
    // SSL_CTX_use_certificate_file(sdata->client_tls_ctx, CA_cert_location, SSL_FILETYPE_PEM);
    SSL_CTX_use_PrivateKey_file(sdata->client_tls_ctx, CA_key_location, SSL_FILETYPE_PEM);


    if (sdata->client_tls_ctx == NULL)
    {
        printf("ssl conext fail\n");
        return -1;
    }

    printf("ssl finished\n");


    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0x1301, "TLS_AES_128_GCM_SHA256");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0x1302, "TLS_AES_256_GCM_SHA384");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0x1303, "TLS_CHACHA20_POLY1305_SHA256");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0xc02b, "ECDHE-ECDSA-AES128-GCM-SHA256");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0xc02f, "ECDHE-RSA-AES128-GCM-SHA256");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0xc02c, "ECDHE-ECDSA-AES256-GCM-SHA384");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0xc030, "ECDHE-RSA-AES256-GCM-SHA384");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0xcca9, "ECDHE-ECDSA-CHACHA20-POLY1305");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0xcca8, "ECDHE-RSA-CHACHA20-POLY1305");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0xc013, "ECDHE-RSA-AES128-SHA");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0xc014, "ECDHE-RSA-AES256-SHA");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0x009c, "AES128-GCM-SHA256");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0x009d, "AES256-GCM-SHA384");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0x002f, "AES128-SHA");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0x0035, "AES256-SHA");
    add_cipher(sdata->recognized_cipher, sdata->cipher_length, 0x000a, "DES-CBC3-SHA");




    sdata->evbase = event_base_new();
    struct event *accept_ev = event_new(sdata->evbase, listenSock, EV_READ | EV_PERSIST, accept_cb, (void *) sdata);


    event_add(accept_ev, NULL);
    event_base_dispatch(sdata->evbase);





    return 0;

}

