#!/usr/bin/python
# -*- coding: utf-8 -*-
from attr import define

from cloudshell.shell.standards.resource_config_generic_models import (
    GenericCLIConfig,
    GenericConsoleServerConfig,
)

@define(slots=False, str=False)
class LinuxResourceConfig(GenericCLIConfig, GenericConsoleServerConfig):
    pass