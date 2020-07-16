import gnupg
import pyperclip
import logging

from gpgclip import gpg_messages

log = logging.getLogger(__name__)


def main():
    clipboard_content = pyperclip.paste()
    public_keys = gpg_messages.get_pubkeys(clipboard_content)
    gpg = gnupg.GPG(use_agent=True)
    for key in public_keys:
        import_result = gpg.import_keys(key)
        log.info("Imported public key: {}", import_result)
    decrypted_data = gpg.decrypt(data)


