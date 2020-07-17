import logging

from gpgclip import gpg_messages

log = logging.getLogger(__name__)


class GPGClip(object):
    def __init__(self, gpg, clipboard):
        self.gpg = gpg
        self.clipboard = clipboard
        self.latest_imported_keys = []
        self.latest_primary_message = ''
        self.latest_clipboard_message = ''
        self.latest_encrypted_message = ''
        self.latest_decrypted_message = ''

    def _clear_state(self):
        self.latest_clipboard_message = ''
        self.latest_encrypted_message = ''
        self.latest_decrypted_message = ''

    def import_public_keys(self, public_keys):
        import_results = []
        for key in public_keys:
            import_result = self.gpg.import_keys(key)
            import_results.append(import_result.fingerprints)
            for fp in import_result.fingerprints:
                log.info("Imported public key: {}".format(fp))
        return import_results

    def main_loop(self):
        primary_content = self.clipboard.read_primary()

        if primary_content == self.latest_primary_message or primary_content == self.latest_encrypted_message:
            log.debug('No new primary content, skipping')
            return
        self.latest_primary_message = primary_content

        encrypted_messages = gpg_messages.get_encrypted_messages(primary_content)
        if encrypted_messages:
            log.info("Encrypted message found, decrypting")
            for message in encrypted_messages:
                decrypted_message = self.gpg.decrypt(message).data.decode("utf-8").strip()
                log.info("Decrypted message:\n{}".format(decrypted_message))
                # Setting decrypted message in primary selection
                self.clipboard.write_primary(decrypted_message)
                self._clear_state()
                self.latest_decrypted_message = decrypted_message
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
                    log.info("Valid signature from: {}".format(verification.username))
                # ToDo: make it appear in popup window?
            return verification

        public_keys = gpg_messages.get_pubkeys(primary_content)
        if public_keys:
            log.info("Public_keys found, importing them")
            self.latest_imported_keys = self.import_public_keys(public_keys)

        clipboard_content = self.clipboard.read_clipboard()
        # Because primary selection only exists on linux we store latest imported keys on memory so we can read the
        # both the key and message to encrypt from plain clipboard on successive iterations of the program.

        if clipboard_content == self.latest_clipboard_message or clipboard_content == self.latest_decrypted_message:
            log.debug('No new clipboard content, skipping')
            return

        if clipboard_content and \
                (clipboard_content != primary_content or not public_keys and not encrypted_messages and not signed_texts):
            if not self.latest_imported_keys:
                log.debug("Plain text found but I don't know which key to use to encrypt it")
                return

            log.info("Content found in clipboard, encrypting it and setting it in primary selection")
            if len(self.latest_imported_keys) > 1:
                log.warning("More than one key imported, using %s to encrypt".format(self.latest_imported_keys[0]))
            encrypted_message = self.gpg.encrypt(clipboard_content, recipients=self.latest_imported_keys[0], always_trust=True)
            if not encrypted_message.ok:
                log.error(encrypted_message.stderr)
            else:
                self._clear_state()
                self.latest_encrypted_message = encrypted_message.data.decode('utf-8')  # To avoid decrypting it on the next iteration
                self.clipboard.write_primary(self.latest_encrypted_message)
                self.latest_clipboard_message = clipboard_content
                log.debug("Encrypted message set in primary selection")
        else:
            log.debug("No clipboard content found, nothing to encrypt")
        return
