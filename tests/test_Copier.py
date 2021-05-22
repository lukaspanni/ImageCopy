from ImageCopy.config import Config
from ImageCopy.copier import Copier


class TestCopier:

    class TestConfig(Config):
        def __init__(self, config_path):
            try:
                super().__init__(config_path)
            except Exception:
                pass

    def test_constructor_config_default(self):
        config_dict = {"copy": {"mode": "invalid"}}
        config = TestCopier.TestConfig(None)
        config._cfg = config_dict

        copier = Copier(config)
        assert copier.mode == Copier.OverwriteOptions.OVERWRITE

    def test_constructor_config(self):
        config_dict = {"copy": {"mode": "warn-before-overwrite"}}
        config = TestCopier.TestConfig(None)
        config._cfg = config_dict

        copier = Copier(config)
        assert copier.mode == Copier.OverwriteOptions.WARN