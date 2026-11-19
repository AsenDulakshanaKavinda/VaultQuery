package services

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"golang.org/x/crypto/bcrypt"
)

func TestHashPassword(t *testing.T) {
	password := "SecurePassword123!"

	hash, err := HashPassword(password)
	assert.NoError(t, err)
	assert.NotEmpty(t, hash)
	assert.NotEqual(t, password, hash)

	// Verify that the hash was generated using the expected bcrypt cost
	cost, err := bcrypt.Cost([]byte(hash))
	assert.NoError(t, err)
	assert.Equal(t, bcrypt.DefaultCost, cost)
}

func TestCheckPasswordHash(t *testing.T) {
	password := "SecurePassword123!"
	wrongPassword := "WrongPassword456!"

	// Generate a valid hash to test against
	hash, err := HashPassword(password)
	assert.NoError(t, err)

	t.Run("Matching Password Succeeds", func(t *testing.T) {
		match := CheckPasswordHash(password, hash)
		assert.True(t, match)
	})

	t.Run("Non-Matching Password Fails", func(t *testing.T) {
		match := CheckPasswordHash(wrongPassword, hash)
		assert.False(t, match)
	})

	t.Run("Malformed Hash Fails Gracefully", func(t *testing.T) {
		match := CheckPasswordHash(password, "not-a-valid-bcrypt-hash")
		assert.False(t, match)
	})
}