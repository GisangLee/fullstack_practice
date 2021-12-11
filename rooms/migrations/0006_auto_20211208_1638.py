# Generated by Django 2.2.5 on 2021-12-08 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20211208_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='rooms.Amenity'),
        ),
        migrations.AlterField(
            model_name='room',
            name='facilities',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='rooms.Facilitiy'),
        ),
        migrations.AlterField(
            model_name='room',
            name='houserules',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='rooms.HouseRule'),
        ),
        migrations.AlterField(
            model_name='room',
            name='roomtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to='rooms.RoomType'),
        ),
    ]