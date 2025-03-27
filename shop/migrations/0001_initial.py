import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.contrib.auth.models import User


def add_default_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    # Create default products
    Product.objects.get_or_create(name='Djan', price=9.99, description='Good Djan', stock=10)
    Product.objects.get_or_create(name='Djan Pro', price=19.99, description='Best Djan', stock=5)
    Product.objects.get_or_create(name='Go', price=24.99, description='Good Pro', stock=3)
    Product.objects.get_or_create(name='Go Pro', price=499.99, description='Best Pro', stock=0)

    # Avoid creating superuser here; it's better done manually or via command line.
    # For demonstration, we'll skip creating users here in the migration.

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # Add dependencies if any (e.g., previous migrations or external apps)
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField()),
                ('stock', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.RunPython(add_default_products),
    ]
