from __future__ import annotations

from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.types import T_ON_SESSION_START


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
