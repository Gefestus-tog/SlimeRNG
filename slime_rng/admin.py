from django.apps import apps
from django.contrib import admin
from .models import CollectionRequirement

# Register your models here.
models = apps.get_app_config('slime_rng').get_models()

# Register Models in the Admin
for model in models:
    if model.__name__ != 'CollectionRequirement':
        admin.site.register(model)

class CollectionRequirementAdmin(admin.ModelAdmin):
    list_filter = ('slime_type',)
    list_display = ('collection', 'slime_type', 'amount')
    ordering = ('collection__name', 'slime_type__name')

admin.site.register(CollectionRequirement, CollectionRequirementAdmin)
