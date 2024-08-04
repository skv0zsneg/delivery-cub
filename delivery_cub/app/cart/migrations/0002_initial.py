# Generated by Django 5.0.7 on 2024-08-04 19:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        ('restaurant', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='dish',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='блюдо', to='restaurant.dish', verbose_name='cart_position'),
        ),
        migrations.AddField(
            model_name='cart',
            name='positions',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart', to='cart.cartposition', verbose_name='позиция'),
        ),
    ]
