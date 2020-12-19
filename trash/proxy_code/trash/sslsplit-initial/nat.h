#ifndef NAT_H
#define NAT_H

#include <sys/types.h>
#include <sys/socket.h>

#include <event2/util.h>

typedef int (*nat_lookup_cb_t)(struct sockaddr *, socklen_t *, evutil_socket_t,
                               struct sockaddr *, socklen_t);
typedef int (*nat_socket_cb_t)(evutil_socket_t);

int nat_exist(const char *);
nat_lookup_cb_t nat_getlookupcb(const char *);
nat_socket_cb_t nat_getsocketcb(const char *);
int nat_ipv6ready(const char *);

const char *nat_getdefaultname(void);
void nat_list_engines(void);
int nat_preinit(void);
int nat_init(void);
void nat_fini(void);
void nat_version(void);

#endif /* !NAT_H */

/* vim: set noet ft=c: */
