# praktikum_new_diplom
foodgram-project-react - API для проекта Foodgramm.  
Проект где пользователь может создавать свои рецепты, просматривать чужие рецепты.  
Есть список избранных рецептов. Есть список покупок.  
Можно скачать список покупок с наименованием и количеством ингридиентов.  
  
Развернуть проект:

Загрузить и запустить на сервере контейнер Docker  
docker pull aivanstiv070593/foodgramm:infra_frontend  
docker pull aivanstiv070593/foodgramm:infra_backend

На сервере выполнить из под root:  
docker-compose up -d # Запускаем приложение  
docker-compose exec backend python manage.py migrate # Применяем миграции  
docker-compose exec backend python manage.py collectstatic --no-input # Собираем статику  
docker-compose exec backend python manage.py createsuperuser # Создать администратора  
docker-compose exec backend python manage.py load_data --file ingredients.csv # Наполняем БД начальными данными, файл положить в data.



Тестовый администратор:  
Login admin@mail.ru  
password admin
