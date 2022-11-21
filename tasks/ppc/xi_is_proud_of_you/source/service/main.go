package main

import (
	"bufio"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"log"
	"math/rand"
	"net"
	"strconv"
	"time"
)

type Question struct {
	ID        int
	Text      string
	ValidAnsw string
	BadAnsw1  string
	BadAnsw2  string
	BadAnsw3  string
	ValidInd  int
}

const (
	HOST   = "0.0.0.0"
	PORT   = "8080"
	TYPE   = "tcp"
	LEVELS = 500
	FLAG   = "surctf_kitai_procvetanie_udar"
)

func main() {
	rand.Seed(time.Now().UnixNano())

	log.Printf("Starting TCP server on %s:%s", HOST, PORT)
	listener, err := net.Listen("tcp", HOST+":"+PORT)
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()

	db, err := gorm.Open(sqlite.Open("questions.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect database")
	}

	for {
		c, err := listener.Accept()
		if err != nil {
			log.Println("Error connecting:", err.Error())
			return
		}

		log.Printf("Client %s connected\n", c.RemoteAddr().String())

		go handleConnection(c, db)
	}
}

func handleConnection(conn net.Conn, db *gorm.DB) {
	defer conn.Close()

	conn.Write([]byte("Привет русский Иван цтф участник курса! Это игра ответ вопрос социальный рейтинг увеличить. Когда рейтинг 500 флаг получить! Удар!\n\n"))

	for i := 0; i < LEVELS; i++ {
		var q Question
		db.Find(&q, "id = ?", rand.Int()%1000+1)

		conn.Write([]byte("[R: " + strconv.Itoa(i+1) + "]"))
		conn.Write([]byte("[ВОПРОС]\n"))

		conn.Write([]byte("    " + q.Text + "\n"))
		conn.Write([]byte("[ОТВЕТ]\n"))

		badAnswers := []string{q.BadAnsw1, q.BadAnsw2, q.BadAnsw3}
		for i := 1; i < 5; i++ {
			if i == q.ValidInd {
				conn.Write([]byte("   " + strconv.Itoa(i) + ". " + q.ValidAnsw + "\n"))
				continue
			}

			badAnsw := badAnswers[0]
			badAnswers = badAnswers[1:]
			conn.Write([]byte("   " + strconv.Itoa(i) + ". " + badAnsw + "\n"))
		}

		conn.Write([]byte("Твой ответ:\n"))
		bytesBuff, err := bufio.NewReader(conn).ReadBytes('\n')
		if err != nil {
			log.Println("Client left")
			return
		}
		answ, err := strconv.Atoi(string(bytesBuff[:len(bytesBuff)-1]))
		if err != nil || answ != q.ValidInd {
			conn.Write([]byte("Плохой ответ тупой Иван пока пока кушай больше рис стать умным\n"))
			return
		}
	}

	conn.Write([]byte("Иван молодец рейтинг " + strconv.Itoa(LEVELS) + " поздравление партия гордится тобой твой подарок:\n"))
	conn.Write([]byte(FLAG + "\n"))
}
