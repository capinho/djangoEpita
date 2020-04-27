import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r'^[a-zA-Z]+\/(...)\/(....)'
    message = _(
        'Entrez un nom d\'utilisateur valide. Cette valeur peut contenir uniquement des lettres, '
        'nombres, et @/./+/-/_ characteres.'
    )
    flags = re.ASCII
