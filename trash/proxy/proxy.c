int main()
{
    // prepare sockAddr for its use in bind
    struct addrinfo hint, *sockAddr;

    memset(&hint, 0, sizeof hint);
    hint.ai_family = AF_INET6;
    hint.ai_socktype = SOCK_STREAM;
    hint.ai_flags = AI_PASSIVE;

    if (getaddrinfo(NULL, "8080", &hint, &sockAddr) != 0) {
        fprintf(stderr, "getaddrinfo failed\n");
        exit(1);
    }


    // init socket that listen local 8080
    int sock = socket(AF_INET6, SOCK_STREAM, 0);
    if (sock == -1) {
        fprintf(stderr, "socket failed\n");
    }

    int opt[] = {1, 1, 0};
    setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &opt[0], sizeof(int));
    setsockopt(sock, SOL_SOCKET, SO_KEEPALIVE, &opt[1], sizeof(int));
    setsockopt(sock, IPPROTO_IPV6, IPV6_V6ONLY, &opt[2], sizeof(int));


    // bind and listen
    if (bind(listenSock, sockAddr->ai_addr, sockAddr->ai_addrlen) != 0)
        printf("bind failed\n");
    if (listen(listenSock, 20) != 0)
        printf("listen failed\n");
    freeaddrinfo(sockAddr);

