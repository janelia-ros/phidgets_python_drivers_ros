from Phidget22.Phidget import *
from Phidget22.PhidgetException import *
import Phidget22.Devices.Stepper

from .PhidgetHelperFunctions import *

class StepperInfo():
    def __init__(self):
        self.channel_info = ChannelInfo()
        self.channel_info.deviceSerialNumber = Phidget.ANY_SERIAL_NUMBER
        self.channel_info.isHubPortDevice = False
        self.channel_info.channel = 0
        self.channel_info.isVint = True
        self.channel_info.netInfo.isRemote = False
        self.attachment_timeout = 5000
        self.data_interval = 100
        self.acceleration = 10000
        self.velocity_limit = 0000
        self.home_velocity_limit = 1000
        self.home_target_position = -10000
        self.current_limit = 0.1
        self.holding_current_limit = 0.0
        self.rescale_factor = 1.0
        self.invert_direction = False

class Stepper:
    def __init__(self, name, stepper_info):
        self._name = name
        self._stepper_info = stepper_info

        if not stepper_info.invert_direction:
            self._disable_inverse_direction()
        else:
            self._enable_inverse_direction()

        try:
            self._stepper = Phidget22.Devices.Stepper()
        except PhidgetException as e:
            DisplayError(e)
            raise

        self._setup_channel(self._stepper, self._stepper_channel_info)

        self._open_channels_wait_for_attachment()

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

    def _setup_channel(self, channel, info):
        channel.setDeviceSerialNumber(info.deviceSerialNumber)
        channel.setHubPort(info.hubPort)
        channel.setIsHubPortDevice(info.isHubPortDevice)
        channel.setChannel(info.channel)

        channel.setOnAttachHandler(self._on_attach_handler)
        channel.setOnDetachHandler(self._on_detach_handler)
        channel.setOnErrorHandler(self._on_error_handler)

    def _open_channels_wait_for_attachment(self):
        self._stepper.openWaitForAttachment(self._stepper_info.attachment_timeout)
        self._setup()

    def _setup(self):
        self.set_rescale_factor(self._stepper_info.rescale_factor)
        self.set_acceleration(self._stepper_info.acceleration)
        self.set_current_limit(self._stepper_info.current_limit)
        self.set_velocity_limit(self._stepper_info.velocity_limit)
        self.set_holding_current_limit(self._stepper_info.holding_current_limit)
        self.enable()

    def _enable_inverse_direction(self):
        self._direction = -1

    def _disable_inverse_direction(self):
        self._direction = 1

    def close(self):
        self._stepper.setOnPositionChangeHandler(None)
        self._stepper.close()

    def get_acceleration(self):
        return self._stepper.getAcceleration()

    def set_acceleration(self, acceleration):
        self._stepper.setAcceleration(acceleration)

    def get_min_acceleration(self):
        return self._stepper.getMinAcceleration()

    def get_max_acceleration(self):
        return self._stepper.getMaxAcceleration()

    def step_control_mode(self):
        return self._stepper.getControlMode() == StepperControlMode.CONTROL_MODE_STEP

    def set_step_control_mode(self):
        self._stepper.setControlMode(StepperControlMode.CONTROL_MODE_STEP)

    def get_current_limit(self):
        return self._stepper.getCurrentLimit()

    def set_current_limit(self, current_limit):
        self._stepper.setCurrentLimit(current_limit)

    def get_holding_current_limit(self):
        return self._stepper.getHoldingCurrentLimit()

    def set_holding_current_limit(self, holding_current_limit):
        self._stepper.setHoldingCurrentLimit(holding_current_limit)

    def get_is_moving(self):
        return self._stepper.getIsMoving()

    def get_position(self):
        return self._direction * self._stepper.getPosition()

    def set_target_position(self, target_position):
        self._stepper.setTargetPosition(self._direction * target_position)

    def add_position_offset(self, position_offset):
        self._stepper.addPositionOffset(position_offset)

    def enable(self):
        self._stepper.setEngaged(True)

    def disable(self):
        self._stepper.setEngaged(False)

    def get_velocity(self):
        return self._stepper.getVelocity()

    def set_velocity_limit(self, velocity_limit):
        self._stepper.setVelocityLimit(velocity_limit)

    def set_rescale_factor(self, rescale_factor):
        self._stepper.setRescaleFactor(rescale_factor)

    def get_rescale_factor(self):
        return self._stepper.getRescaleFactor()
