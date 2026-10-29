package models

import "admin-service/internal/store"

type RegisterRequestPayload struct {
	Username string `json:"username" binding:"required,min=3,max=50"`
	Password string `json:"password" binding:"required,min=8"`
	Email    string `json:"email" binding:"required"`
}

type RegisterRequestResponse struct {
	RequestID      string `json:"request_id"`
	UserName       string `json:"username"`
	Email          string `json:"email"`
	HashedPassword string `json:"hashed_password"`
	Status         string `json:"status"`
	RequestedAt    string `json:"requested_at"`
	UpdatedAt      string `json:"updated_at"`
}

func ToRegisterRequestResponse(u *store.RegisterRequest) RegisterRequestResponse {
	return RegisterRequestResponse{
		RequestID:      u.RequestID,
		UserName:       u.UserName,
		Email:          u.Email,
		HashedPassword: u.HashedPassword,
		Status:         u.Status,
		RequestedAt:    u.RequestedAt,
		UpdatedAt:      u.UpdatedAt,
	}
}
