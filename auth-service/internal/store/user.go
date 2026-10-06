package store

import (
	"database/sql"
	"fmt"
)

type User struct {
	UserID         string `json:"user_id"`
	Username       string `json:"username"`
	Email          string `json:"email"`
	Role           string `json:"role"`
	Status         string `json:"status"` // 'active', 'inactive'
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

// CreateUser inserts a new user
func (s *UserStore) CreateUser(u *User) error {
	query := `
		INSERT INTO users (user_id, username, email, role, hashed_password, organization)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING created_at, status;`

	err := s.db.QueryRow(
		query,
		u.UserID,
		u.Username,
		u.Email,
		u.Role,
		u.HashedPassword,
		u.Organization,
	).Scan(&u.CreatedAt, &u.Status)

	if err != nil {
		return fmt.Errorf("failed to create user: %w", err)
	}
	return nil
}



// GetUserByID fetches a single user by ID
func (s *UserStore) GetUserByEmail(email string) (*User, error) {
	query := `
		SELECT user_id, username, role, hashed_password, organization, created_at, status
		FROM users
		WHERE email = $1 AND status = 'active';`

	u := &User{}
	err := s.db.QueryRow(query, email).Scan(
		&u.UserID,
		&u.Username,
		&u.Role,
		&u.HashedPassword,
		&u.Organization,
		&u.CreatedAt,
		&u.Status,
	)
	if err == sql.ErrNoRows {
		return nil, nil // user not found or inactive
	} else if err != nil {
		return nil, fmt.Errorf("failed to get user: %w", err)
	}
	return u, nil
}


