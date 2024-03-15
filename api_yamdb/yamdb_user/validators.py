import re

from django.core.exceptions import ValidationError


class BaseUserValidator:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Username cannot be "me"')
        if banned_symbols := re.sub(r'[\w.@+-]+', '', value):
            raise ValidationError(
                'Prohibited username symbols: "{'
                + '}, {'.join(banned_symbols)
                + '}"'
            )
        return value
