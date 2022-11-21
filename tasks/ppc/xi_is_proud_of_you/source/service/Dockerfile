# syntax=docker/dockerfile:1
FROM golang:1.18-alpine

WORKDIR /app

RUN apk add build-base

COPY *go* ./
COPY questions.db ./

RUN go build -o main
CMD [ "./main" ]

