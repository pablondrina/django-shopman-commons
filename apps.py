"""Django AppConfig for shopman_commons.

Adding 'shopman_commons' to INSTALLED_APPS enables Django's static file
finders to locate the bundled JavaScript (autocomplete_autofill.js, etc.).

No models or migrations — this is a utility-only app.
"""

from django.apps import AppConfig


class ShopmanCommonsConfig(AppConfig):
    name = "shopman_commons"
    label = "shopman_commons"
    verbose_name = "Shopman Commons"
    default_auto_field = "django.db.models.BigAutoField"
