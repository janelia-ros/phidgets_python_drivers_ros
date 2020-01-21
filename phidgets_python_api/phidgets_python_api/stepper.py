from Phidget22.PhidgetException import *
import Phidget22.Devices.Stepper

import .PhidgetHelperFunctions

from phidget_python_api.phidget import Phidget, ChannelInfo

class StepperInfo():
    def __init__(self):
        self.channel_info = ChannelInfo()
        self.data_interval = 100
        self.rescale_factor = 1.0
        self.acceleration = 10000
        self.velocity_limit = 0000
        self.home_velocity_limit = 1000
        self.home_target_position = -10000
        self.current_limit = 0.1
        self.holding_current_limit = 0.0
        self.invert_direction = False

class Stepper(Phidget):
    def __init__(self, stepper_info):
        super().__init__(stepper_info.channel_info)
        self._stepper_info = stepper_info

        try:
            self._handle = Phidget22.Devices.Stepper()
        except PhidgetException as e:
            DisplayError(e)
            raise

        open_wait_for_attachment(self._handle)
        self._setup()

    def _setup(self):
        self.set_data_interval(self._stepper_info.data_interval)
        self.set_rescale_factor(self._stepper_info.rescale_factor)
        self.set_acceleration(self._stepper_info.acceleration)
        self.set_current_limit(self._stepper_info.current_limit)
        self.set_holding_current_limit(self._stepper_info.holding_current_limit)
        self.set_velocity_limit(self._stepper_info.velocity_limit)
        if not stepper_info.invert_direction:
            self._direction = 1
        else:
            self._direction = -1

        self.enable()

    def close(self):
        self.set_on_position_change_handler(None)
        self.set_on_velocity_change_handler(None)
        self.set_on_stopped_handler(None)
        super().close(self._handle)

    # void onPositionChange(self, position)
    def set_on_position_change_handler(self, on_position_change_handler):
        self._handle.setOnPositionChangeHandler(on_position_change_handler)

    # void onVelocityChange(self, velocity)
    def set_on_velocity_change_handler(self, on_velocity_change_handler):
        self._handle.setOnVelocityChangeHandler(on_velocity_change_handler)

    # void onStopped(self)
    def set_on_stopped_handler(self, on_stopped_handler):
        self._handle.setOnStoppedHandler(on_stopped_handler)

    def get_acceleration(self):
        return self._handle.getAcceleration()

    def set_acceleration(self, acceleration):
        self._handle.setAcceleration(acceleration)

    def get_min_acceleration(self):
        return self._handle.getMinAcceleration()

    def get_max_acceleration(self):
        return self._handle.getMaxAcceleration()

    def step_control_mode(self):
        return self._handle.getControlMode() == StepperControlMode.CONTROL_MODE_STEP

    def set_step_control_mode(self):
        self._handle.setControlMode(StepperControlMode.CONTROL_MODE_STEP)

    def get_current_limit(self):
        return self._handle.getCurrentLimit()

    def set_current_limit(self, current_limit):
        self._handle.setCurrentLimit(current_limit)

    def get_min_current_limit(self):
        return self._handle.getMinCurrentLimit()

    def get_max_current_limit(self):
        return self._handle.getMinCurrentLimit()

    def get_data_interval(self):
        return self._handle.getDataInterval()

    def set_data_interval(self, data_interval):
        self._handle.setDataInterval(data_interval)

    def get_min_data_interval(self):
        return self._handle.getMinDataInterval()

    def get_max_data_interval(self):
        return self._handle.getMaxDataInterval()

    def enable(self):
        self._handle.setEngaged(True)

    def disable(self):
        self._handle.setEngaged(False)

    def enabled(self):
        return self._handle.getEngaged()

    def get_holding_current_limit(self):
        return self._handle.getHoldingCurrentLimit()

    def set_holding_current_limit(self, holding_current_limit):
        self._handle.setHoldingCurrentLimit(holding_current_limit)

    def get_is_moving(self):
        return self._handle.getIsMoving()

    def get_position(self):
        return self._direction * self._handle.getPosition()

    def add_position_offset(self, position_offset):
        self._handle.addPositionOffset(position_offset)

    def get_rescale_factor(self):
        return self._handle.getRescaleFactor()

    def set_rescale_factor(self, rescale_factor):
        self._handle.setRescaleFactor(rescale_factor)

    def get_target_position(self):
        return self._direction * self._handle.getTargetPosition()

    def set_target_position(self, target_position):
        self._handle.setTargetPosition(self._direction * target_position)

    def get_velocity(self):
        return self._handle.getVelocity()

    def set_velocity_limit(self, velocity_limit):
        self._handle.setVelocityLimit(velocity_limit)

    def get_min_velocity_limit(self):
        return self._handle.getMinVelocityLimit()

    def get_max_velocity_limit(self):
        return self._handle.getMaxVelocityLimit()
