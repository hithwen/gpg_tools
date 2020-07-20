import logging
import platform
import pyperclip


log = logging.getLogger(__name__)


class ClipWrapper(object):
    def __init__(self):
        self.has_primary = False
        if self._is_linux():
            try:
                pyperclip.set_clipboard('xclip')
                log.debug("Set clipboard driver to xclip")
                self.has_primary = True
            except Exception as xclip_exception:
                try:
                    pyperclip.set_clipboard('xsel')
                    log.debug("Set clipboard driver to xclip")
                    self.has_primary = True
                except Exception as xsel_exception:
                    log.error("Could not select a clipboard driver with primary selection. Errors:\n{}\n{}".format(
                        xclip_exception, xsel_exception))

    @staticmethod
    def _is_linux():
        return platform.system() == 'Linux'

    def read_primary(self):
        if self.has_primary:
            return pyperclip.paste(primary=True)
        else:
            log.debug("Primary selection does not work in this system, using clipboard instead")
            return self.read_clipboard()

    @staticmethod
    def read_clipboard():
        return pyperclip.paste()

    @staticmethod
    def write_clipboard(message):
        pyperclip.copy(message)

    def write_primary(self, message):
        if self.has_primary:
            return pyperclip.copy(message, primary=True)
        else:
            log.debug("Primary selection does not work in this system, using clipboard instead")
            return self.write_clipboard(message)
