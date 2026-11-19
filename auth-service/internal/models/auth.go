package models

import (

	"github.com/golang-jwt/jwt/v5"
)



type User struct {
	ID           string `json:"id"`
	Email        string `json:"email"`
	Name         string `json:"name"`
	PasswordHash string `json:"password_hash"`
	Status       string `json:"status"` // pending | active | disabled
	Role         string `json:"role"`   // employee | admin
	Groups       string `json:"groups"`
	Title        string `json:"title"` // grp_account_managers
	Location     string `json:"location"`
	Organization string `json:"organization"`
	CreatedAt    string `json:"created_at"`
}

type PasswordResets struct {
	TokenHash string `json:"token_hash"`
	UserID    string `json:"id"`
	ExpiresAt string `json:"expires_at"`
	UsedAt    string `json:"used_at"`
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


type RegisterRequestPayload struct {
	Username string `json:"Username" binding:"required,min=3,max=50"`
	Password string `json:"password" binding:"required,min=8"`
	Email    string `json:"email" binding:"required"`
}

type UserResponse struct {
	UserID       string `json:"id"`
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
	RefreshToken string `json:"refresh_token"`
	TokenType   string       `json:"token_type"`
	ExpiresIn   int64        `json:"expires_in"` // expiration in seconds
	User        UserResponse `json:"user"`
}

// CustomClaims stores non-sensitive user metadata inside the JWT
type CustomClaims struct {
	UserID       string `json:"id"`
	Username     string `json:"username"`
	Role         string `json:"role"`
	Groups       string `json:"groups"`
	Organization string `json:"organization"`
	jwt.RegisteredClaims
}

func ToUserResponse(u *User) UserResponse {
	return UserResponse{
		UserID:       u.ID,
		Username:     u.Name,
		Email:        u.Email,
		Role:         u.Role,
		Organization: u.Organization,
		Status:       u.Status,
		CreatedAt:    u.CreatedAt,
	}
}
