### - migration

1. go install github.com/pressly/goose/v3/cmd/goose@latest
2. goose -dir migrations postgres postgres://< user >:< password >@localhost:5432/< database >?sslmode=disable up
