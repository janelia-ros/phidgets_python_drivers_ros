# Copyright (c) 2020, Howard Hughes Medical Institute
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from Phidget22.PhidgetException import *
from phidgets_python_api.phidget import PhidgetComposite
from phidgets_python_api.digital_output import DigitalOutput, DigitalOutputInfo

class LedHubInfo():
    def __init__(self):
        self.led_count = 6
        self.leds_info = []
        for i in range(self.led_count):
            led_info = DigitalOutputInfo()
            led_info.phidget_info.label = 'led_hub'
            self.leds_info.append(led_info)

class LedHub(PhidgetComposite):
    def __init__(self, name, logger, led_hub_info):
        super().__init__(name, logger)
        self.led_hub_info = led_hub_info

        self.leds = []
        for i in range(self.led_hub_info.led_count):
            led_name = self.name + '_' + str(i)
            led = DigitalOutput(led_name, self.logger, self.led_hub_info.leds_info[i])
            self.add(led)
            self.leds.append(led)

    def turn_on_led(self, led_index):
        self.leds[led_index].activate()

    def turn_off_led(self, led_index):
        self.leds[led_index].deactivate()
