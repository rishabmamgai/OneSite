# Generated by Django 3.1.3 on 2021-03-12 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sem1',
            name='practicals',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='sem1',
            name='end_sem',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='sem1',
            name='mid_sem',
            field=models.TextField(),
        ),
    ]