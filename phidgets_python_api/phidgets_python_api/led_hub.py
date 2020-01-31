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
from phidgets_python_api.digital_output import DigitalOutput, DigitalOutputInfo

class LedHubInfo():
    def __init__(self):
        self.led_count = 6
        self.leds_info = []
        for i in range(self.led_count):
            led_info = DigitalOutputInfo()
            led_info.phidget_info.label = 'led_hub'
            self.leds_info.append(led_info)

class LedHub:
    def __init__(self, led_hub_info, name, logger):
        self.led_hub_info = led_hub_info
        self.name = name
        self.logger = logger

        self.leds = []
        for i in range(self.led_hub_info.led_count):
            led = DigitalOutput(self.led_hub_info.leds_info[i], self.name + '_' + str(i), self.logger)

    def open(self):
        [led.open() for led in self.leds]

    def close(self):
        [led.close() for led in self.leds]

    def has_handle(self, handle):
        for led in self.leds:
            if led.has_handle(handle):
                return True
        return False

    def set_on_attach_handler(self, on_attach_handler):
        [led.set_on_attach_handler(on_attach_handler) for led in self.leds]

    def _on_attach_handler(self, handle):
        [led._on_attach_handler(handle) for led in self.leds if led.has_handle(handle)]

    def is_attached(self):
        for led in self.leds:
            if not led.is_attached():
                return False
        return True

    def turn_on_led(self, led_index):
        self.leds[led_index].activate()

    def turn_off_led(self, led_index):
        self.leds[led_index].deactivate()
