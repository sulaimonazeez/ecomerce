# Generated by Django 4.2.4 on 2023-10-18 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_products_alter_cart_products_alter_cartitem_product_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['-id']},
        ),
    ]
