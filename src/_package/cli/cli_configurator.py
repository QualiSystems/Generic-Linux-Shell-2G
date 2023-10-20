from __future__ import annotations

import logging
from collections.abc import Collection
from typing import TYPE_CHECKING

from attrs import define, field
from typing_extensions import Self

from cloudshell.cli.configurator import AbstractModeConfigurator
from cloudshell.cli.factory.session_factory import (
    SessionFactory,
)
from cloudshell.cli.service.command_mode_helper import CommandModeHelper

from .command_modes import (
    ConfigCommandMode,
    DefaultCommandMode,
)

if TYPE_CHECKING:
    from cloudshell.cli.service.cli import CLI
    from cloudshell.cli.service.command_mode import CommandMode
    from cloudshell.cli.types import T_COMMAND_MODE_RELATIONS, CliConfigProtocol


@define
class GenericLinuxCliConfigurator(AbstractModeConfigurator):

    modes: T_COMMAND_MODE_RELATIONS = field(init=False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.modes = CommandModeHelper.create_command_mode(self._auth)

    @classmethod
    def from_config(
        cls,
        conf: CliConfigProtocol,
        logger: logging.Logger | None = None,
        cli: CLI | None = None,
        registered_sessions: Collection[SessionFactory] | None = None,
    ) -> Self:
        if not logger:
            logger = logging.getLogger(__name__)
        return super().from_config(conf, logger, cli, registered_sessions)

    @property
    def enable_mode(self) -> CommandMode:
        return self.modes.get(DefaultCommandMode)

    @property
    def config_mode(self) -> CommandMode:
        return self.modes.get(ConfigCommandMode)