"""
Lutes is a micro entity-component-system module.

It defines base classes to work with: Manager and System.
As entities should not contain any data, they are just mere identifiers.
"""


class Component:
    """A component is a data bag attached to an entity"""

    def __init__(self, entity=None):
        self.entity = entity
        """Entity the component relates to"""


class System:
    """A system handles a set of components.
    It is responsible for updating them.
    """

    def __init__(self, priority=99):
        self.priority = priority
        """System priority, lower is updated first"""
        self.manager = None
        self.entities = []
        """Entities handled by the system"""
        self.handled_components = []
        """Components the system needs to update entites"""

    def update(self, delta):
        """Update entities"""
        pass

    def init(self):
        """Initialize the system"""
        pass


class Manager:
    """Manager handles entities and their components."""

    def __init__(self):
        self._index = 0
        self._components = {}
        self._entities = []
        self._systems = []
        self._subscribers = {}

    def create_entity(self):
        """Create an entity in the world and return its identifier."""
        index = self._index
        self._entities.append(index)
        self._index += 1
        return index

    def remove_entity(self, entity):
        """Remove an entity from the world"""
        self._entities.remove(entity)
        for system in self._systems:
            if entity in system.entities:
                system.entities.remove(entity)
        for component_type in self._components:
            if entity in self._components[component_type]:
                # Related components should be orphans
                self._components[component_type][entity].entity = None
                del self._components[component_type][entity]

    def add_component(self, entity, component):
        """Add a component to an entity"""
        component.entity = entity
        if type(component) in self._components:
            if entity in self._components[type(component)]:
                # Old component is now orphan
                self._components[type(component)][entity].entity = None
            self._components[type(component)][entity] = component
        else:
            self._components[type(component)] = {entity: component}
        self._subscribe_entity(entity)

    def remove_component(self, entity, component):
        """Remove a component from an entity"""
        component.entity = None
        del self._components[component][entity]
        self._subscribe_entity(entity)

    def get_component(self, entity, component):
        return self._components[component][entity]

    def add_system(self, system):
        """Add system to the world"""
        self._systems.append(system)
        system.manager = self
        self._systems.sort(key=lambda x: x.priority)

    def dispatch_event(self, event, data):
        if event in self._subscribers:
            for callback in self._subscribers[event]:
                callback(data)

    def subscribe(self, event, callback):
        """Subscribe a callback to an event"""
        if event in self._subscribers:
            self._subscribers[event].append(callback)
        else:
            self._subscribers[event] = [callback]

    def remove_system(self, system):
        """Remove a system from the world"""
        self._systems.remove(system)

    def update(self, delta):
        """Update every system"""
        for system in self._systems:
            system.update(delta)

    def init(self):
        """Initialize systems"""
        for entity in self._entities:
            self._subscribe_entity(entity)
        for system in self._systems:
            system.init()

    def _subscribe_entity(self, entity):
        """Check if entity needs to be removed or added to a system"""
        for system in self._systems:
            if system.handled_components:
                try:
                    for component in system.handled_components:
                        self.get_component(entity, component)
                    if entity not in system.entities:
                        system.entities.append(entity)
                except KeyError:
                    if entity in system.entities:
                        system.entities.remove(entity)
