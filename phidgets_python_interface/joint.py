from Phidget22.Phidget import *
from Phidget22.PhidgetException import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.DigitalInput import *

from .PhidgetHelperFunctions import *

class Joint:
    def __init__(self, name, parameters, logger, publish_joint_state):
        self._name = name
        self._parameters = parameters
        self._set_logger(logger)

        self._stepper_channel_info = ChannelInfo()
        self._stepper_channel_info.deviceSerialNumber = Phidget.ANY_SERIAL_NUMBER
        self._stepper_channel_info.isHubPortDevice = False
        self._stepper_channel_info.channel = 0
        self._stepper_channel_info.isVint = True
        self._stepper_channel_info.netInfo.isRemote = False

        self._home_switch_channel_info = ChannelInfo()
        self._home_switch_channel_info.deviceSerialNumber = Phidget.ANY_SERIAL_NUMBER
        self._home_switch_channel_info.isHubPortDevice = True
        self._home_switch_channel_info.channel = 0
        self._home_switch_channel_info.isVINT = True
        self._home_switch_channel_info.netInfo.isRemote = False

        self._stepper_channel_info.hubPort = parameters['stepper_hub_port']
        self._home_switch_channel_info.hubPort = parameters['switch_hub_port']

        self._disable_inverse_direction()
        try:
            if parameters['invert_direction']:
                self._enable_inverse_direction()
        except KeyError:
            pass

        try:
            self._stepper = Stepper()
            self._home_switch = DigitalInput()
        except PhidgetException as e:
            DisplayError(e)
            raise

        self._setup_channel(self._stepper, self._stepper_channel_info)
        self._setup_channel(self._home_switch, self._home_switch_channel_info)

        self._set_publish_joint_state(publish_joint_state)
        self._open_channels_wait_for_attachment()

    def _set_logger(self, logger):
        self._logger = logger

    def _set_publish_joint_state(self, publish_joint_state):
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
                msg = 'home switch {0} attached on hub port {1} on serial number {2}'.format(self._name, hub_port, serial_number)
                self._logger.info(msg)
            else:
                msg = 'stepper {0} attached on hub port {1} on serial number {2}'.format(self._name, hub_port, serial_number)
                self._logger.info(msg)

            try:
                ph.setDataInterval(self._parameters['data_interval'])
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

    def _setup_channel(self,channel,info):
        channel.setDeviceSerialNumber(info.deviceSerialNumber)
        channel.setHubPort(info.hubPort)
        channel.setIsHubPortDevice(info.isHubPortDevice)
        channel.setChannel(info.channel)

        channel.setOnAttachHandler(self._on_attach_handler)
        channel.setOnDetachHandler(self._on_detach_handler)
        channel.setOnErrorHandler(self._on_error_handler)

    def _open_channels_wait_for_attachment(self):
        self._stepper.openWaitForAttachment(self._parameters['attachment_timeout'])
        self._home_switch.openWaitForAttachment(self._parameters['attachment_timeout'])
        self._setup()

    def _setup(self):
        self.set_rescale_factor(self._parameters['rescale_factor'])
        self.set_acceleration(self._parameters['acceleration'])
        self.set_current_limit(self._parameters['current_limit'])
        self.set_velocity_limit(self._parameters['velocity_limit'])
        self.set_holding_current_limit(self._parameters['holding_current_limit'])
        self.enable()

    def _enable_inverse_direction(self):
        self._direction = -1

    def _disable_inverse_direction(self):
        self._direction = 1

    def home(self):
        if self._home_switch.getState():
            self.set_velocity_limit(self._parameters['home_velocity_limit'])
            self.set_target_position(self._parameters['home_target_position'])
            while self._home_switch.getState():
                pass
            self.set_velocity_limit(0.0)
            self.add_position_offset(-self._stepper.getPosition())
            self.set_target_position(0.0)
            self._publish_joint_state(None,None)
            self.set_velocity_limit(self._parameters['velocity_limit'])
        self._logger.info('{0} homed'.format(self._name))

    def close(self):
        self._stepper.setOnPositionChangeHandler(None)
        self._stepper.close()
        self._home_switch.close()

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
