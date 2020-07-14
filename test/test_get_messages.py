from gpgclip.gpg_messages import get_pubkey

PUBKEY_ONLY = '''
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQINBFRUAGoBEACuk6ze2V2pZtScf1Ul25N2CX19AeL7sVYwnyrTYuWdG2FmJx4x
DLTLVUazp2AEm/JhskulL/7VCZPyg7ynf+o20Tu9/6zUD7p0rnQA2k3Dz+7dKHHh
eEsIl5EZyFy1XodhUnEIjel2nGe6f1OO7Dr3UIEQw5JnkZyqMcbLCu9sM2twFyfa
a8JNghfjltLJs3/UjJ8ZnGGByMmWxrWQUItMpQjGr99nZf4L+IPxy2i8O8WQewB5

[... snip - full example below ...]

fvfidBGruUYC+mTw7CusaCOQbBuZBiYduFgH8hRW97KLmHn0xzB1FV++KI7syo8q
XGo8Un24WP40IT78XjKO
=nUop
-----END PGP PUBLIC KEY BLOCK-----
'''


def test_get_pubkey():
    pubkeys = get_pubkey(PUBKEY_ONLY)
    assert pubkeys[0] == PUBKEY_ONLY.strip()
