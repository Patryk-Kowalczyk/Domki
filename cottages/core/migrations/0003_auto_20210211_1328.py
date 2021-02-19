# Generated by Django 3.1.6 on 2021-02-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_cottage_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='cottage',
            name='categories',
            field=models.ManyToManyField(to='core.Category'),
        ),
    ]
