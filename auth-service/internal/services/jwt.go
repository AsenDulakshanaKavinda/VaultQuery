package services

import (
	"AuthService/internal/models"
	"AuthService/internal/store"
	"errors"
	"fmt"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var jwtSecret = []byte(os.Getenv("SECRET_JWT_KEY"))

var (
	ErrInvalidToken = errors.New("invalid or tampered token")
	ErrExpiredToken = errors.New("token has expired")
)

// GenerateToken creates a signed JWT string valid for 6 hours
func GenerateToken(user *store.User) (string, int64, error) {
	expirationTime := time.Now().Add(6 * time.Hour)
	expiresInSeconds := int64(6 * 60 * 60)

	claims := &models.CustomClaims{
		UserID:       user.UserID,
		Username:     user.Username,
		Role:         user.Role,
		Organization: user.Organization,
	}

	claims.ExpiresAt = jwt.NewNumericDate(expirationTime)
	claims.IssuedAt = jwt.NewNumericDate(time.Now())
	claims.Issuer = "AuthService"
	claims.Subject = user.UserID


	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	signedToken, err := token.SignedString(jwtSecret)
	if err != nil {
		return "", 0, fmt.Errorf("failed to sign token: %w", err)
	}

	return signedToken, expiresInSeconds, nil
}

// ValidateToken parses, verifies the signature, and returns claims from a JWT string
func ValidateToken(tokenString string) (*models.CustomClaims, error) {
	// parse the token with claims validation
	token, err := jwt.ParseWithClaims(tokenString, &models.CustomClaims{}, func(token *jwt.Token) (interface{}, error) {
		// verify that the signing method matches expected HMAC algorithm (HS256)
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return jwtSecret, nil
	})

	if err != nil {
		if errors.Is(err, jwt.ErrTokenExpired) {
			return nil, ErrExpiredToken
		}
		return nil, ErrInvalidToken
	}

	// extract and validate claims
	claims, ok := token.Claims.(*models.CustomClaims)
	if !ok || !token.Valid {
		return nil, ErrInvalidToken
	}

	return claims, nil
}
