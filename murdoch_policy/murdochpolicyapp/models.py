from django.db import models
#from .validators import UnicodeUsernameValidator
#from django.utils.translation import gettext as _

# Create your models here.
class User (models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
#    username_validator = UnicodeUsernameValidator()

#    username = models.CharField(
#         _('username'),
#         max_length=150,
#         unique=True,
#         help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#        validators=[username_validator],
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
#     first_name = models.CharField(_('first name'), max_length=150, blank=True)
#     last_name = models.CharField(_('last name'), max_length=150, blank=True)
#     email = models.EmailField(_('email address'), blank=True)
#     password = models.CharField(_('password'), max_length=50, blank=True)
