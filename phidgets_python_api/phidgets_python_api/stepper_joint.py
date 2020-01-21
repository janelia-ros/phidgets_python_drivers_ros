from phidget_python_api.stepper import Stepper, StepperInfo
from phidget_python_api.digital_input import DigitalInput, DigitalInputInfo

class StepperJointInfo():
    def __init__(self):
        self.stepper_info = StepperInfo()
        self.digital_input_info = DigitalInputInfo()
        self.home_velocity_limit = 1000
        self.home_target_position = -10000

class StepperJoint:
    def __init__(self, stepper_joint_info):
        self.stepper = Stepper(stepper_joint_info.stepper_info)
        self.digital_input = DigitalInput(stepper_joint_info.digital_input_info)
        self._stepper_joint_info = stepper_joint_info

    def home(self):
        if self.digital_input.getState():
            self.stepper.set_velocity_limit(self._stepper_joint_info.home_velocity_limit)
            self.stepper.set_target_position(self._stepper_joint_info.home_target_position)
            while self.digital_input.getState():
                pass
            self.stepper.set_velocity_limit(0.0)
            self.stepper.add_position_offset(-self.stepper.get_position())
            self.stepper.set_target_position(0.0)
            self.stepper.set_velocity_limit(self._stepper_joint_info.stepper_info.velocity_limit)

    def close(self):
        self.stepper.close()
        self.digital_input.close()
