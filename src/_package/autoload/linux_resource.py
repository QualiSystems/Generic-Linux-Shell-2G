from cloudshell.shell.standards.autoload_generic_models import GenericResourceModel, GenericPort, BasePort


class LinuxResourcePort(BasePort):
    _RESOURCE_MODEL = "ResourcePort"

class LinuxResourceModel(GenericResourceModel):
    SUPPORTED_FAMILY_NAMES = ['CS_Resource', 'CS_RealServer']
    @property
    def entities(self):
        class _entities:
            Port = LinuxResourcePort
        return _entities

    def connect_port(self, port: GenericPort) -> None:
        """Connect chassis sub resource."""
        self._add_sub_resource_with_type_restrictions(port, [LinuxResourcePort])