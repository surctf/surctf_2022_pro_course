from pwn import *

answers = dict()  # словарь вопрос: ответ

while True:
    r = remote("185.104.115.19", 8080)
    r.recvline()  # skip Привет русский Иван цтф участник
    r.recvline()  # skip empty

    question = ''  # глобальная переменная для хранения вопроса
    answer = 0  # глобальная переменная для хранения ответа

    while True:
        answer_result = r.recvline().decode("utf-8")  # [R: 1][ВОПРОС]
        print("Result", answer_result)  # выводим результат

        # если мы уже на что то отвечали
        if (answer_result.count("[R: 1]") == 0):

            # если в последний раз ответили неверно
            if answer_result.count("Плохой ответ") == 1:
                print("BAD")

                # последний ответ был неверным, убавляем значение
                answers[question] = answer - 1
                break
            else:  # если в последний раз ответили верно
                print("OK")

                # последний ответ был верным, записываем не изменяя
                answers[question] = answer

        question = r.recvline().decode("utf-8").strip() # принимаем вопрос

        print("Question: ", question[:30])  # вывод вопроса (для отладки)

        if (question.count("surctf") == 1):  # выходим если нашли флаг
            exit() # выход

        r.recvlines(6) # пропуск 6 строк с мусором

        answer = 4  # дефолтный ответ, если еще не отвечали на этот вопрос

        # если уже отвечали на вопрос, то достаем значение из словаря
        if question in answers:
            answer = answers[question]

        print("Answer: ", answer)
        r.sendline(str(answer)) # отправляем ответ
