# установка с помошью PYTON

скопируйте проект командой 
 ```bash
git clone git@github.com:serapXXXD/site_1.git
 ```
или
 ```bash
git clone https://github.com/serapXXXD/site_1.git
 ```
откройте его в терминале

разверните виртуальное окружение
 ```bash
python -m venv venv
 ```
запустите виртуальное окружение
 ```bash
source venv/bin/activate
 ```
проваливаемся в new
 ```bash
cd backend/new/
 ```
устанавливаем зависимости
 ```bash
pip install -r requirements.txt
 ```
создайте свой сикретный ключ для джанго приложения
```bash
python manage.py createsecretkey название_проекта
 ```
в файле settings.py замените константу SECRET_KEY_FOR_DJANGO на секретный ключ для джанго
```bash
SECRET_KEY = (вставьте сюда полученный секретный ключ)  # в кавычках "key"
 ```

в приложении стоит база данных Postgresql, если вы хотите использовать другую вам необходимо будет заменить на свою

```bash
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.environ.get('POSTGRES_NAME', default='postgres'),
        'USER': os.environ.get('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', default='localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', default='5432'),
    }
}
 ```

выполняем миграций базы данных
```bash
python manage.py  makemigrations

python manage.py migrate
 ```

запускаем приложение 
 ```bash
python manage.py runserver
 ```
переходим по ссылке

http://127.0.0.1:8000/

сайт должен работать

остановите работу сайта комбинацией кнопок ``` CTRL+C ```

создайте супер пользователя 
 ```bash
python manage.py createsuperuser
 ```
заполните требуемые поля

снова запускаем сервер

 ```bash
python manage.py runserver
 ```
далее перейдте по ссылке 

http://127.0.0.1:8000/admin/

авторизуйтесь как супер пользователь, создайте 1 или несколько тегов и 1 или несолько катерий 


после этого сайтом можно пользоваться

# установка через Docker

### У вас должен быть установлен и запущен Docker

скопируйте проект командой 
 ```bash
git clone git@github.com:serapXXXD/site_1.git
 ```
или
 ```bash
git clone https://github.com/serapXXXD/site_1.git
 ```
откройте его в терминале

провалитесь в 
 ```bash
cd blog_infra
 ```

запускаем docker-compose

 ```bash
docker-compose up -d
 ```

проверьте запущенные IMAGES 

 ```bash
docker ps
 ```
должно быть запущенно 3 образа
 ```bash
NAMES
blog_infra_nginx_1
blog_infra_backend_1
blog_infra_data_base_1
 ```

далее нужно сделать миграцию
 ```bash
docker exec blog_infra_backend_1 python manage.py migrate
 ```

и собрать статику
 ```bash
docker exec blog_infra_backend_1 python manage.py collectstatic --no-input
 ```
переходдим по ссылке

http://localhost/

сайт должен работать

далее нужно провалиться в образ с бэкэндом
 ```bash
docker exec -it blog_infra_backend_1 sh
 ```

создайте супер пользователя 
 ```bash
python manage.py createsuperuser
 ```
заполните требуемые поля

выходим из образа
 ```bash
exit
 ```

далее перейдте по ссылке 

http://localhost/admin/

авторизуйтесь как супер пользователь и создайте 1 или несколько тегов и 1 или несолько катерий 


после этого сайтом можно пользоваться
