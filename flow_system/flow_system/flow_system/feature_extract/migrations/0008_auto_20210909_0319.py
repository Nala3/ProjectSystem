# Generated by Django 2.2 on 2021-09-09 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_extract', '0007_auto_20210909_0303'),
    ]

    operations = [
        migrations.CreateModel(
            name='flow_feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='null', max_length=100)),
                ('label', models.CharField(default='white', max_length=10)),
                ('feature', models.CharField(max_length=10000)),
            ],
        ),
        migrations.RenameModel(
            old_name='image_featue',
            new_name='image_feature',
        ),
        migrations.DeleteModel(
            name='flow_featue',
        ),
    ]
