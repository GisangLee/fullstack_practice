# Generated by Django 2.2.5 on 2021-12-08 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0004_auto_20211208_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('cleanliness', models.DecimalField(decimal_places=1, max_digits=1)),
                ('location', models.DecimalField(decimal_places=1, max_digits=1)),
                ('accuracy', models.DecimalField(decimal_places=1, max_digits=1)),
                ('check_in', models.DecimalField(decimal_places=1, max_digits=1)),
                ('communication', models.DecimalField(decimal_places=1, max_digits=1)),
                ('pricesatisfaction', models.DecimalField(decimal_places=1, max_digits=1)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
