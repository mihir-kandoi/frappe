# Generated by Django 5.1.2 on 2024-10-25 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_book_qty_in_stock_alter_transaction_issued_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='outstanding',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
