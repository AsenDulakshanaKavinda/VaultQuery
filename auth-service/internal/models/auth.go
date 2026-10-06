package models

type RegisterRequest struct {
	Username     string `json:"name" binding:"required,min=3,max=50"`
	Password     string `json:"password" binding:"required,min=8"`
	Email        string `json:"email" binding:"required"`
	Role         string `json:"role" binding:"required"`
	Organization string `json:"organization" binding:"required"`
}

type UserResponse struct {
	UserID       string `json:"user_id"`
	Username     string `json:"name"`
	Email        string `json:"email"`
	Role         string `json:"role"`
	Organization string `json:"organization"`
	Status       string `json:"status"`
	CreatedAt    string `json:"created_at"`
}
