from Phidget22.PhidgetException import *
import Phidget22.Devices.DigitalInput

import .PhidgetHelperFunctions

from phidget_python_api.phidget import Phidget, ChannelInfo

class DigitalInputInfo():
    def __init__(self):
        self.channel_info = ChannelInfo()
        self.channel_info.is_hub_port_device = True

class DigitalInput(Phidget):
    def __init__(self, digital_input_info):
        super().__init__(digital_input_info.channel_info)
        self._digital_input_info = digital_input_info

        try:
            self._handle = Phidget22.Devices.DigitalInput()
        except PhidgetException as e:
            DisplayError(e)
            raise

        open_wait_for_attachment(self._handle)
        _setup()

    def _setup(self):
        pass

    def close(self):
        self.set_on_state_change_handler(None)
        super().close(self._handle)

    # void onStateChange(self, state)
    def set_on_state_change_handler(self, on_state_change_handler):
        self._handle.setOnStateChangeHandler(on_state_change_handler)

    def get_state(self):
        return self._handle.getState()
