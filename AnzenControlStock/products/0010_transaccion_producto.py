# Generated by Django 4.2.10 on 2024-03-08 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_transaccion_user_empleado'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='producto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.producto'),
            preserve_default=False,
        ),
    ]
