from time import sleep

import gnupg

from gpgclip.clip_wrapper import ClipWrapper
from gpgclip.gpgclip import main_loop

gpg = gnupg.GPG(use_agent=True)
while True:
    main_loop(gpg, ClipWrapper())
    sleep(1)
