# inherited
VERSION?=	unknown
OPENSSL?=	openssl
MKDIR?=		mkdir

# OpenSSL settings
CA_SUBJECT?=	'/O=SSLsplit Root CA/CN=SSLsplit Root CA/'
CA_DAYS?=	3650
CONFIG:=	x509v3ca.cnf
CONFIG_EXT:=	v3_ca

all: rsa dsa ec targets

session: session.pem

dh: dh512.param dh1024.param dh2048.param

rsa: rsa.pem

dsa: dsa.pem

ec: ec.pem

dh512.param:
	$(OPENSSL) dhparam -out $@ -2 512

dh1024.param:
	$(OPENSSL) dhparam -out $@ -2 1024

dh2048.param:
	$(OPENSSL) dhparam -out $@ -2 2048

dsa.param:
	$(OPENSSL) dsaparam -out $@ 1024

dsa.key: dsa.param
	$(OPENSSL) gendsa -out $@ $<

rsa.key:
	$(OPENSSL) genrsa -out $@ 1024

ec.key:
	$(OPENSSL) ecparam -out $@ -name prime192v1 -genkey

%.crt: %.key
	$(OPENSSL) req -new -nodes -x509 -sha1 -out $@ -key $< \
		-config $(CONFIG) -extensions $(CONFIG_EXT) \
		-subj $(CA_SUBJECT) \
		-set_serial 0 -days $(CA_DAYS)

%.pem: %.crt %.key
	cat $^ >$@

targets: rsa.crt
	$(MKDIR) targets
	$(OPENSSL) genrsa -out targets/daniel.roe.ch.key 1024
	$(OPENSSL) req -new -sha1 -subj '/C=CH/CN=daniel.roe.ch/' \
		-key targets/daniel.roe.ch.key \
		-out targets/daniel.roe.ch.csr
	$(OPENSSL) x509 -req -sha1 -CAcreateserial -days 365 \
		-CA rsa.crt -CAkey rsa.key \
		-in targets/daniel.roe.ch.csr \
		-out targets/daniel.roe.ch.crt
	cat targets/daniel.roe.ch.crt targets/daniel.roe.ch.key rsa.crt \
		>targets/daniel.roe.ch.pem
	$(RM) targets/daniel.roe.ch.{key,csr,crt}
	$(OPENSSL) genrsa -out targets/wildcard.roe.ch.key 1024
	$(OPENSSL) req -new -sha1 -subj '/C=CH/CN=*.roe.ch/' \
		-key targets/wildcard.roe.ch.key \
		-out targets/wildcard.roe.ch.csr
	$(OPENSSL) x509 -req -sha1 -CAcreateserial -days 365 \
		-CA rsa.crt -CAkey rsa.key \
		-in targets/wildcard.roe.ch.csr \
		-out targets/wildcard.roe.ch.crt
	cat targets/wildcard.roe.ch.crt targets/wildcard.roe.ch.key rsa.crt \
		>targets/wildcard.roe.ch.pem
	$(RM) targets/wildcard.roe.ch.{key,csr,crt} rsa.srl

# openssl s_server cannot be easily controlled from scripts; it is
# more robust to just connect to a real server to create a session
session.pem:
	echo -e 'GET /test/SSLsplit-$(VERSION) HTTP/1.1\r\nHost:' \
		'daniel.roe.ch\r\nConnection: close\r\n\r\n' | \
		$(OPENSSL) s_client -connect daniel.roe.ch:443 \
		-quiet -no_ign_eof -sess_out $@ >/dev/null 2>&1
	test -r $@

clean:
	rm -rf rsa.* dsa.* ec.* dh*.param targets *.srl session.pem

.PHONY: all clean rsa dsa ec dh dhall session

