from test_plus import TestCase

from thefederation.models import Platform
from thefederation.tests.factories import PlatformFactory


class GetMethodTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.platform = PlatformFactory(name='socialhome')
        cls.unknown_platform = PlatformFactory(name='unknown')

    def test_empty_for_unknown_platform(self):
        self.assertIsNone(self.unknown_platform.get_method((0, 9, 0)))

    def test_returns_a_method(self):
        self.assertEqual(self.platform.get_method((0, 6, 0)), 'nodeinfo')
        self.assertEqual(self.platform.get_method((0, 9, 0)), 'nodeinfo2')

    def test_survives_empty_version(self):
        self.assertIsNone(self.platform.get_method(None))


class VersionCleanChoicesTestCase(TestCase):
    def test_remove_commit_hash(self):
        platform = PlatformFactory(version_clean_style=Platform.VERSION_CLEAN_REMOVE_COMMIT_HASH)
        self.assertEqual(
            platform.clean_version('Pleroma 0.9.0 dca1d6d16278599485df3a175fb356bdc995441c'),
            'Pleroma 0.9.0',
        )
