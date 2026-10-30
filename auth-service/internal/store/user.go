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

type RegisterRequest struct {
	RequestID      string `json:"req_id"`
	Username       string `json:"Username"`
	Email          string `json:"email"`
	HashedPassword string `json:"hashed_password"`
	Status         string `json:"status"`
	RequestedAt    string `json:"requested_at"`
	UpdatedAt      string `json:"updated_at"`
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

func (s *UserStore) CreateRegisterRequest(r *RegisterRequest) error {
    query := `
        INSERT INTO register_request (req_id, username, email, hashed_password, status, requested_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        RETURNING requested_at, updated_at;`

    err := s.db.QueryRow(
        query,
        r.RequestID,
        r.Username,
        r.Email,
        r.HashedPassword,
        r.Status,
    ).Scan(&r.RequestedAt, &r.UpdatedAt)

    if err != nil {
        return fmt.Errorf("failed to create register request: %w", err)
    }
    return nil
}

func (s *UserStore) GetRegisterRequestsByID(requestID string) (*RegisterRequest, error) {
	query := `SELECT req_id, Username, email, hashed_password, status, requested_at, updated_at FROM register_request WHERE req_id = $1`

	var r RegisterRequest
	err := s.db.QueryRow(query, requestID).Scan(
		&r.RequestID,
		&r.Username,
		&r.Email,
		&r.HashedPassword,
		&r.Status,
		&r.RequestedAt,
		&r.UpdatedAt,
	)

	if err != nil {
		if err == sql.ErrNoRows {
			return nil, fmt.Errorf("register request not found: %w", err)
		}
		return nil, fmt.Errorf("failed to get register request by id: %w", err)
	}
	return &r, nil
}


// GetUserByID fetches a single user by Email
func (s *UserStore) GetUserByEmail(email string) (*User, error) {
	query := `
		SELECT user_id, username, email, role, hashed_password, organization, created_at, status
		FROM users
		WHERE email = $1 AND status = 'active';`

	u := &User{}
	err := s.db.QueryRow(query, email).Scan(
		&u.UserID,
		&u.Username,
		&u.Email,
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

// GetUserByID fetches a single user by ID
func (s *UserStore) GetUserByID(id string) (*User, error) {
	query := `
		SELECT user_id, username, email, role, hashed_password, organization, created_at, status
		FROM users
		WHERE user_id = $1 AND status = 'active';`

	u := &User{}
	err := s.db.QueryRow(query, id).Scan(
		&u.UserID,
		&u.Username,
		&u.Email,
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
