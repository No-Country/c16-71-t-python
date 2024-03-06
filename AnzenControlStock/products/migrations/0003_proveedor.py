
from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
       ('products', '0002_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(to='products.proveedor', on_delete=models.CASCADE)
        )
    ]
