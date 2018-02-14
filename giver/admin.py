from django.contrib import admin

from .models import Charge, Status, Aide, Shift, PrimaryCaregiver, Email

admin.site.register(Email)
admin.site.register(Charge)
admin.site.register(Status)
admin.site.register(Aide)
admin.site.register(Shift)
admin.site.register(PrimaryCaregiver)
