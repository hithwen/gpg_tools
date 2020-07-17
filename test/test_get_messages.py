from gpgclip.gpg_messages import get_pubkeys, get_encrypted_messages, get_signed_messages
from .common import PUBKEY, ENCRYPTED_MESSAGE, SIGNED_MESSAGE, ATTACHED_SIGNED_MESSAGE


def test_get_pubkeys():
    pubkeys = get_pubkeys(PUBKEY)
    assert pubkeys[0] == PUBKEY.strip()


def test_get_encryped_messages():
    messages = get_encrypted_messages(ENCRYPTED_MESSAGE)
    assert messages[0] == ENCRYPTED_MESSAGE.strip()


def test_get_signed_messages():
    messages = get_signed_messages(ATTACHED_SIGNED_MESSAGE)
    assert messages[0] == ATTACHED_SIGNED_MESSAGE.strip()
