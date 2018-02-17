from palantir.configuration_manager import ConfigurationManager


class TestConfigurationManager:

    def test_basic(self, configuration_manager):
        assert isinstance(configuration_manager, ConfigurationManager)
        assert isinstance(configuration_manager._storage, dict)

    def test_get_existing_attribute(self, configuration_manager):
        assert isinstance(configuration_manager['description'], dict)
        assert configuration_manager['defaults']['well']['choke'] == 100

    def test_get_missing_attribute_returns_none(self, configuration_manager):
        assert configuration_manager['missing attribute'] == None
