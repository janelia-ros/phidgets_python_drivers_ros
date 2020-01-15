from Phidget22.Phidget import *
from Phidget22.PhidgetException import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.DigitalInput import *

from .PhidgetHelperFunctions import *

class Joint:
    ACCELERATION = 100000
    VELOCITY_LIMIT = 20000
    HOME_VELOCITY_LIMIT = 1000
    HOME_TARGET_POSITION = -10000
    CURRENT_LIMIT = 0.3
    HOLDING_CURRENT_LIMIT = 0.5
    ATTACHMENT_TIMEOUT = 5000

    def __init__(self, stepper_channel_info, home_switch_channel_info, name):
        self.name = name
        try:
            self._stepper = Stepper()
            self._home_switch = DigitalInput()
        except PhidgetException as e:
            DisplayError(e)
            raise
        self._logger = None
        self._setup_channel(self._stepper, stepper_channel_info)
        self._setup_channel(self._home_switch, home_switch_channel_info)

    def set_logger(self, logger):
        self._logger = logger

    def set_publish_joint_state(self, publish_joint_state):
        self._publish_joint_state = publish_joint_state
        self._stepper.setOnPositionChangeHandler(publish_joint_state)
        self._stepper.setOnVelocityChangeHandler(publish_joint_state)

    def _on_attach_handler(self, ph):
        try:
            channel_class_name = ph.getChannelClassName()
            serial_number = ph.getDeviceSerialNumber()
            channel = ph.getChannel()
            hub_port = ph.getHubPort()
            if ph.getIsHubPortDevice():
                msg = 'home switch {0} attached on hub port {1} on serial number {2}'.format(self.name, hub_port, serial_number)
                self._logger.info(msg)
            else:
                msg = 'stepper {0} attached on hub port {1} on serial number {2}'.format(self.name, hub_port, serial_number)
                self._logger.info(msg)

            try:
                ph.setDataInterval(100)
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
                msg = 'home switch {0} detached on hub port {1} on serial number {2}'.format(self.name, hub_port, serial_number)
                self._logger.info(msg)
            else:
                msg = 'stepper {0} detached on hub port {1} on serial number {2}'.format(self.name, hub_port, serial_number)
                self._logger.info(msg)

        except PhidgetException as e:
            DisplayError(e)
            traceback.print_exc()
            return

    def _on_error_handler(self, ph, error_code, error_string):
        self._logger.error('[Phidget Error Event] -> ' + error_string + ' (' + str(error_code) + ')\n')

    def _setup_channel(self,channel,info):
        channel.setDeviceSerialNumber(info.deviceSerialNumber)
        channel.setHubPort(info.hubPort)
        channel.setIsHubPortDevice(info.isHubPortDevice)
        channel.setChannel(info.channel)

        channel.setOnAttachHandler(self._on_attach_handler)
        channel.setOnDetachHandler(self._on_detach_handler)
        channel.setOnErrorHandler(self._on_error_handler)

    def open_wait_for_attachment(self):
        self._stepper.openWaitForAttachment(self.ATTACHMENT_TIMEOUT)
        self._home_switch.openWaitForAttachment(self.ATTACHMENT_TIMEOUT)
        self._setup()

    def _setup(self):
        self._stepper.setAcceleration(self.ACCELERATION)
        self._stepper.setCurrentLimit(self.CURRENT_LIMIT)
        self._stepper.setVelocityLimit(self.VELOCITY_LIMIT)
        self._stepper.setHoldingCurrentLimit(self.HOLDING_CURRENT_LIMIT)
        self.enable()

    def home(self):
        if self._home_switch.getState():
            self._stepper.setVelocityLimit(self.HOME_VELOCITY_LIMIT)
            self._stepper.setTargetPosition(self.HOME_TARGET_POSITION)
            while self._home_switch.getState():
                pass
            self._stepper.setVelocityLimit(0.0)
            self._stepper.addPositionOffset(-self._stepper.getPosition())
            self._stepper.setTargetPosition(0.0)
            self._publish_joint_state(None,None)
            self._stepper.setVelocityLimit(self.VELOCITY_LIMIT)
        self._logger.info('{0} homed'.format(self.name))

    def close(self):
        self._stepper.setOnPositionChangeHandler(None)
        self._stepper.close()
        self._home_switch.close()

    def get_rescale_factor(self):
            try:
                rescale_factor = self._stepper.getRescaleFactor()
                self._logger.info('rescale_factor: {0}'.format(rescale_factor))
            except PhidgetException as e:
                DisplayError(e)
                return
        # return self._stepper.getRescaleFactor()

    def set_rescale_factor(self, rescale_factor):
        self._stepper.setRescaleFactor(rescale_factor)

    def get_position(self):
        return self._stepper.getPosition()

    def get_velocity(self):
        return self._stepper.getVelocity()

    def enable(self):
        self._stepper.setEngaged(True)

    def disable(self):
        self._stepper.setEngaged(False)

    def set_target_position(self, target_position):
        self._stepper.setTargetPosition(target_position)

    def set_velocity_limit(self, velocity_limit):
        self._stepper.setVelocityLimit(velocity_limit)
