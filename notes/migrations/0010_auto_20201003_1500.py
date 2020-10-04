# Generated by Django 3.0.7 on 2020-10-03 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0009_auto_20201003_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=10)),
                ('branch', models.CharField(choices=[('Computer Science', 'Computer Science'), ('Mechanical', 'Mechanical'), ('Electrical', 'Electrical'), ('Electronics', 'Electronics')], default='Computer Science', max_length=30)),
                ('role', models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Student', max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='notes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Signup'),
        ),
    ]