
import time
from src.utils.executor import run_cmd

class MediaController:
    KEY_PLAY = ['207:1', '207:0']
    KEY_PAUSE = ['119:1', '119:0']
    KEY_NEXT = ['163:1', '163:0']
    KEY_PREV = ['165:1', '165:0']
    KEY_VOL_UP = ['115:1', '115:0']
    KEY_VOL_DOWN = ['114:1', '114:0']

    def __init__(self, cooldown: float = 0.5):
        self.last_trigger = 0
        self.cooldown = cooldown

    def _trigger(self, key_sequence: list) -> bool:
        if time.time() - self.last_trigger > self.cooldown:
            run_cmd(['ydotool', 'key'] + key_sequence)
            self.last_trigger = time.time()
            return True
        return False

    def play(self) -> bool: return self._trigger(self.KEY_PLAY)
    def pause(self) -> bool: return self._trigger(self.KEY_PAUSE)
    def next(self) -> bool: return self._trigger(self.KEY_NEXT)
    def prev(self) -> bool: return self._trigger(self.KEY_PREV)
    
    def volume_change(self, increase: bool):
        key = self.KEY_VOL_UP if increase else self.KEY_VOL_DOWN
        run_cmd(['ydotool', 'key'] + key)