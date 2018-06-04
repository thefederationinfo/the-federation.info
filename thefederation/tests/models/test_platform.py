from test_plus import TestCase

from thefederation.models import Platform
from thefederation.tests.factories import PlatformFactory


class VersionCleanChoicesTestCase(TestCase):
    def test_remove_commit_hash(self):
        platform = PlatformFactory(version_clean_style=Platform.VERSION_CLEAN_REMOVE_COMMIT_HASH)
        self.assertEqual(
            platform.clean_version('Pleroma 0.9.0 dca1d6d16278599485df3a175fb356bdc995441c'),
            'Pleroma 0.9.0',
        )
