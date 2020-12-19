#include <stdio.h>
// #include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>
// #include <errno.h>
// #include <poll.h>
#include <unistd.h>
#include <linux/netfilter_ipv4.h>
#include <linux/netfilter_ipv6/ip6_tables.h>
#include <event2/event.h>



void accept_cb(evutil_socket_t listenSock, short event, void *arg)
{

    // struct event_base *base = (struct event_base *) arg;
    struct sockaddr_storage clientAddr;
    socklen_t clientAddrlen = sizeof(clientAddr);
    int clientSock = accept(listenSock, (struct sockaddr*)&clientAddr, &clientAddrlen);

    if (clientSock == -1) {
        perror("accept");
        close(clientSock);
    }

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

}







// switch to libuv or boost:async if needed
int main(int argc, char *argv[]) {
    int listenSock;



    struct addrinfo hint, *proxyAddr;


    memset(&hint, 0, sizeof hint);
    // hint.ai_family = AF_UNSPEC;  // use IPv4 and/or IPv6, whatever is available
    hint.ai_family = AF_INET6;
    hint.ai_socktype = SOCK_STREAM;
    hint.ai_flags = AI_PASSIVE;     // fill in my IP for me

    if (getaddrinfo(NULL, "8080", &hint, &proxyAddr) != 0) {
        fprintf(stderr, "getaddrinfo failed\n");
        exit(1);
    }



    // listenSock = socket(proxyAddr->ai_family, proxyAddr->ai_socktype | SOCK_NONBLOCK, proxyAddr->ai_protocol);
    listenSock = socket(proxyAddr->ai_family, proxyAddr->ai_socktype, proxyAddr->ai_protocol);
    if (listenSock == -1) {
        fprintf(stderr, "socket failed\n");
    }
    int opt[] = {0, 1, 1, 1};
    setsockopt(listenSock, IPPROTO_IPV6, IPV6_V6ONLY, &opt[0], sizeof(int));
    setsockopt(listenSock, SOL_SOCKET, SO_REUSEADDR, &opt[1], sizeof(int));
    setsockopt(listenSock, SOL_SOCKET, SO_KEEPALIVE, &opt[2], sizeof(int));
    // check if this option can pass through transparent check?
    setsockopt(listenSock, SOL_IP, IP_TRANSPARENT, &opt[3], sizeof(int));


    if (bind(listenSock, proxyAddr->ai_addr, proxyAddr->ai_addrlen) != 0)
        printf("bind failed\n");
    if (listen(listenSock, 20) != 0)
        printf("listen failed\n");

    freeaddrinfo(proxyAddr);

    printf("%s\n", "I reach here");
    struct event_base *evbase;
    struct event *listenEv = event_new(evbase, listenSock, EV_READ | EV_PERSIST, accept_cb, (void *) evbase);

}


