package store

import (
	"database/sql"
	"fmt"

	_ "github.com/jackc/pgx/v5/stdlib"
)

type RegisterRequest struct {
	RequestID      string `json:"req_id"`
	Username       string `json:"Username"`
	Email          string `json:"email"`
	HashedPassword string `json:"hashed_password"`
	Status         string `json:"status"`
	RequestedAt    string `json:"requested_at"`
	UpdatedAt      string `json:"updated_at"`
}

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



type AdminStore struct {
	db *sql.DB
}

func NewAdminStore(db *sql.DB) *AdminStore {
	return &AdminStore{db: db}
}

func (s *AdminStore) CreateRegisterRequest(r *RegisterRequest) error {
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

func (s *AdminStore) GetAllRegisterRequests() ([]*RegisterRequest, error) {
	query := `SELECT req_id, Username, email, hashed_password, status, requested_at, updated_at FROM register_request`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, fmt.Errorf("failed to get all register requests: %w", err)
	}
	defer rows.Close()

	var requests []*RegisterRequest
	for rows.Next() {
		var r RegisterRequest
		if err := rows.Scan(&r.RequestID, &r.Username, &r.Email, &r.HashedPassword, &r.Status, &r.RequestedAt, &r.UpdatedAt); err != nil {
			return nil, fmt.Errorf("failed to scan register request: %w", err)
		}
		requests = append(requests, &r)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error iterating register requests: %w", err)
	}
	return requests, nil
}

func (s *AdminStore) FilterRegisterRequestsByStatus(status string) ([]*RegisterRequest, error) {
	query := `SELECT req_id, username, email, hashed_password, status, requested_at, updated_at FROM register_request WHERE status = $1`

	rows, err := s.db.Query(query, status)
	if err != nil {
		return nil, fmt.Errorf("failed to filter register requests by status: %w", err)
	}
	defer rows.Close()

	var requests []*RegisterRequest
	for rows.Next() {
		var r RegisterRequest
		if err := rows.Scan(&r.RequestID, &r.Username, &r.Email, &r.HashedPassword, &r.Status, &r.RequestedAt, &r.UpdatedAt); err != nil {
			return nil, fmt.Errorf("failed to scan register request: %w", err)
		}
		requests = append(requests, &r)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error iterating filtered register requests: %w", err)
	}

	return requests, nil

}

func (s *AdminStore) GetRegisterRequestsByID(requestID string) (*RegisterRequest, error) {
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

func (s *AdminStore) UpdateRegisterRequestByID(id string, status string) (*RegisterRequest, error) {
	query := `
        UPDATE register_request 
        SET status = $2, updated_at = NOW() 
        WHERE req_id = $1 
        RETURNING req_id, Username, email, hashed_password, status, requested_at, updated_at
    `

	var req RegisterRequest
	err := s.db.QueryRow(query, id, status).Scan(
		&req.RequestID,
		&req.Username,
		&req.Email,
		&req.HashedPassword,
		&req.Status,
		&req.RequestedAt,
		&req.UpdatedAt,
	)

	if err != nil {
		return nil, err
	}

	return &req, nil
}

// CreateUser inserts a new user
func (s *AdminStore) CreateUser(u *User) error {
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