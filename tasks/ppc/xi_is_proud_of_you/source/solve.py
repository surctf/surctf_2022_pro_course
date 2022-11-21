from pwn import *
import sys


ip = "185.104.115.19"

conn = remote(ip, 8080)
conn.recvuntil("Удар!\n\n".encode("utf-8")).decode("utf-8")

questions = {"<q>" : {"answ" : 0, "solved" : False}}
result = ""

try:
	while True:
		print(len(questions))
		# recv [R: %d][ВОПРОС]
		if "[ВОПРОС]" not in result:
			print(conn.recvline().decode("utf-8"))

		q = conn.recvline().decode("utf-8")
		# print("QUESTION: ", q, end="")

		conn.recvline().decode("utf-8")
		answers = []
		for i in range(4):
			answ = conn.recvline().decode("utf-8")
			answers.append(answ)

		# print(answers)
		conn.recvline().decode("utf-8")
		if q in questions:
			if questions[q]["solved"]:
				conn.sendline(str(questions[q]["answ"]).encode("utf-8"))
			else:
				questions[q]["answ"] += 1
				conn.sendline(str(questions[q]["answ"]).encode("utf-8"))
		else:
			questions[q] = {"answ" : 1, "solved" : False}
			conn.sendline(str(questions[q]["answ"]).encode("utf-8"))

		result = conn.recvline().decode("utf-8")

		if "тупой" in result:
			conn.close()
			conn = remote(ip, 8080)
			conn.recvuntil("Удар!\n\n".encode("utf-8")).decode("utf-8")
		else:
			questions[q]["solved"] = True
except:
	conn.interactive()

conn.close()