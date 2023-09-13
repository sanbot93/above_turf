from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.db import models as gis_models


# Create your models here.
class GolfCourseManager(models.Manager):
    def to_list(self):
        return [golfcourse.json() for golfcourse in self.get_queryset()]


class GolfCourse(gis_models.Model):
    name = models.CharField(verbose_name="Course Name")
    address = models.CharField(verbose_name="Address")
    email = models.CharField(verbose_name="Email")
    website = models.CharField(verbose_name="Website")
    description = models.CharField(verbose_name="Description")
    par = models.IntegerField(verbose_name="Par")
    rating = models.IntegerField(verbose_name="Rating")
    spatial_extent = gis_models.PolygonField(null=True, verbose_name="Extent")

    objects = GolfCourseManager()

    def __str__(self):
        return str(self.name)

    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "address": self.address,
            "email": self.email,
            "website": self.website,
            "description": self.description,
            "par": self.par,
            "rating": self.rating,
            "spatial_extent": self.spatial_extent,
        }


class CustomUser(AbstractUser):
    pass
    # add additional fields in here
    first_name = models.CharField(verbose_name="First Name")
    last_name = models.CharField(verbose_name="Last Name")
    golf_role = models.CharField(verbose_name="Role")
    created_date = models.DateTimeField(auto_now_add=True)
    golf_course = models.ForeignKey(GolfCourse, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.username


class Hole(gis_models.Model):
    course_id = models.ForeignKey(GolfCourse, on_delete=models.CASCADE, null=True)
    hole_number = models.IntegerField(verbose_name="Hole Number")
    par = models.IntegerField(verbose_name="Par")
    current_sponsor = models.CharField(verbose_name="Sponsor")
    red_distance = models.IntegerField(verbose_name="Red Distance")
    white_distance = models.IntegerField(verbose_name="White Distance")
    blue_distance = models.IntegerField(verbose_name="Blue Distance")
    gold_distance = models.IntegerField(verbose_name="Gold Distance")
    spatial_extent = gis_models.PolygonField()

    def __str__(self):
        return str(self.hole_number)


groundcover = (("TEE", "Tee Box"), ("FAIR", "Fairway"), ("ROUGH", "Rough"), ("GREEN", "Green"), ("TREES", "Trees"))


class GroundCover(gis_models.Model):
    golf_course = models.ForeignKey(GolfCourse, on_delete=models.CASCADE, null=True)
    hole_id = models.ForeignKey(Hole, on_delete=models.PROTECT)
    turf_type = models.CharField(choices=groundcover, verbose_name="Ground Type")
    spatial_extent = gis_models.PolygonField(verbose_name="Spatial Extent")

    def __str__(self):
        return str(self.turf_type)


treatment_types = (("CHEMICAL", "Chemical"), ("NUTRIENT", "Nutrient"), ("WEED", "Weed"), ("INSECTICIDE", "Insecticide"), ("SEEDING", "Seeding"))


class CourseTreatment(gis_models.Model):
    treatment_name = models.CharField(verbose_name="Treatment Title")
    course_id = models.ForeignKey(GolfCourse, null=True, related_name="course_treatments", on_delete=models.CASCADE)
    hole_id = models.ForeignKey(Hole, null=True, related_name="holes_treatments", on_delete=models.PROTECT)
    groundcover_id = models.ForeignKey(GroundCover, null=True, related_name="groundcover_treatments", on_delete=models.PROTECT)
    start_date = models.DateField(verbose_name="Treatment Start Date")
    end_date = models.DateField(verbose_name="Treatment End Date")
    description = models.CharField(verbose_name="Treatment Description")
    treatment_type = models.CharField(choices=treatment_types, verbose_name="Treatment Type")
    spatial_extent = gis_models.PolygonField(verbose_name="Treatment Extent")
    a = models.Choices

    def __str__(self):
        return str(self.treatment_name)


class Statistic(gis_models.Model):
    total_count = models.IntegerField()


data_types = (("RGB", "Regular Color"), ("MS", "Multispectral"))


class Flight(gis_models.Model):
    course_id = models.ForeignKey(GolfCourse, on_delete=models.PROTECT, null=True)
    data_type = models.CharField(choices=data_types, verbose_name="Data Type")
    mission_date = models.DateTimeField(verbose_name="Flight Date")
    processed = models.BooleanField(verbose_name="Processed Complete", default=False)
    odm_task_id = models.CharField(verbose_name="WebODM Task ID")

    def __str__(self):
        return str(self.odm_task_id)


class Service(models.Model):
    service_name = models.CharField(verbose_name="Service Name")
    description = models.CharField(verbose_name="Description")
    price = models.IntegerField(verbose_name="Price")
    duration = models.IntegerField(verbose_name="Duration")
    availability = models.BooleanField(verbose_name="Service Available")

    def __str__(self):
        return str(self.service_name)


class Raster(gis_models.Model):
    course_id = models.ForeignKey(GolfCourse, null=True, related_name="course", on_delete=models.PROTECT)
    flight_id = models.ForeignKey(Flight, null=True, related_name="flights", on_delete=models.PROTECT)
    raster_data = gis_models.RasterField()

    def __str__(self):
        return str(self)
