package store

import (
	"database/sql"
	"fmt"
	"uuid"
)

type User struct {
	UserID         string `json:"user_id"`
	Username       string `json:"username"`
	Role           string `json:"role"`
	HashedPassword string `json:"hashed_password"`
	Organization   string `json:"organization"`
	CreatedAt      string `json:"created_at"`
}

type UserStore struct {
	db *sql.DB
}

func NewUserStore(db *sql.DB) *UserStore {
	return &UserStore{db: db}
}

// create - insert a new user
func (s *UserStore) CreateUser(u *User) error {
	query := `
		INSERT INTO users (user_id, username, role, hashed_password, organization)
		VALUES ($1, $2, $3, $4, $5)
		RETURNING created_at;`

	newUUID := uuid.New()

	
	u.UserID = newUUID.String()
	err := s.db.QueryRow(query, u.UserID, u.Username, u.Role, u.HashedPassword, u.Organization).Scan(&u.CreatedAt)
	if err != nil {
		return fmt.Errorf("failed to create user: %w", err)
	}
	return nil
}