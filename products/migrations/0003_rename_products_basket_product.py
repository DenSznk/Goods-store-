# Generated by Django 4.1.3 on 2022-12-02 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_basket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='products',
            new_name='product',
        ),
    ]
