from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Member)
admin.site.register(GymClass)
admin.site.register(Enrollment)
admin.site.register(UserProfile)