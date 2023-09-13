# Generated by Django 4.2.5 on 2023-09-13 01:49

import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_type', models.CharField(choices=[('RGB', 'Regular Color'), ('MS', 'Multispectral')], verbose_name='Data Type')),
                ('mission_date', models.DateTimeField(verbose_name='Flight Date')),
                ('processed', models.BooleanField(default=False, verbose_name='Processed Complete')),
                ('odm_task_id', models.CharField(verbose_name='WebODM Task ID')),
            ],
        ),
        migrations.CreateModel(
            name='GolfCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Course Name')),
                ('address', models.CharField(verbose_name='Address')),
                ('email', models.CharField(verbose_name='Email')),
                ('website', models.CharField(verbose_name='Website')),
                ('description', models.CharField(verbose_name='Description')),
                ('par', models.IntegerField(verbose_name='Par')),
                ('rating', models.IntegerField(verbose_name='Rating')),
                ('spatial_extent', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326, verbose_name='Extent')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(verbose_name='Service Name')),
                ('description', models.CharField(verbose_name='Description')),
                ('price', models.IntegerField(verbose_name='Price')),
                ('duration', models.IntegerField(verbose_name='Duration')),
                ('availability', models.BooleanField(verbose_name='Service Available')),
            ],
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Raster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raster_data', django.contrib.gis.db.models.fields.RasterField(srid=4326)),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='course', to='turf.golfcourse')),
                ('flight_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='flights', to='turf.flight')),
            ],
        ),
        migrations.CreateModel(
            name='Hole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hole_number', models.IntegerField(verbose_name='Hole Number')),
                ('par', models.IntegerField(verbose_name='Par')),
                ('current_sponsor', models.CharField(verbose_name='Sponsor')),
                ('red_distance', models.IntegerField(verbose_name='Red Distance')),
                ('white_distance', models.IntegerField(verbose_name='White Distance')),
                ('blue_distance', models.IntegerField(verbose_name='Blue Distance')),
                ('gold_distance', models.IntegerField(verbose_name='Gold Distance')),
                ('spatial_extent', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='turf.golfcourse')),
            ],
        ),
        migrations.CreateModel(
            name='GroundCover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turf_type', models.CharField(choices=[('TEE', 'Tee Box'), ('FAIR', 'Fairway'), ('ROUGH', 'Rough'), ('GREEN', 'Green'), ('TREES', 'Trees')], verbose_name='Ground Type')),
                ('spatial_extent', django.contrib.gis.db.models.fields.PolygonField(srid=4326, verbose_name='Spatial Extent')),
                ('golf_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='turf.golfcourse')),
                ('hole_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='turf.hole')),
            ],
        ),
        migrations.AddField(
            model_name='flight',
            name='course_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='turf.golfcourse'),
        ),
        migrations.CreateModel(
            name='CourseTreatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment_name', models.CharField(verbose_name='Treatment Title')),
                ('start_date', models.DateField(verbose_name='Treatment Start Date')),
                ('end_date', models.DateField(verbose_name='Treatment End Date')),
                ('description', models.CharField(verbose_name='Treatment Description')),
                ('treatment_type', models.CharField(choices=[('CHEMICAL', 'Chemical'), ('NUTRIENT', 'Nutrient'), ('WEED', 'Weed'), ('INSECTICIDE', 'Insecticide'), ('SEEDING', 'Seeding')], verbose_name='Treatment Type')),
                ('spatial_extent', django.contrib.gis.db.models.fields.PolygonField(srid=4326, verbose_name='Treatment Extent')),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_treatments', to='turf.golfcourse')),
                ('groundcover_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='groundcover_treatments', to='turf.groundcover')),
                ('hole_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='holes_treatments', to='turf.hole')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(verbose_name='First Name')),
                ('last_name', models.CharField(verbose_name='Last Name')),
                ('golf_role', models.CharField(verbose_name='Role')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('golf_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='turf.golfcourse')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]