import logging
import platform
import pyperclip


log = logging.getLogger(__name__)


class ClipWrapper(object):
    def _is_linux(self):
        return platform.system() == 'Linux'

    def read_primary(self):
        if self._is_linux():
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
        if self._is_linux():
            return pyperclip.copy(message, primary=True)
        else:
            log.debug("Primary selection does not work in this system, using clipboard instead")
            return self.write_clipboard(message)
