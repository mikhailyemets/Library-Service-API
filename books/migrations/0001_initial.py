# Generated by Django 5.0.6 on 2024-06-14 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
                'unique_together': {('first_name', 'last_name')},
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('cover', models.CharField(choices=[('Hard', 'Hard'), ('Soft', 'Soft')], default='Hard', max_length=4)),
                ('inventory', models.PositiveIntegerField()),
                ('daily_fee', models.DecimalField(decimal_places=2, max_digits=6)),
                ('authors', models.ManyToManyField(max_length=255, related_name='books', to='books.author')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]