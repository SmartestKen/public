/*
 * SSLsplit - transparent and scalable SSL/TLS interception
 * Copyright (c) 2009-2012, Daniel Roethlisberger <daniel@roe.ch>
 * All rights reserved.
 * http://www.roe.ch/SSLsplit
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice unmodified, this list of conditions, and the following
 *    disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef SSL_H
#define SSL_H

#include "attrib.h"

#include <openssl/opensslv.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/rand.h>
#include <openssl/x509.h>
#include <openssl/x509v3.h>

#if (OPENSSL_VERSION_NUMBER < 0x10000000L) && !defined(OPENSSL_NO_THREADID)
#define OPENSSL_NO_THREADID
#endif
#if (OPENSSL_VERSION_NUMBER < 0x0090806FL) && !defined(OPENSSL_NO_TLSEXT)
#define OPENSSL_NO_TLSEXT
#endif
#if (OPENSSL_VERSION_NUMBER < 0x1000005FL) && !defined(OPENSSL_NO_ECDH)
#define OPENSSL_NO_ECDH
#endif
#if (OPENSSL_VERSION_NUMBER < 0x0090802FL) && !defined(OPENSSL_NO_ECDSA)
#define OPENSSL_NO_ECDSA
#endif
#if (OPENSSL_VERSION_NUMBER < 0x0090802FL) && !defined(OPENSSL_NO_EC)
#define OPENSSL_NO_EC
#endif

void ssl_openssl_version(void);
int ssl_init(void);
void ssl_fini(void);

#ifndef OPENSSL_NO_DH
DH * ssl_tmp_dh_callback(SSL *, int, int) NONNULL();
DH * ssl_dh_load(const char *) NONNULL();
void ssl_dh_refcount_inc(DH *) NONNULL();
#endif /* !OPENSSL_NO_DH */

#ifndef OPENSSL_NO_ECDH
#define SSL_EC_KEY_CURVE_DEFAULT "prime256v1"
EC_KEY * ssl_ecdh_by_name(const char *);
#endif /* !OPENSSL_NO_ECDH */

EVP_PKEY * ssl_key_load(const char *) NONNULL();
EVP_PKEY * ssl_key_genrsa(const int);
void ssl_key_refcount_inc(EVP_PKEY *) NONNULL();

#ifndef OPENSSL_NO_TLSEXT
int ssl_x509_v3ext_add(X509V3_CTX *, X509 *, char *, char *) NONNULL();
int ssl_x509_v3ext_copy_by_nid(X509 *, X509 *, int) NONNULL();
#endif /* !OPENSSL_NO_TLSEXT */
int ssl_x509_serial_copyrand(X509 *, X509 *) NONNULL();
X509 * ssl_x509_forge(X509 *, EVP_PKEY *, X509 *, const char *, EVP_PKEY *) \
       NONNULL(1,2,3,5) MALLOC;
X509 * ssl_x509_load(const char *) NONNULL() MALLOC;
char * ssl_x509_subject(X509 *) NONNULL() MALLOC;
char * ssl_x509_subject_cn(X509 *, size_t *) NONNULL() MALLOC;
#define SSL_X509_FPRSZ 20
int ssl_x509_fingerprint_sha1(X509 *, unsigned char *) NONNULL();
int ssl_x509_names_match(X509 *, const char *) NONNULL();
char * ssl_x509_names_to_str(X509 *, size_t) NONNULL() MALLOC;
char ** ssl_x509_names(X509 *) NONNULL() MALLOC;
int ssl_x509_is_valid(X509 *) NONNULL();
char * ssl_x509_to_str(X509 *) NONNULL() MALLOC;
char * ssl_x509_to_pem(X509 *) NONNULL() MALLOC;
void ssl_x509_refcount_inc(X509 *) NONNULL();

int ssl_x509chain_load(X509 **, STACK_OF(X509) **, const char *) NONNULL(2,3);
void ssl_x509chain_use(SSL_CTX *, X509 *, STACK_OF(X509) *) NONNULL();

char * ssl_session_to_str(SSL_SESSION *) NONNULL() MALLOC;
int ssl_session_is_valid(SSL_SESSION *) NONNULL();

#ifndef OPENSSL_NO_TLSEXT
char * ssl_tls_clienthello_parse_sni(const unsigned char *, ssize_t *) \
       NONNULL() MALLOC;
#endif /* !OPENSSL_NO_TLSEXT */
int ssl_dnsname_match(const char *, size_t, const char *, size_t) NONNULL();
char * ssl_wildcardify(const char *) NONNULL() MALLOC;

#endif /* !SSL_H */

/* vim: set noet ft=c: */
