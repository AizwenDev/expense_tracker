# Generated migration for Expense model

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount spent in Philippine Peso (₱)', max_digits=10)),
                ('category', models.CharField(choices=[('food', '🍔 Food'), ('transport', '🚗 Transport'), ('bills', '💡 Bills'), ('other', '📦 Other')], default='other', help_text='Type of expense', max_length=20)),
                ('date', models.DateField(default=django.utils.timezone.now, help_text='Date of the expense')),
                ('description', models.TextField(blank=True, help_text='Optional description or notes', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
                'ordering': ['-date', '-created_at'],
            },
        ),
    ]