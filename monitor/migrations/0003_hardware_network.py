# Generated by Django 2.1.1 on 2018-12-22 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20181220_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id_agent', models.IntegerField(primary_key=True, serialize=False)),
                ('total', models.IntegerField()),
                ('usage', models.IntegerField()),
                ('free', models.IntegerField()),
                ('cpu_name', models.CharField(max_length=255)),
                ('hw_scan_time', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id_agent', models.IntegerField(primary_key=True, serialize=False)),
                ('n_scan_time', models.DateField()),
                ('mac', models.CharField(max_length=255)),
                ('tx_packets', models.IntegerField()),
                ('tx_bytes', models.IntegerField()),
                ('tx_errors', models.IntegerField()),
                ('tx_dropped', models.IntegerField()),
                ('rx_packets', models.IntegerField()),
                ('rx_bytes', models.IntegerField()),
                ('rx_errors', models.IntegerField()),
                ('rx_dropped', models.IntegerField()),
            ],
        ),
    ]