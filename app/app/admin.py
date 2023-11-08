from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from app.models import *

User = get_user_model()

admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Item)
admin.site.register(Product)
admin.site.register(Stock)

admin.site.site_header = 'Administração HubMecanico'