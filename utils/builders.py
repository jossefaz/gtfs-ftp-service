from registry.data_struct import REGISTRY

def InterfaceBuilder(container, interface_name) :
        if 'LINKED_TO' in container :
            interface_name = interface_name + '_LINK'
        if 'CB' in container :
            interface_name = interface_name + '_CB'
        interface = REGISTRY[interface_name]
        if container is None:
            args = [None] * len(interface._fields)
            return interface(*args)
        if isinstance(container, (list, tuple)):
            return interface(*container)
        elif isinstance(container, dict):
            return interface(**container)
        else:
            raise TypeError( "Cannot create '{}' tuple out of {} ({}).".format(interface.__name__, type(container).__name__, container))
