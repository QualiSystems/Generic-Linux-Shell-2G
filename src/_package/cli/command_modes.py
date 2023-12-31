#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from collections import OrderedDict
from typing import TYPE_CHECKING

from cloudshell.cli.service.command_mode import CommandMode

if TYPE_CHECKING:
    from cloudshell.shell.standards.resource_config_generic_models import (
        GenericCLIConfig,
    )


class DefaultCommandMode(CommandMode):
    PROMPT: str = r".+\$\s*$"
    ENTER_COMMAND: str = ""
    EXIT_COMMAND: str = "exit"

    def __init__(self, resource_config: GenericCLIConfig):
        self.resource_config = resource_config
        CommandMode.__init__(
            self,
            DefaultCommandMode.PROMPT,
            DefaultCommandMode.ENTER_COMMAND,
            DefaultCommandMode.EXIT_COMMAND,
            enter_action_map=self.enter_action_map(),
            exit_action_map=self.exit_action_map(),
            enter_error_map=self.enter_error_map(),
            exit_error_map=self.exit_error_map(),
            use_exact_prompt=True,
        )

    def enter_action_map(self) -> OrderedDict:
        return OrderedDict()

    def enter_error_map(self) -> OrderedDict:
        return OrderedDict([(r"[Ee]rror:", "Command error")])

    def exit_action_map(self) -> OrderedDict:
        return OrderedDict()

    def exit_error_map(self) -> OrderedDict:
        return OrderedDict([(r"[Ee]rror:", "Command error")])


class ConfigCommandMode(CommandMode):
    PROMPT: str = r".+\#\s*$"
    ENTER_COMMAND: str = "sudo -i"
    EXIT_COMMAND: str = "exit"

    def __init__(self, resource_config: GenericCLIConfig):
        self.resource_config = resource_config
        CommandMode.__init__(
            self,
            ConfigCommandMode.PROMPT,
            ConfigCommandMode.ENTER_COMMAND,
            ConfigCommandMode.EXIT_COMMAND,
            enter_action_map=self.enter_action_map(),
            exit_action_map=self.exit_action_map(),
            enter_error_map=self.enter_error_map(),
            exit_error_map=self.exit_error_map(),
            use_exact_prompt=True,
        )

    def enter_action_map(self) -> OrderedDict:
        return OrderedDict(
            [
                (
                    r"password for.+\:",
                    lambda session, logger: session.send_line(
                        self.resource_config.enable_password
                        or self.resource_config.password,
                        logger,
                    ),
                )
            ]
        )

    def enter_error_map(self) -> OrderedDict:
        return OrderedDict([(r"[Ee]rror:", "Command error")])

    def exit_action_map(self) -> OrderedDict:
        return OrderedDict()

    def exit_error_map(self) -> OrderedDict:
        return OrderedDict([(r"[Ee]rror:", "Command error")])


CommandMode.RELATIONS_DICT = {DefaultCommandMode: {ConfigCommandMode: {}}}
