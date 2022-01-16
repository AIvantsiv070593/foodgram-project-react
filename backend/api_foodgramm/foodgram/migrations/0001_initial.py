# Generated by Django 3.1 on 2022-01-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientInRicepe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default='0', verbose_name='Колличество')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецептах',
            },
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название Ингредиента')),
                ('measurement_unit', models.CharField(max_length=20, verbose_name='Еденицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название Рецепта')),
                ('image', models.ImageField(help_text='Добавте картинку', upload_to='static/images/', verbose_name='Фото')),
                ('text', models.CharField(default='', max_length=200, verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(default=0, verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, unique=True, verbose_name='Название Тэга')),
                ('slug', models.SlugField(default='', unique=True, verbose_name='uniqueSlug')),
                ('color', models.CharField(max_length=200, unique=True, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ['name'],
            },
        ),
    ]
