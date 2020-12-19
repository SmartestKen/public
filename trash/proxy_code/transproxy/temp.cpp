










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