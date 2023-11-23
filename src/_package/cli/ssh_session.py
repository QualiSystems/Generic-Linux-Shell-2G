from __future__ import annotations

import os
import re
from logging import Logger

from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.types import (
    T_ACTION_MAP,
    T_ERROR_MAP,
    T_ON_SESSION_START,
    T_TIMEOUT,
)


class LinuxSSHSession(SSHSession):
    READ_TIMEOUT = 60

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int | None = None,
        on_session_start: T_ON_SESSION_START | None = None,
        pkey: str | None = None,
        pkey_passphrase: str | None = None,
        *args,
        **kwargs,
    ):
        kwargs["timeout"] = self.READ_TIMEOUT
        super().__init__(
            host,
            username,
            password,
            port,
            on_session_start,
            pkey,
            pkey_passphrase,
            *args,
            **kwargs,
        )

    def hardware_expect(
        self,
        command: str | None,
        expected_string: str,
        logger: Logger,
        action_map: T_ACTION_MAP | None = None,
        error_map: T_ERROR_MAP | None = None,
        timeout: T_TIMEOUT | None = None,
        retries: int | None = None,
        check_action_loop_detector: bool = True,
        empty_loop_timeout: T_TIMEOUT | None = None,
        remove_command_from_output: bool = True,
        **optional_args,
    ) -> str:
        output = super().hardware_expect(
            command,
            expected_string,
            logger,
            action_map,
            error_map,
            timeout,
            retries,
            check_action_loop_detector,
            empty_loop_timeout,
            remove_command_from_output,
            **optional_args,
        )
        exit_code_out = super().hardware_expect(
            "echo _code_$?_code_",
            expected_string,
            logger,
            {},
            {},
            timeout,
            retries,
            check_action_loop_detector,
            empty_loop_timeout,
            remove_command_from_output,
            **optional_args,
        )
        match = re.match(r".*_code_(\d+)_code_.*", exit_code_out)
        if match:
            exit_code = int(match.group(1))
            if exit_code > 0:
                output += f"{os.linesep}__EXIT_CODE__={exit_code}"
        return output
