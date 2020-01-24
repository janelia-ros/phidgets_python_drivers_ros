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

import Phidget22
from Phidget22.PhidgetException import *

class PhidgetInfo():
    def __init__(self):
        self.serial_number = Phidget22.Phidget.Phidget.ANY_SERIAL_NUMBER
        self.label = Phidget22.Phidget.Phidget.ANY_LABEL
        self.channel = Phidget22.Phidget.Phidget.ANY_CHANNEL
        self.hub_port = Phidget22.Phidget.Phidget.ANY_HUB_PORT
        self.is_hub_port_device = False
        self.timeout = Phidget22.Phidget.Phidget.DEFAULT_TIMEOUT

class Phidget:
    def __init__(self, phidget_info, name, logger):
        self.phidget_info = phidget_info
        self.name = name
        self.logger = logger

        self._setup_phidget()

    def _setup_phidget(self):
        self._handle = None

    def is_handle(self, handle):
        return self._handle == handle

    def get_handle(self):
        return self._handle

    def open_wait_for_attachment(self, handle):
        if handle is None:
            return

        handle.setDeviceSerialNumber(self.phidget_info.serial_number)
        if self.phidget_info.label:
            handle.setDeviceLabel(self.phidget_info.label)
        handle.setChannel(self.phidget_info.channel)
        handle.setHubPort(self.phidget_info.hub_port)
        handle.setIsHubPortDevice(self.phidget_info.is_hub_port_device)

        handle.openWaitForAttachment(self.phidget_info.timeout)

        self.phidget_info.serial_number = handle.getDeviceSerialNumber()
        self.phidget_info.label = handle.getDeviceLabel()
        self.phidget_info.channel = handle.getChannel()
        self.phidget_info.hub_port = handle.getHubPort()
        self.phidget_info.is_hub_port_device = handle.getIsHubPortDevice()

        if self.phidget_info.label:
            msg = '{0} -> label: {1.label}, hub_port: {1.hub_port}'
        else:
            msg = '{0} -> serial_number: {1.serial_number}, hub_port: {1.hub_port}'
        msg = msg.format(self.name, self.phidget_info)
        self.logger.info(msg)

    def close(self, handle):
        if handle is not None:
            handle.close()

    # def on_attach_handler(self, handle):
    def set_on_attach_handler(self, handle, on_attach_handler):
        if handle is not None:
            handle.setOnAttachHandler(on_attach_handler)

    # def on_detach_handler(self, handle):
    def set_on_detach_handler(self, handle, on_detach_handler):
        if handle is not None:
            handle.setOnDetachHandler(on_detach_handler)

    # def on_error_handler(self, handle, code, description):
    def set_on_error_handler(self, handle, on_error_handler):
        if handle is not None:
            handle.setOnErrorHandler(on_error_handler)
