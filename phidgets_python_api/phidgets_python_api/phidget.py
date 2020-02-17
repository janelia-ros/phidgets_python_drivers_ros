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

from abc import ABC, abstractmethod

class PhidgetInfo():
    def __init__(self):
        self.serial_number = Phidget22.Phidget.Phidget.ANY_SERIAL_NUMBER
        self.label = Phidget22.Phidget.Phidget.ANY_LABEL
        self.channel = Phidget22.Phidget.Phidget.ANY_CHANNEL
        self.hub_port = Phidget22.Phidget.Phidget.ANY_HUB_PORT
        self.is_hub_port_device = False

class PhidgetComponent(ABC):
    def __init__(self, name, logger):
        self.name = name
        self.logger = logger

    @abstractmethod
    def has_handle(self, handle):
        pass

    @abstractmethod
    def set_on_attach_handler(self, on_attach_handler):
        pass

    @abstractmethod
    def _on_attach_handler(self, handle):
        pass

    @abstractmethod
    def is_attached(self):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

class Phidget(PhidgetComponent):
    def __init__(self, name, logger, phidget_info):
        super().__init__(name, logger)
        self.phidget_info = phidget_info

        self.set_handle(None)

    def set_handle(self, phidget_handle):
        self._phidget_handle = phidget_handle

    def has_handle(self, handle):
        return self._phidget_handle == handle

    # def on_attach_handler(self, handle):
    def set_on_attach_handler(self, on_attach_handler):
        if self._phidget_handle is not None:
            self._phidget_handle.setOnAttachHandler(on_attach_handler)

    def _on_attach_handler(self, handle):
        self.phidget_info.serial_number = self._phidget_handle.getDeviceSerialNumber()
        self.phidget_info.label = self._phidget_handle.getDeviceLabel()
        self.phidget_info.channel = self._phidget_handle.getChannel()
        self.phidget_info.hub_port = self._phidget_handle.getHubPort()
        self.phidget_info.is_hub_port_device = self._phidget_handle.getIsHubPortDevice()

        if self.phidget_info.label:
            msg = '{0} -> label: {1.label}, hub_port: {1.hub_port}'
        else:
            msg = '{0} -> serial_number: {1.serial_number}, hub_port: {1.hub_port}'
        msg = msg.format(self.name, self.phidget_info)
        self.logger.info(msg)

    def is_attached(self):
        if self._phidget_handle is None:
            return False
        return self._phidget_handle.getAttached()

    def open(self):
        self._phidget_handle.setDeviceSerialNumber(self.phidget_info.serial_number)
        if self.phidget_info.label:
            self._phidget_handle.setDeviceLabel(self.phidget_info.label)
        self._phidget_handle.setChannel(self.phidget_info.channel)
        self._phidget_handle.setHubPort(self.phidget_info.hub_port)
        self._phidget_handle.setIsHubPortDevice(self.phidget_info.is_hub_port_device)

        self._phidget_handle.open()

    def close(self):
        if self._phidget_handle is not None:
            self._phidget_handle.close()

    # def on_detach_handler(self, handle):
    def set_on_detach_handler(self, on_detach_handler):
        if self._phidget_handle is not None:
            self._phidget_handle.setOnDetachHandler(on_detach_handler)

    # def on_error_handler(self, handle, code, description):
    def set_on_error_handler(self, on_error_handler):
        if self._phidget_handle is not None:
            self._phidget_handle.setOnErrorHandler(on_error_handler)

class PhidgetComposite(PhidgetComponent):
    def __init__(self, name, logger):
        super().__init__(name, logger)

        self._components = []

    def add(self, component):
        self._components.append(component)

    def has_handle(self, handle):
        has_handle = False
        for component in self._components:
            if component.has_handle(handle):
                has_handle = True
                break
        return has_handle

    def set_on_attach_handler(self, on_attach_handler):
        for component in self._components:
            component.set_on_attach_handler(on_attach_handler)

    def _on_attach_handler(self, handle):
        for component in self._components:
            if component.has_handle(handle):
                component._on_attach_handler(handle)
                break

    def is_attached(self):
        is_attached = True
        for component in self._components:
            if not component.is_attached():
                is_attached = False
                break
        return is_attached

    def open(self):
        for component in self._components:
            component.open()

    def close(self):
        for component in self._components:
            component.close()
