from django.apps import apps
from django.contrib import admin

# Register your models here.
models = apps.get_app_config('slime_rng').get_models()

# Register Models in the Admin
for model in models:
    admin.site.register(model)
