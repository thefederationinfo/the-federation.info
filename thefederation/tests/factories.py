import factory
from django.utils.timezone import utc

from thefederation.models import Node, Platform, Protocol


class PlatformFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = Platform


class ProtocolFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = Protocol


class NodeFactory(factory.DjangoModelFactory):
    host = factory.Sequence(lambda n: 'node%s.local' % n)
    name = factory.Faker('company')
    open_signups = factory.Faker('pybool')
    platform = factory.SubFactory(PlatformFactory)

    class Meta:
        model = Node

    class Params:
        active = factory.Trait(
            last_success = factory.Faker('past_datetime', start_date='-1d', tzinfo=utc),
        )

    @factory.post_generation
    def protocols(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.protocols.add(extracted)
            return

        self.protocols.add(ProtocolFactory())
