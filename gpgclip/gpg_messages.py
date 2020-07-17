import re

# Regexes
PUBKEY_RE = '(-----BEGIN PGP PUBLIC KEY BLOCK-----(.|\n)*-----END PGP PUBLIC KEY BLOCK-----)'
ENCRYPTED_RE = '(-----BEGIN PGP MESSAGE-----(.|\n)*-----END PGP MESSAGE-----)'
SIGNED_RE = '(-----BEGIN PGP SIGNED MESSAGE-----(.|\n)*\n-----BEGIN PGP SIGNATURE-----(.|\n)*-----END PGP SIGNATURE-----)'


def get_pubkeys(text):
    pubkey_re = re.compile(PUBKEY_RE, re.MULTILINE)
    groups = pubkey_re.findall(text)
    return [g[0] for g in groups]


def get_encrypted_messages(text):
    encrypted_re = re.compile(ENCRYPTED_RE, re.MULTILINE)
    groups = encrypted_re.findall(text)
    return [g[0] for g in groups]


def get_signed_messages(text):
    pubkey_re = re.compile(SIGNED_RE, re.MULTILINE)
    groups = pubkey_re.findall(text)
    return [g[0] for g in groups]
