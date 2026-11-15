package store

import (
	"AuthService/internal/models"
	"database/sql"
	"fmt"
)

type UserStore struct {
	db *sql.DB
}

func NewUserStore(db *sql.DB) *UserStore {
	return &UserStore{db: db}
}

// CreateUser inserts a new user
func (s *UserStore) CreateUser(u *models.User) error {
	query := `
		INSERT INTO users (id, email, name, password_hash, status, role, groups, title, location, organization, created_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
		RETURNING created_at, status;`

	err := s.db.QueryRow(
		query,
		u.ID,
		u.Email,
		u.Name,
		u.PasswordHash,
		u.Status,
		u.Role,
		u.Groups,
		u.Title,
		u.Location,
		u.Organization,
		u.CreatedAt,
	).Scan(&u.CreatedAt, &u.Status, &u.Role, &u.Groups)

	if err != nil {
		return fmt.Errorf("failed to create a new user: %w", err)
	}
	return nil
}

// GetUserByID fetch a single user by Email
func (s *UserStore) GetUserByEmail(email string) (*models.User, error) {
	query := `
		SELECT id, email, name, password_hash, status, role, groups, title, location, organization, created_at
		FROM users
		WHERE email = $1 AND status = 'active';`

	u := &models.User{}
	err := s.db.QueryRow(query, email).Scan(
		&u.ID,
		&u.Email,
		&u.Name,
		&u.PasswordHash,
		&u.Status,
		&u.Role,
		&u.Groups,
		&u.Title,
		&u.Location,
		&u.Organization,
		&u.CreatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, nil // user not found or inactive
	} else if err != nil {
		return nil, fmt.Errorf("failed to get user: %w", err)
	}
	return u, nil
}

// GetUserByID fetch a single user by ID
func (s *UserStore) GetUserByID(id string) (*models.User, error) {
	query := `
		SELECT id, email, name, password_hash, status, role, groups, title, location, organization, created_at
		FROM users
		WHERE id = $1 AND status = 'active';`

	u := &models.User{}
	err := s.db.QueryRow(query, id).Scan(
		&u.ID,
		&u.Email,
		&u.Name,
		&u.PasswordHash,
		&u.Status,
		&u.Role,
		&u.Groups,
		&u.Title,
		&u.Location,
		&u.Organization,
		&u.CreatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, nil // user not found or inactive
	} else if err != nil {
		return nil, fmt.Errorf("failed to get user: %w", err)
	}
	return u, nil
}

// CreateRegisterRequest insert a new register request
func (s *UserStore) CreateRegisterRequest(r *models.RegisterRequest) error {
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
