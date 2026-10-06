package store

import (
	"AuthService/internal/services"
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
func (s *UserStore) GetUserByID(id string) (*User, error) {
	query := `
		SELECT user_id, username, role, hashed_password, organization, created_at, status
		FROM users
		WHERE user_id = $1;`

	u := &User{}
	err := s.db.QueryRow(query, id).Scan(
		&u.UserID,
		&u.Username,
		&u.Role,
		&u.HashedPassword,
		&u.Organization,
		&u.CreatedAt,
		&u.Status,
	)
	if err == sql.ErrNoRows {
		return nil, nil // user not found
	} else if err != nil {
		return nil, fmt.Errorf("failed to get user: %w", err)
	}
	return u, nil
}

// UpdateUserPassword hashes and updates the password for a user
func (s *UserStore) UpdateUserPassword(id string, newPassword string) error {
	query := `UPDATE users SET hashed_password = $1 WHERE user_id = $2;`

	newHashedPassword, err := services.HashPassword(newPassword)
	if err != nil {
		return fmt.Errorf("failed to hash password: %w", err)
	}

	res, err := s.db.Exec(query, newHashedPassword, id)
	if err != nil {
		return fmt.Errorf("failed to update password: %w", err)
	}

	rows, err := res.RowsAffected()
	if err != nil || rows == 0 {
		return fmt.Errorf("no user found to update password")
	}

	return nil
}

// SoftDeleteUser sets the user status to 'inactive' instead of deleting the record
func (s *UserStore) DeleteUser(id string) error {
	query := `UPDATE users SET status = 'inactive' WHERE user_id = $1;`

	res, err := s.db.Exec(query, id)
	if err != nil {
		return fmt.Errorf("failed to deactivate user: %w", err)
	}

	rows, err := res.RowsAffected()
	if err != nil || rows == 0 {
		return fmt.Errorf("no user found to deactivate")
	}

	return nil
}
