"""Class to represent Error State
"""
import subprocess   # nosec #pylint-disable type: ignore
import json_config
from .base_state import State
from .lights import lights

config = json_config.connect('config.json')


class ErrorState(State):
    """Error State inherits from the State class. If any error is encountered in any state, it should transition to
    error mentioning the error in the payload.
    """

    def on_enter(self, payload=None):
        """Method executed on entry to Error State. Relevant error message is spoken.
        :param payload: String mentioning the error encountered.
        :return: None
        """
        if payload == 'RecognitionError':
            self.notify_renderer('error', 'recognition')
            lights.speak()
            subprocess.call(['play', 'extras/recognition-error.wav'])   # nosec #pylint-disable type: ignore
            lights.off()
        elif payload == 'ConnectionError':
            self.notify_renderer('error', 'connection')
            config['default_tts'] = 'flite'
            config['default_stt'] = 'pocket_sphinx'
            lights.speak()
            subprocess.call(['play', 'extras/connect-error.wav'])   # nosec #pylint-disable type: ignore
            lights.off()
            print("Changed to offline providers")
        else:
            self.notify_renderer('error')
            lights.speak()
            subprocess.call(['play', 'extras/problem.wav'])   # nosec #pylint-disable type: ignore
            lights.off()

        self.transition(self.allowedStateTransitions.get('idle'))

    def on_exit(self):
        """Method executed on exit from the Error State.
        :return: None
        """
        pass
