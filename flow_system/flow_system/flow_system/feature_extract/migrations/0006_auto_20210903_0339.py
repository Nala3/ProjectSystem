# Generated by Django 2.1.8 on 2021-09-03 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_extract', '0005_auto_20210831_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tls_feature',
            name='certificate',
            field=models.CharField(max_length=5000),
        ),
    ]
