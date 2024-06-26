# Generated by Django 4.2.13 on 2024-06-23 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_videotimestamps'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prediction', models.CharField(blank=True, max_length=2, null=True)),
                ('video_timestamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.videotimestamps')),
            ],
        ),
    ]
