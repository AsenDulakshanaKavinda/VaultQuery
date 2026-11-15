package services

import (
	"AuthService/internal/config"
	"AuthService/internal/models"
	"errors"
	"fmt"
	"log"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

// var jwtSecret = []byte(os.Getenv("SECRET_JWT_KEY"))

var (
	ErrInvalidToken = errors.New("invalid or tampered token")
	ErrExpiredToken = errors.New("token has expired")
)

// GenerateToken creates a signed JWT string valid for 6 hours
// return signedToken, expiresInSeconds, error
func GenerateToken(user *models.User) (string, int64, error) {
	expirationTime := time.Now().Add(6 * time.Hour)
	expiresInSeconds := int64(6 * 60 * 60)

	claims := &models.CustomClaims{
		UserID:       user.ID,
		Username:     user.Name,
		Role:         user.Role,
		Organization: user.Organization,
	}

	claims.ExpiresAt = jwt.NewNumericDate(expirationTime)
	claims.IssuedAt = jwt.NewNumericDate(time.Now())
	claims.Issuer = "AuthService"
	claims.Subject = user.ID

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	settings, err := config.LoadSettings()
	if err != nil {
		log.Printf("failed to read secret refresh key: %v\n", err)
	}

	secret := []byte(settings.SecretRefreshKey)
	signedToken, err := token.SignedString(secret)
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

		settings, err := config.LoadSettings()
		if err != nil {
			log.Printf("failed to read secret refresh key: %v\n", err)
		}
		secret := []byte(settings.SecretRefreshKey)
		return secret, nil
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

var refreshJwtSecret = []byte(getRefreshSecret())

func getRefreshSecret() string {
	settings, err := config.LoadSettings()
	if err != nil {
		log.Printf("failed to read refresh key: %v\n", err)
	}
	secret := settings.SecretRefreshKey
	if secret == "" {
		return settings.SecretJwtKey
	}
	return secret
}

func GenerateRefreshToken(user *models.User) (string, int64, error) {
	// Set a longer expiration time, for example: 7 days
	expirationTime := time.Now().Add(7 * 24 * time.Hour)
	expiresInSeconds := int64(7 * 24 * 60 * 60)

	claims := &models.CustomClaims{
		UserID:       user.ID,
		Username:     user.Name,
		Role:         user.Role,
		Organization: user.Organization,
	}

	claims.ExpiresAt = jwt.NewNumericDate(expirationTime)
	claims.IssuedAt = jwt.NewNumericDate(time.Now())
	claims.Issuer = "AuthService-Refresh"
	claims.Subject = user.ID

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	signedToken, err := token.SignedString(refreshJwtSecret)
	if err != nil {
		return "", 0, fmt.Errorf("failed to sign refresh token: %w", err)
	}

	return signedToken, expiresInSeconds, nil
}

// ValidateRefreshToken parses, verifies the signature using the refresh secret, and returns claims from a refresh token string
func ValidateRefreshToken(tokenString string) (*models.CustomClaims, error) {
	// Parse the token with claims validation using the refresh secret
	token, err := jwt.ParseWithClaims(tokenString, &models.CustomClaims{}, func(token *jwt.Token) (interface{}, error) {
		// Verify that the signing method matches the expected HMAC algorithm (HS256)
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return refreshJwtSecret, nil // Crucial: uses the refresh secret instead of the access secret
	})

	if err != nil {
		if errors.Is(err, jwt.ErrTokenExpired) {
			return nil, ErrExpiredToken
		}
		return nil, ErrInvalidToken
	}

	// Extract and validate claims
	claims, ok := token.Claims.(*models.CustomClaims)
	if !ok || !token.Valid {
		return nil, ErrInvalidToken
	}

	return claims, nil
}
