# Generated by Django 4.0.3 on 2022-03-27 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fundraisers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='cost',
            new_name='amount',
        ),
    ]
