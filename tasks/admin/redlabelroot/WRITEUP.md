после того как мы получили доступ к пользователю test, попробуем посмотреть конфиг sudo:

![](imgs/sudopasswordless.jpg)

как мы видим мы можем исполнить команду journalctl -n15 без пароля

поищем как можно повысить привелегии с помощью journalctl:

![](imgs/journalctlprivelegeescalation.jpg)

давайте посмотрим этот [видос](https://www.youtube.com/watch?v%3Dany8EXHDsAQ)

так, а теперь попробуем сделать тоже самое и получить флаг:

![](imgs/easyflag.gif)

![]()

наш флаг:

> surctf_pr1v1l3g3_escalation