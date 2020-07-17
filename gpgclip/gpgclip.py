import logging
import platform

from gpgclip import gpg_messages

log = logging.getLogger(__name__)


class GPGClip(object):
    def __init__(self, gpg, clipboard):
        self.gpg = gpg
        self.clipboard = clipboard
        self.latest_imported_key = None

    def import_public_keys(self, public_keys):
        import_results = []
        for key in public_keys:
            import_result = self.gpg.import_keys(key)
            import_results.append(import_result.fingerprints)
            log.info("Imported public key: {}", import_result.fingerprints)
        return import_results

    def main_loop(self):
        primary_content = self.clipboard.read_primary()

        encrypted_messages = gpg_messages.get_encrypted_messages(primary_content)
        if encrypted_messages:
            log.debug("Encrypted message found, decrypting")
            for message in encrypted_messages:
                decrypted_message = self.gpg.decrypt(message).data.decode("utf-8").strip()
                log.info("Decrypted message:\n{}".format(decrypted_message))
                # Setting decrypted message in primary selection
                self.clipboard.write_primary(decrypted_message)
                # ToDo: make it appear in popup window? (maybe with tkinter)
            return

        signed_texts = gpg_messages.get_signed_messages(primary_content)
        if signed_texts:
            log.debug("Signed message found, verifying")
            for signed_text in signed_texts:
                verification = self.gpg.verify(signed_text)
                if not verification.valid:
                    log.error("Could not verify signature, {}", verification.stderr)
                else:
                    log.info("Valid signature from: {}", verification.username)
                # ToDo: make it appear in popup window?
            return verification

        public_keys = gpg_messages.get_pubkeys(primary_content)
        if public_keys:
            log.debug("Public_keys found, adding importing them")
            self.latest_imported_key = self.import_public_keys(public_keys)

        clipboard_content = self.clipboard.read_clipboard()
        # Because primary selection only exists on linux we store latest imported keys on memory so we can read the
        # both the key and message to encrypt from plain clipboard on successive iterations of the program.

        if clipboard_content and platform.system() == 'Linux' or not public_keys and not encrypted_messages and not signed_texts:
            log.debug("Content found in clipboard, encrypting it")
            if len(self.latest_imported_key) > 1:
                log.warning("More than one key imported, using {} to encrypt", self.latest_imported_key[0])
            encrypted_message = self.gpg.encrypt(clipboard_content, recipients=self.latest_imported_key[0], always_trust=True)
            if not encrypted_message.ok:
                log.error(encrypted_message.stderr)
            else:
                self.clipboard.write_primary(
                    encrypted_message.data.decode("utf-8"))  # Set encrypted message in primary selection
                log.debug("Encrypted message set in primary selection")
        else:
            log.debug("No clipboard content found, nothing to encrypt")
        return
