from django.utils.translation import ugettext_lazy as _
from enumfields import Enum


class Relay(Enum):
    ALL = 'all'
    NONE = 'none'
    TAGS = 'tags'

    class Labels:
        ALL = _('All')
        NONE = _('None')
        TAGS = _('Tags')
