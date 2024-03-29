# Generated by Django 3.0.7 on 2020-09-02 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0002_auto_20200901_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadingdate', models.CharField(max_length=10)),
                ('uploadingtime', models.CharField(max_length=10)),
                ('branch', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=30)),
                ('notesfile', models.FileField(upload_to='')),
                ('filetype', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=215, null=True)),
                ('comments', models.CharField(max_length=254, null=True)),
                ('marks', models.CharField(max_length=10)),
                ('status', models.CharField(default='pending', max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
