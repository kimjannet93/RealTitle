# Generated by Django 2.2.5 on 2020-05-02 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_media_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
    ]
