# Generated by Django 4.2.7 on 2023-12-11 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='lang',
            field=models.CharField(choices=[('zh', 'Chinese'), ('en', 'English'), ('es', 'Spanish'), ('ja', 'Japanese')], default=None, help_text='node lang', max_length=2),
        ),
    ]