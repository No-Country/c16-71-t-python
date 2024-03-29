from django.db import migrations, models


def create_categorias(apps, schema_editor):
    Categoria = apps.get_model("products", "Categoria")
    nombres = [
        "Electrónica",
        "Ropa",
        "Hogar y Jardín",
        "Alimentos y Bebidas",
        "Salud y Belleza",
        "Juguetes y Juegos",
        "Automotriz",
        "Libros y Audiolibros",
        "Electrodomésticos",
        "Muebles",
        "Instrumentos Musicales",
        "Arte y Manualidades",
        "Cine y Música",
        "Computadoras y Accesorios",
        "Calzado",
        "Bolsos y Accesorios",
        "Bebés y Niños",
        "Joyas y Relojes",
    ]
    categorias = [Categoria(nombre=nombre) for nombre in nombres]
    Categoria.objects.bulk_create(categorias)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categorias),
    ]