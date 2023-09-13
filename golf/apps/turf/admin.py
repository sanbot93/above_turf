from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .models import GolfCourse, Hole, GroundCover, CourseTreatment, Statistic, Flight, Service, Raster


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "first_name", "last_name", "golf_role"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GolfCourse, LeafletGeoAdmin)
admin.site.register(Hole, LeafletGeoAdmin)
admin.site.register(GroundCover, LeafletGeoAdmin)
admin.site.register(CourseTreatment, LeafletGeoAdmin)
admin.site.register(Statistic, LeafletGeoAdmin)
admin.site.register(Flight, LeafletGeoAdmin)
admin.site.register(Service, LeafletGeoAdmin)
admin.site.register(Raster, LeafletGeoAdmin)
