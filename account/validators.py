import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        # Minimum 4 characters
        if len(password) < 4:
            raise ValidationError(_('Password must be at least 4 characters long'))
        
        # Must contain uppercase, lowercase, number, and special character
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter'))
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(_('Password must contain at least one lowercase letter'))
        
        if not re.search(r'\d', password):
            raise ValidationError(_('Password must contain at least one number'))
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_('Password must contain at least one special character'))

    def get_help_text(self):
        return _(
            'Your password must contain at least 4 characters, '
            'including uppercase, lowercase, number, and special character.'
        )

def validate_username(value):
    # Username validation
    if len(value) < 1:
        raise ValidationError(_('Username must be at least 1 characters long'))
    
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError(_('Username can only contain letters, numbers, and underscores'))