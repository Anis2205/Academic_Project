# Generated manually

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('greenapp', '0002_alter_diy_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteVisitStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, unique=True)),
                ('visit_count', models.PositiveIntegerField(default=0)),
                ('unique_visitors', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Site Visit Statistic',
                'verbose_name_plural': 'Site Visit Statistics',
                'ordering': ['-date'],
            },
        ),
    ]