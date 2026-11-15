package models


type RegisterRequestPayload struct {
	Username string `json:"Username" binding:"required,min=3,max=50"`
	HashedPassword string `json:"password" binding:"required,min=8"`
	Email    string `json:"email" binding:"required"`
}

type RegisterRequestResponse struct {
	RequestID      string `json:"req_id"`
	Username       string `json:"Username"`
	Email          string `json:"email"`
	HashedPassword string `json:"hashed_password"`
	Status         string `json:"status"`
	RequestedAt    string `json:"requested_at"`
	UpdatedAt      string `json:"updated_at"`
}

