# Generated by Django 4.2.13 on 2024-06-18 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_url_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoTimeStamps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.FloatField()),
                ('end_time', models.FloatField()),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.url')),
            ],
        ),
    ]
