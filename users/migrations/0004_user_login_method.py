# Generated by Django 2.2.5 on 2021-12-12 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211212_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('email', 'Email'), ('github', 'Github'), ('kakao', 'Kakao')], default='email', max_length=50),
        ),
    ]
