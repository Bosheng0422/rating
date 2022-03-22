# Generated by Django 4.0.3 on 2022-03-20 03:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0005_remove_rate_module_remove_rate_professor'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='module',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='rating.module'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rate',
            name='professor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='rating.professor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='professor',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='rate',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]