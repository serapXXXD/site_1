# PYTON

скопируйте проект командой 

git clone git@github.com:serapXXXD/site_1.git

или

git clone https://github.com/serapXXXD/site_1.git

откройте его в терминале

разверните виртуальное окружение

python -m venv venv

запустите виртуальное окружение

source venv/bin/activate

проваливаемся в new

cd new/

устанавливаем зависимости

pip install -r requirements.txt

проверяем список зависимостей (можно пропустить)

pip list


asgiref==3.6.0
autopep8==2.0.2
Django==4.2
pycodestyle==2.10.0
python-dotenv==1.0.0
sqlparse==0.4.4


поднимаем базу данных

python manage.py  makemigrations

python manage.py migrate

в файле settings.py на 25 строчке замените константу SECRET_KEY_FOR_DJANGO на секретный ключ для джанго

запускаем приложение 

python manage.py runserver

переходим по ссылке

http://127.0.0.1:8000/



