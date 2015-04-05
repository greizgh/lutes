from lutes import Manager, System, Component, InvalidEntityError
import pytest


class DummySystem(System):
    def __init__(self):
        super().__init__()
        self.handled_components = [Component]


class UpdateSystem(System):
    def __init__(self):
        super().__init__()
        self.updated = False

    def update(self, delta):
        self.updated = True


class TestManager:
    def test_entity_creation(self):
        manager = Manager()
        entity = manager.create_entity()
        assert entity == 0

    def test_component_association(self):
        manager = Manager()
        entity = manager.create_entity()
        component1 = Component()
        component2 = Component()
        manager.add_component(entity, component1)
        assert component1.entity == entity
        assert manager.get_component(entity, Component) == component1
        manager.add_component(entity, component2)
        assert component1.entity is None
        assert component2.entity == entity
        assert manager.get_component(entity, Component) == component2

    def test_get_inexistant_component(self):
        manager = Manager()
        entity = manager.create_entity()
        assert manager.get_component(entity, Component) is None

    def test_get_inexistant_entity(self):
        manager = Manager()
        with pytest.raises(InvalidEntityError):
            manager.get_component(12, Component)

    def test_event_dispatching(self):
        manager = Manager()
        data = ['test', True]

        def _callback(event_data):
            assert data == event_data

        manager.subscribe('test', _callback)
        manager.subscribe('test', _callback)
        manager.dispatch_event('test', data)

    def test_init(self):
        manager = Manager()
        system = DummySystem()
        manager.add_system(system)
        entity1 = manager.create_entity()
        manager.add_component(entity1, Component())
        manager.create_entity()
        manager.init()
        assert system.entities == [entity1]

    def test_component_removal(self):
        manager = Manager()
        system = DummySystem()
        manager.add_system(system)
        entity = manager.create_entity()
        manager.add_component(entity, Component())
        manager.init()
        assert entity in system.entities
        manager.remove_component(entity, Component)
        manager.init()
        assert entity not in system.entities

    def test_entity_removal(self):
        manager = Manager()
        system = DummySystem()
        entity = manager.create_entity()
        manager.add_system(system)
        manager.add_component(entity, Component())
        manager.init()
        assert entity in system.entities
        manager.remove_entity(entity)
        assert entity not in system.entities

    def test_update(self):
        manager = Manager()
        system1 = UpdateSystem()
        system2 = UpdateSystem()
        system3 = DummySystem()
        manager.add_system(system1)
        manager.add_system(system2)
        manager.add_system(system3)
        manager.update(0.01)
        assert system1.updated
        assert system2.updated
