import tempfile

from gpgclip import gpgclip
from .common import PUBKEY, SIGNED_MESSAGE, PRIVATE_KEY, ENCRYPTED_MESSAGE
import gnupg
from mock import MagicMock

SAMPLE_MESSAGE = '''
Sample text


'''


def test_add_key_and_encrypt_message():
    # find PGP public key
    # Add it to the PGP key ring, and encrypt clipboard to the key in the primary selection
    with tempfile.TemporaryDirectory() as tmp_dir:
        gpg = gnupg.GPG(gnupghome=tmp_dir)
        primary_selection = MagicMock()
        clipboard = MagicMock()

        primary_selection.get_text.return_value = PUBKEY
        clipboard.paste.return_value = SAMPLE_MESSAGE
        gpgclip.main_loop(gpg, primary_selection, clipboard)
        encrypted_message = primary_selection.set_text.call_args_list[0].args[0]

    with tempfile.TemporaryDirectory() as tmp_dir:
        gpg = gnupg.GPG(gnupghome=tmp_dir)
        gpg.import_keys(PRIVATE_KEY)
        original_message = gpg.decrypt(encrypted_message).data.decode("utf-8")
        assert original_message == SAMPLE_MESSAGE


def test_decrypt_message_and_strip_it():
    primary_selection = MagicMock()

    with tempfile.TemporaryDirectory() as tmp_dir:
        gpg = gnupg.GPG(gnupghome=tmp_dir)
        gpg.import_keys(PRIVATE_KEY)
        primary_selection.get_text.return_value = ENCRYPTED_MESSAGE
        gpgclip.main_loop(gpg, primary_selection, None)
        decrypted_message = primary_selection.set_text.call_args_list[0].args[0]
    assert decrypted_message == 'Sample text'

