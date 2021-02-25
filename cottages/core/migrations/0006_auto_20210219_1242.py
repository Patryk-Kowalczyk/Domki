# Generated by Django 3.1.6 on 2021-02-19 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210219_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Construction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField(max_length=20)),
            ],
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='Additional',
        ),
        migrations.RemoveField(
            model_name='cottage',
            name='categories',
        ),
        migrations.AddField(
            model_name='cottage',
            name='additionals',
            field=models.ManyToManyField(to='core.Additional'),
        ),
        migrations.AddField(
            model_name='cottage',
            name='number_of_rooms',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cottage',
            name='roof_area',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cottage',
            name='terrace_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='cottage',
            name='construction',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.construction'),
            preserve_default=False,
        ),
    ]