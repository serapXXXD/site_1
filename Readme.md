# PYTON

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
cd new/
 ```
устанавливаем зависимости
 ```bash
pip install -r requirements.txt
 ```
проверяем список зависимостей (можно пропустить)
 ```bash
pip list
 ```
 ```bash
asgiref==3.6.0
autopep8==2.0.2
certifi==2023.7.22
cffi==1.15.1
charset-normalizer==3.2.0
crispy-tailwind==0.5.0
cryptography==41.0.3
defusedxml==0.7.1
Django==4.2
django-allauth==0.56.0
django-crispy-forms==2.0
django-debug-toolbar==4.2.0
django-filter==23.3
djangorestframework==3.14.0
drf-yasg==1.21.7
gunicorn==21.2.0
idna==3.4
inflection==0.5.1
oauthlib==3.2.2
packaging==23.2
Pillow==9.5.0
psycopg2-binary==2.9.9
pycodestyle==2.10.0
pycparser==2.21
PyJWT==2.8.0
python-dotenv==1.0.0
python3-openid==3.2.0
pytz==2023.3
PyYAML==6.0.1
requests==2.31.0
requests-oauthlib==1.3.1
sqlparse==0.4.4
uritemplate==4.1.1
urllib3==2.0.4

 ```

поднимаем базу данных
 ```bash
python manage.py  makemigrations

python manage.py migrate
 ```
в файле settings.py на 25 строчке замените константу SECRET_KEY_FOR_DJANGO на секретный ключ для джанго

запускаем приложение 
 ```bash
python manage.py runserver
 ```
переходим по ссылке

http://127.0.0.1:8000/



