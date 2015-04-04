from lutes import Manager, System


class TestSystem:
    def test_system_add(self):
        manager = Manager()
        system = System()
        manager.add_system(system)
        assert system.manager == manager

    def test_system_add_remove(self):
        manager = Manager()
        system1 = System(1)
        system2 = System(2)
        system3 = System(3)
        manager.add_system(system2)
        manager.add_system(system1)
        manager.add_system(system3)
        assert manager._systems == [system1, system2, system3]
        manager.remove_system(system2)
        assert manager._systems == [system1, system3]
