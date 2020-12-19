import urllib.request

fp = urllib.request.urlopen("http://www.google.com/search?source=hp&ei=_2aFXtHwMMT3-gSdrZXoDA&q=qeqcvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq&oq=qeqcvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq&gs_lcp=CgZwc3ktYWIQAzoCCAA6BQgAEIMBOgQIABAKOgQIABANOgYIABANEApQmwRYhURgiVBoAHAAeAGAAZMBiAGnRJIBBTg2LjExmAEEoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwiR7JL38MjoAhXEu54KHZ1WBc0Q4dUDCAg&uact=5")
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()

print(mystr)

import OpenSSL



def create_ca(organization, cn, exp, key_size):
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, key_size)
    cert = OpenSSL.crypto.X509()
    cert.set_serial_number(int(time.time() * 10000))
    cert.set_version(2)
    cert.get_subject().CN = cn
    cert.get_subject().O = organization
    cert.gmtime_adj_notBefore(-3600 * 48)
    cert.gmtime_adj_notAfter(exp)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.add_extensions([
        OpenSSL.crypto.X509Extension(
            b"basicConstraints",
            True,
            b"CA:TRUE"
        ),
        OpenSSL.crypto.X509Extension(
            b"nsCertType",
            False,
            b"sslCA"
        ),
        OpenSSL.crypto.X509Extension(
            b"extendedKeyUsage",
            False,
            b"serverAuth,clientAuth,emailProtection,timeStamping,msCodeInd,msCodeCom,msCTLSign,msSGC,msEFS,nsSGC"
        ),
        OpenSSL.crypto.X509Extension(
            b"keyUsage",
            True,
            b"keyCertSign, cRLSign"
        ),
        OpenSSL.crypto.X509Extension(
            b"subjectKeyIdentifier",
            False,
            b"hash",
            subject=cert
        ),
    ])
    cert.sign(key, "sha256")
    return key, cert


def dummy_cert(privkey, cacert, commonname, sans, organization):
    """
        Generates a dummy certificate.

        privkey: CA private key
        cacert: CA certificate
        commonname: Common name for the generated certificate.
        sans: A list of Subject Alternate Names.
        organization: Organization name for the generated certificate.

        Returns cert if operation succeeded, None if not.
    """
    ss = []
    for i in sans:
        try:
            ipaddress.ip_address(i.decode("ascii"))
        except ValueError:
            ss.append(b"DNS:%s" % i)
        else:
            ss.append(b"IP:%s" % i)
    ss = b", ".join(ss)

    cert = OpenSSL.crypto.X509()
    cert.gmtime_adj_notBefore(-3600 * 48)
    cert.gmtime_adj_notAfter(DEFAULT_EXP_DUMMY_CERT)
    cert.set_issuer(cacert.get_subject())
    if commonname is not None and len(commonname) < 64:
        cert.get_subject().CN = commonname
    if organization is not None:
        cert.get_subject().O = organization
    cert.set_serial_number(int(time.time() * 10000))
    if ss:
        cert.set_version(2)
        cert.add_extensions(
            [OpenSSL.crypto.X509Extension(b"subjectAltName", False, ss)])
    cert.add_extensions([
        OpenSSL.crypto.X509Extension(
            b"extendedKeyUsage",
            False,
            b"serverAuth,clientAuth"
        )
    ])
    cert.set_pubkey(cacert.get_pubkey())
    cert.sign(privkey, "sha256")
    return Cert(cert)