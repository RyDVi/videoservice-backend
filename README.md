# videoservice-backend
Необходимо многое удалить. 
Не реализована до конца реаомендательная система с использование GPT. По изначальной задумке должен был быть чат вида:
- хочу посмотреть фильмы с тем-то или кем-то или по настроению
- gpt выдаёт результаты с фильмами из картотеки (выдаёт вместе со ссылками и постерами), либо говорит, что такого к сожалению нет, но есть вот этот список...

## Direnv (linux)
Install direnv
Add direnv hook to your shell https://direnv.net/docs/hook.html
Description:
In ~/.bashrc add line at the end of file: ```eval "$(direnv hook bash)"```

Allow direnv: `direnv allow`.


```
   source_env .direnvrc
   layout python
   layout postgres
   # Activate local venv
   source $VIRTUAL_ENV/bin/activate
   #For enable django-admin runserver need add backend into PYTHONPATH
   export PYTHONPATH=$PWD/backend
   export DJANGO_SETTINGS_MODULE=backend.settings
   export CDN_VIDEO_USERNAME=...
   export CDN_VIDEO_EMAIL=...
   export CDN_VIDEO_PASSWORD=...
   export OPENAI_API_KEY=...
```

## Linux console
export DJANGO_SETTINGS_MODULE=backend.settings
export PYTHONPATH=backend
export USER=postgres
export PGPASSWORD=admin
export PGHOST=localhost
export PGPORT=5432
export OPENAI_API_KEY=...

## PowerShell (windows)
Before, create venv with command:
```
py -m venv venv
```

Also, disable restriction for PowerShell (need execute from administrator):
```
Set-ExecutionPolicy Unrestricted -Force
```

After, run venv and export env variables:
```
venv\Scripts\Activate.ps1
$Env:DJANGO_SETTINGS_MODULE="backend.settings"
$Env:PYTHONPATH="backend"
$Env:USER="postgres"
$Env:PGPASSWORD="admin"
$Env:PGHOST="localhost"
$Env:PGPORT="5432"
```

If you has access to CDN then add credentials
```
$Env:CDN_VIDEO_USERNAME="..."
$Env:CDN_VIDEO_EMAIL="..."
$Env:CDN_VIDEO_PASSWORD="..."
```

If you don't have access then will be used default file storage.

For using GPT need API Key:
```
$Env:OPENAI_API_KEY="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"
```

## First run
If ```django-admin runserver``` not work then run ```python -m manage runserver```.
1. Create org with ```django-admin create_org```
2. Create superuser with ```createsuperuser```

## Commands
which command for get path

## Posgtres

### Postgres start
Message from console:
"""
You can now start the database server using:
pg_ctl -D /home/rydvi/Documents/videoservice/videoservice-backend/.direnv/postgres -l logfile start
pg_ctl -D $PGDATA -l logfile start
"""

But start need with command "postgres". After all will work. Before, symbolic links to commands are needed if they are not found

### Resolve postgres problems
To find command use: find / -name initdb
1. initdb not foud
Add symbolic link to initdb: sudo ln -s /usr/lib/postgresql/14/bin/initdb /usr/local/bin/

2. pg_ctl not found
Add symbolic link to pg_ctl: sudo ln -s /usr/lib/postgresql/14/bin/pg_ctl /usr/local/bin/

3. postgres not found
Add symbolic link to postgres: sudo ln -s /usr/lib/postgresql/14/bin/postgres /usr/local/bin/

4. Install:
sudo apt-get install -y libpq-dev
pip install psycopg2
pip install psycopg2-binary

If not working then uninstall both psycopg2 and psycopg2-binary and reinstall only psycopg2-binary


# videoservice-frontend
# Settings

## Multiple hosts

1. Allow for node port :80
   sudo apt-get install libcap2-bin
   sudo setcap cap_net_bind_service=+ep `readlink -f \`which node\``

2. Add in hosts next hosts
   Windows 10 — «C:\Windows\System32\drivers\etc\hosts»
   Linux — «/etc/hosts»
   Mac OS X — «/private/etc/hosts»

   127.0.0.1 blue.videoservice.com
   127.0.0.1 red.videoservice.com
   127.0.0.1 green.videoservice.com
   127.0.0.1 videoservice.com

3. Optional. If process already used.
   sudo kill -9 $(sudo lsof -t -i:80)

## source-map-explorer

devtool: 'inline-source-map' used for it

1. yarn build or yarn build-producation
2. npx source-map-explorer dist/\*.js --html result.html

## .envrc
source_env .direnvrc
layout python
layout postgres
# Activate local venv
source $VIRTUAL_ENV/bin/activate
#For enable django-admin runserver need add backend into PYTHONPATH
export PYTHONPATH=$PWD/backend
export DJANGO_SETTINGS_MODULE=backend.settings
export CDN_VIDEO_USERNAME=
export CDN_VIDEO_EMAIL=
export CDN_VIDEO_PASSWORD=