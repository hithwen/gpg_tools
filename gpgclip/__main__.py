from time import sleep

import gnupg
import klembord
import pyperclip

from gpgclip.gpgclip import main_loop

gpg = gnupg.GPG(use_agent=True)
klembord.init(selection='PRIMARY')
while True:
    main_loop(klembord, pyperclip, gpg)
    sleep(1)
