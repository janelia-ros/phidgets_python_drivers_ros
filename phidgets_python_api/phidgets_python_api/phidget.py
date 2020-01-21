import Phidget22.Phidget
import Phidget22.PhidgetException

import .PhidgetHelperFunctions

class ChannelInfo():
    def __init__(self):
        self.serial_number = Phidget22.Phidget.ANY_SERIAL_NUMBER
        self.label = Phidget22.Phidget.ANY_LABEL
        self.channel = Phidget22.Phidget.ANY_CHANNEL
        self.hub_port = Phidget22.Phidget.ANY_HUB_PORT
        self.is_hub_port_device = False
        self.timeout = Phidget22.Phidget.DEFAULT_TIMEOUT

class Phidget:
    def __init__(self, channel_info):
        self._channel_info = channel_info

    def _open_wait_for_attachment(self, handle):
        handle.setDeviceSerialNumber(self._channel_info.serial_number)
        handle.setDeviceLabel(self._channel_info.label)
        handle.setHubPort(self._channel_info.hubPort)
        handle.setIsHubPortDevice(self._channel_info.isHubPortDevice)
        handle.setChannel(self._channel_info.channel)

        self._stepper.openWaitForAttachment(self._stepper_info.attachment_timeout)

    def _setup_channel(self, channel, info):

        channel.setOnAttachHandler(self._on_attach_handler)
        channel.setOnDetachHandler(self._on_detach_handler)
        channel.setOnErrorHandler(self._on_error_handler)

    def _on_attach_handler(self, ph):
        try:
            channel_class_name = ph.getChannelClassName()
            serial_number = ph.getDeviceSerialNumber()
            channel = ph.getChannel()
            hub_port = ph.getHubPort()
            if ph.getIsHubPortDevice():
                msg = 'home switch {0} attached on hub port {1} on serial number {2}'.format(self._name, hub_port, serial_number)
                self._logger.info(msg)
            else:
                msg = 'stepper {0} attached on hub port {1} on serial number {2}'.format(self._name, hub_port, serial_number)
                self._logger.info(msg)

            try:
                ph.setDataInterval(self._stepper_info.data_interval)
            except AttributeError:
                pass
            except PhidgetException as e:
                DisplayError(e)
                return

        except PhidgetException as e:
            DisplayError(e)
            traceback.print_exc()
            return

    def _on_detach_handler(self, ph):
        try:
            channel_class_name = ph.getChannelClassName()
            serial_number = ph.getDeviceSerialNumber()
            channel = ph.getChannel()
            if ph.getIsHubPortDevice():
                msg = 'home switch {0} detached on hub port {1} on serial number {2}'.format(self._name, hub_port, serial_number)
                self._logger.info(msg)
            else:
                msg = 'stepper {0} detached on hub port {1} on serial number {2}'.format(self._name, hub_port, serial_number)
                self._logger.info(msg)

        except PhidgetException as e:
            DisplayError(e)
            traceback.print_exc()
            return

    def _on_error_handler(self, ph, error_code, error_string):
        self._logger.error('[Phidget Error Event] -> ' + error_string + ' (' + str(error_code) + ')\n')
