import logging
from time import sleep

import gnupg

from gpgclip.clip_wrapper import ClipWrapper
from gpgclip.gpgclip import GPGClip

logging.basicConfig(level=logging.INFO)


def main():
    gpg = gnupg.GPG(use_agent=True)
    gpgclip = GPGClip(gpg, ClipWrapper())

    while True:
        gpgclip.main_loop()
        sleep(1)
