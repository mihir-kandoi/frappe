# Generated by Django 5.1.2 on 2024-10-25 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_transaction_issued_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='qty_in_stock',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='issued_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='penalty_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='returned_on',
            field=models.DateField(blank=True, null=True),
        ),
    ]
