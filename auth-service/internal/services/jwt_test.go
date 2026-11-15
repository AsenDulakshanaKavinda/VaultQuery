package services

import (
	"os"
	"testing"

	"AuthService/internal/models"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestMain(m *testing.M) {
	// Set mock environment variables so config.LoadSettings() succeeds during test execution
	os.Setenv("SECRET_REFRESH_KEY", "test-refresh-secret-key-12345")
	os.Setenv("SECRET_JWT_KEY", "test-jwt-secret-key-12345")
	os.Exit(m.Run())
}

func TestGenerateAndValidateToken(t *testing.T) {
	user := &models.User{
		ID:           "user-uuid-123",
		Name:         "John Doe",
		Role:         "admin",
		Organization: "TechCorp",
	}

	// 1. Test Access Token Generation
	tokenString, expiresIn, err := GenerateToken(user)
	require.NoError(t, err)
	assert.NotEmpty(t, tokenString)
	assert.Equal(t, int64(21600), expiresIn) // 6 hours in seconds

	// 2. Test Access Token Validation
	claims, err := ValidateToken(tokenString)
	require.NoError(t, err)
	require.NotNil(t, claims)
	assert.Equal(t, user.ID, claims.UserID)
	assert.Equal(t, user.Name, claims.Username)
	assert.Equal(t, user.Role, claims.Role)
	assert.Equal(t, user.Organization, claims.Organization)
	assert.Equal(t, "AuthService", claims.Issuer)
}

func TestGenerateAndValidateRefreshToken(t *testing.T) {
	user := &models.User{
		ID:           "user-uuid-456",
		Name:         "Jane Doe",
		Role:         "user",
		Organization: "TechCorp",
	}

	// 1. Test Refresh Token Generation
	refreshTokenString, expiresIn, err := GenerateRefreshToken(user)
	require.NoError(t, err)
	assert.NotEmpty(t, refreshTokenString)
	assert.Equal(t, int64(604800), expiresIn) // 7 days in seconds

	// 2. Test Refresh Token Validation
	claims, err := ValidateRefreshToken(refreshTokenString)
	require.NoError(t, err)
	require.NotNil(t, claims)
	assert.Equal(t, user.ID, claims.UserID)
	assert.Equal(t, "AuthService-Refresh", claims.Issuer)
}

func TestValidateToken_Invalid(t *testing.T) {
	t.Run("Malformed Token", func(t *testing.T) {
		claims, err := ValidateToken("invalid.jwt.token.string")
		assert.Error(t, err)
		assert.Nil(t, claims)
		assert.Equal(t, ErrInvalidToken, err)
	})
}