from test_plus import TestCase

from thefederation.models import Platform
from thefederation.tests.factories import PlatformFactory


class PlatformTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.hash_platform = PlatformFactory(version_clean_style=Platform.VERSION_CLEAN_REMOVE_COMMIT_HASH)

    def test_clean_version__remove_commit_hash(self):
        self.assertEqual(
            self.hash_platform.clean_version("Pleroma 0.9.0 dca1d6d16278599485df3a175fb356bdc995441c"),
            "Pleroma 0.9.0",
        )
