# Generated by Django 3.0.5 on 2020-12-30 14:21

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServerStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.CharField(max_length=255)),
                ('disk_info', djongo.models.fields.JSONField()),
                ('up_time', models.CharField(max_length=255)),
                ('memory_info', djongo.models.fields.JSONField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tbl_server_stats',
            },
        ),
    ]
