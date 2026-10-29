package store

import (
	"database/sql"
	"fmt"
)

type RegisterRequest struct {
	RequestID      string `json:"request_id"`
	UserName       string `json:"username"`
	Email          string `json:"email"`
	HashedPassword string `json:"hashed_password"`
	Status         string `json:"status"`
	RequestedAt    string `json:"requested_at"`
	UpdatedAt      string `json:"updated_at"`
}

type AdminStore struct {
	db *sql.DB
}

func NewAdminStore(db *sql.DB) *AdminStore {
	return &AdminStore{db: db}
}

func (s *AdminStore) CreateRegisterRequest(r *RegisterRequest) error {
	query := `
		INSERT INTO register_request (request_id, username, email, handed_password, status, requested_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7)
		RETURNING status, requested_at;`

	err := s.db.QueryRow(
		query,
		r.RequestID,
		r.UserName,
		r.Email,
		r.HashedPassword,
		r.Status,
		r.RequestedAt,
		r.UpdatedAt,
	).Scan(&r.Status, &r.RequestedAt)

	if err != nil {
		return fmt.Errorf("failed to create register request: %w", err)
	}
	return nil

}

func (s *AdminStore) GetAllRegisterRequests() ([]*RegisterRequest, error) {
	query := `SELECT request_id, username, email, hashed_password, status, requested_at, updated_at FROM register_request`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, fmt.Errorf("failed to get all register requests: %w", err)
	}
	defer rows.Close()

	var requests []*RegisterRequest
	for rows.Next() {
		var r RegisterRequest
		if err := rows.Scan(&r.RequestID, &r.UserName, &r.Email, &r.HashedPassword, &r.Status, &r.RequestedAt, &r.UpdatedAt); err != nil {
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
	query := `SELECT request_id, username, email, hashed_password, status, requested_at, updated_at FROM register_request WHERE request_id = $1`

	rows, err := s.db.Query(query, status)
	if err != nil {
		return nil, fmt.Errorf("failed to filter register requests by status: %w", err)
	}
	defer rows.Close()

	var requests []*RegisterRequest
	for rows.Next() {
		var r RegisterRequest
		if err := rows.Scan(&r.RequestID, &r.UserName, &r.Email, &r.HashedPassword, &r.Status, &r.RequestedAt, &r.UpdatedAt); err != nil {
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
	query := `SELECT request_id, username, email, hashed_password, status, requested_at, updated_at FROM register_request WHERE request_id = $1`

	var r RegisterRequest
	err := s.db.QueryRow(query, requestID).Scan(
		&r.RequestID,
		&r.UserName,
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
