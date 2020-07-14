import re

# Regexes
PUBKEY_RE = '(-----BEGIN PGP PUBLIC KEY BLOCK-----(.|\n)*-----END PGP PUBLIC KEY BLOCK-----)'


def get_pubkey(text):
    pubkey_re = re.compile(PUBKEY_RE, re.MULTILINE)
    groups = pubkey_re.findall(text)
    return [g[0] for g in groups]

