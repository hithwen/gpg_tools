import tempfile

import gnupg

from gpgclip.clip_wrapper import ClipWrapper
from gpgclip.gpgclip import GPGClip
from .common import PUBKEY, PRIVATE_KEY, ENCRYPTED_MESSAGE, ATTACHED_SIGNED_MESSAGE
from mock import MagicMock

SAMPLE_MESSAGE = '''
Sample text


'''


def test_add_key_and_encrypt_message():
    # find PGP public key
    # Add it to the PGP key ring, and encrypt clipboard to the key in the primary selection
    with tempfile.TemporaryDirectory() as tmp_dir:
        gpg = gnupg.GPG(gnupghome=tmp_dir)
        clipboard = MagicMock(ClipWrapper)
        gpgclip = GPGClip(gpg, clipboard)

        clipboard.read_primary.return_value = PUBKEY
        clipboard.read_clipboard.return_value = SAMPLE_MESSAGE
        gpgclip.main_loop()
        encrypted_message = clipboard.write_primary.call_args_list[0].args[0]

    with tempfile.TemporaryDirectory() as tmp_dir:
        gpg = gnupg.GPG(gnupghome=tmp_dir)
        gpg.import_keys(PRIVATE_KEY)
        original_message = gpg.decrypt(encrypted_message).data.decode("utf-8")
        assert original_message == SAMPLE_MESSAGE


def test_decrypt_message_and_strip_it():
    clipboard = MagicMock(ClipWrapper)
    with tempfile.TemporaryDirectory() as tmp_dir:
        gpg = gnupg.GPG(gnupghome=tmp_dir)
        gpg.import_keys(PRIVATE_KEY)
        clipboard.read_primary.return_value = ENCRYPTED_MESSAGE

        gpgclip = GPGClip(gpg, clipboard)
        gpgclip.main_loop()
        decrypted_message = clipboard.write_primary.call_args_list[0].args[0]
    assert decrypted_message == 'Sample text'


def test_verify_good_signature():
    clipboard = MagicMock(ClipWrapper)
    with tempfile.TemporaryDirectory() as tmp_dir:
        gpg = gnupg.GPG(gnupghome=tmp_dir)
        gpg.import_keys(PUBKEY)
        clipboard.read_primary.return_value = ATTACHED_SIGNED_MESSAGE

        gpgclip = GPGClip(gpg, clipboard)
        verify = gpgclip.main_loop()
    assert verify.valid
