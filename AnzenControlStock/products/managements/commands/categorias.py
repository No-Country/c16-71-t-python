from django.core.management.base import BaseCommand
from products.models import Categoria


class Command(BaseCommand):
    help = "Crea categorias manualmente"

    def handle(self, *args, **kwargs):
        categorias = [
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

        for categoria_name in categorias:
            Categoria.objects.get_or_create(name=categoria_name)
            self.stdout.write(self.style.SUCCESS(f"Se creó la categoria: {categoria_name}"))
