package models

import (
	"AuthService/internal/store"

	"github.com/golang-jwt/jwt/v5"
)

type RegisterRequest struct {
	Username     string `json:"username" binding:"required,min=3,max=50"`
	Password     string `json:"password" binding:"required,min=8"`
	Email        string `json:"email" binding:"required"`
	Role         string `json:"role" binding:"required"`
	Organization string `json:"organization" binding:"required"`
}

type UserResponse struct {
	UserID       string `json:"user_id"`
	Username     string `json:"username"`
	Email        string `json:"email"`
	Role         string `json:"role"`
	Organization string `json:"organization"`
	Status       string `json:"status"`
	CreatedAt    string `json:"created_at"`
}

type LoginRequest struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

type TokenResponse struct {
	AccessToken string       `json:"access_token"`
	TokenType   string       `json:"token_type"`
	ExpiresIn   int64        `json:"expires_in"` // expiration in seconds
	User        UserResponse `json:"user"`
}

// CustomClaims stores non-sensitive user metadata inside the JWT
type CustomClaims struct {
	UserID       string `json:"user_id"`
	Username     string `json:"username"`
	Role         string `json:"role"`
	Organization string `json:"organization"`
	jwt.RegisteredClaims
}


func ToUserResponse(u *store.User) UserResponse {
    return UserResponse{
        UserID:       u.UserID,
        Username:     u.Username,
        Email:        u.Email,
        Role:         u.Role,
        Organization: u.Organization,
        Status:       u.Status,
        CreatedAt:    u.CreatedAt,
    }
}
