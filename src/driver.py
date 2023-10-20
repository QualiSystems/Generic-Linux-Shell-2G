#!/usr/bin/python
# -*- coding: utf-8 -*-
from _package.autoload.linux_resource import LinuxResourceModel
from _package.cli.cli_configurator import GenericLinuxCliConfigurator
from _package.resource_model import LinuxResourceConfig
from cloudshell.cli.service.cli import CLI
from cloudshell.cli.service.session_pool_manager import SessionPoolManager
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.shell.flows.command.basic_flow import RunCommandFlow
from cloudshell.shell.standards.resource_config_generic_models import GenericCLIConfig


class GenericLinuxOSShellDriver(
    ResourceDriverInterface):
    SHELL_NAME = "Generic Linux OS Shell 2G"

    def __init__(self):
        self._cli = None

    def initialize(self, context):
        """Initialize method.

        :type context: cloudshell.shell.core.context.driver_context.InitCommandContext
        """
        api = CloudShellSessionContext(context).get_api()
        resource_config = LinuxResourceConfig.from_context(context, api)
        session_pool_size = int(resource_config.sessions_concurrency_limit or 1)
        self._cli = CLI(
            SessionPoolManager(max_pool_size=session_pool_size, pool_timeout=100)
        )
        return "Finished initializing"

    @GlobalLock.lock
    def get_inventory(self, context):
        """Return device structure with all standard attributes.

        :param ResourceCommandContext context: ResourceCommandContext object with all
            Resource Attributes inside
        :return: response
        :rtype: str
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = GenericCLIConfig.from_context(
                context, api
            )
            resource_model = LinuxResourceModel.from_resource_config(
                resource_config
            )
            # resource_model.connect_port(resource_model.entities.Port(index="0"))
            logger.info("Autoload started")
            response = resource_model.build()
            logger.info("Autoload completed")
            return response

    def run_custom_command(self, context, custom_command):
        """Send custom command.

        :param ResourceCommandContext context: ResourceCommandContext object with all
            Resource Attributes inside
        :return: result
        :rtype: str
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LinuxResourceConfig.from_context(
                context,
                api,
            )
            cli_configurator = GenericLinuxCliConfigurator.from_config(resource_config, logger, self._cli)

            run_command_flow = RunCommandFlow(cli_configurator)
            run_command_flow.logger = logger
            response = run_command_flow.run_custom_command(custom_command)
            return response

    def run_custom_config_command(self, context, custom_command):
        """Send custom command in configuration mode.

        :param ResourceCommandContext context: ResourceCommandContext object with all
            Resource Attributes inside
        :return: result
        :rtype: str
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LinuxResourceConfig.from_context(
                context,
                api,
            )
            cli_configurator = GenericLinuxCliConfigurator.from_config(resource_config, logger, self._cli)

            run_command_flow = RunCommandFlow(cli_configurator)
            run_command_flow.logger = logger

            result_str = run_command_flow.run_custom_config_command(
                custom_command
            )
            return result_str

    def health_check(self, context):
        """Performs device health check.

        :param ResourceCommandContext context: ResourceCommandContext object with all
            Resource Attributes inside
        :return: Success or Error message
        :rtype: str
        """
        self.run_custom_command(context, "")
        return "Ok"

    def cleanup(self):
        pass

    def shutdown(self, context):
        self.run_custom_config_command(context, "shutdown -h now")
        return "Ok"
