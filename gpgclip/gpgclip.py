import logging

from gpgclip import gpg_messages

log = logging.getLogger(__name__)


def import_public_keys(gpg, public_keys):
    import_results = []
    for key in public_keys:
        import_result = gpg.import_keys(key)
        import_results.append(import_result.fingerprints)
        log.info("Imported public key: {}", import_result.fingerprints)
    return import_results


def main_loop(gpg, clipboard):
    primary_content = clipboard.read_primary()
    public_keys = gpg_messages.get_pubkeys(primary_content)

    if public_keys:
        log.debug("Public_keys found, adding importing them")
        imported_keys = import_public_keys(gpg, public_keys)
        # encrypt clipboard to the key in the primary selection
        clipboard_content = clipboard.read_clipboard()
        if clipboard_content:
            log.debug("Content found in clipboard, encrypting it")
            if len(imported_keys) > 1:
                log.warning("More than one key imported, using {} to encrypt", imported_keys[0])
            encrypted_message = gpg.encrypt(clipboard_content, recipients=imported_keys[0], always_trust=True)
            if not encrypted_message.ok:
                log.error(encrypted_message.stderr)
            else:
                clipboard.write_primary(encrypted_message.data.decode("utf-8"))  # Set encrypted message in primary selection
                log.debug("Encrypted message set in primary selection")
        else:
            log.debug("No clipboard content found, nothing to encrypt")
        return

    encrypted_messages = gpg_messages.get_encrypted_messages(primary_content)
    if encrypted_messages:
        log.debug("Encrypted message found, decrypting")
        for message in encrypted_messages:
            decrypted_message = gpg.decrypt(message).data.decode("utf-8").strip()
            log.info("Decrypted message:\n{}".format(decrypted_message))
            # Setting decrypted message in primary selection
            clipboard.write_primary(decrypted_message)
            # ToDo: make it appear in popup window? (maybe with tkinter)
        return

    signed_texts = gpg_messages.get_signed_messages(primary_content)
    if signed_texts:
        log.debug("Signed message found, verifying")
        for signed_text in signed_texts:
            verification = gpg.verify(signed_text)
            if not verification.valid:
                log.error("Could not verify signature, {}", verification.stderr)
            else:
                log.info("Valid signature from: {}", verification.username)
            # ToDo: make it appear in popup window?
        return verification
