import pyperclip
import logging
import re




logger = logging.getLogger(__name__)


def main():
    clipboard_content = pyperclip.paste()
    if PUBLIC_KEY_START in clipboard_content:
        if PUBLIC_KEY_END not in clipboard_content:
            logger.error("Incomplete GPG public key detected. Don't know how to proceed")
            return


