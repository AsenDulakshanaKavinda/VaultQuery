package services

import (
	"AuthService/internal/models"
	"AuthService/internal/store"
	"fmt"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var jwtSecret = []byte(os.Getenv("SECRET_JWT_KEY"))

// GenerateToken creates a signed JWT string valid for 6 hours
func GenerateToken(user *store.User) (string, int64, error) {
	expirationTime := time.Now().Add(6 * time.Hour)
	expiresInSeconds := int64(6 * 60 * 60)

	claims := &models.CustomClaims{
		UserID:       user.UserID,
		Username:     user.Username,
		Role:         user.Role,
		Organization: user.Organization,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(expirationTime),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Issuer:    "AuthService",
			Subject:   user.UserID,
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	signedToken, err := token.SignedString(jwtSecret)
	if err != nil {
		return "", 0, fmt.Errorf("failed to sign token: %w", err)
	}

	return signedToken, expiresInSeconds, nil
}
