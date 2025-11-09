from django.contrib import admin
from .models import FishermanProfile, DailyCatch, Complaint

admin.site.register(FishermanProfile)
admin.site.register(DailyCatch)
admin.site.register(Complaint)
