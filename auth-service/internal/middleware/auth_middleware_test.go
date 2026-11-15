package middleware

import (
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	"AuthService/internal/models"
	"AuthService/internal/services"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestMain(m *testing.M) {
	// Shift working directory from internal/middleware to the project root 
	// so config.LoadSettings() can successfully locate the root .env file.
	_ = os.Chdir("../../")

	gin.SetMode(gin.TestMode)
	os.Exit(m.Run())
}

func TestAuthMiddleware(t *testing.T) {
	// Generate a valid token for success test cases
	user := &models.User{
		ID:   "user-uuid-123",
		Name: "John Doe",
		Role: "admin",
	}
	validToken, _, err := services.GenerateToken(user)
	require.NoError(t, err)

	router := gin.New()
	router.GET("/protected", AuthMiddleware(), func(c *gin.Context) {
		id, _ := c.Get("id")
		role, _ := c.Get("role")
		c.JSON(http.StatusOK, gin.H{"id": id, "role": role})
	})

	t.Run("Missing Authorization Header", func(t *testing.T) {
		w := httptest.NewRecorder()
		req, _ := http.NewRequest("GET", "/protected", nil)
		router.ServeHTTP(w, req)

		assert.Equal(t, http.StatusUnauthorized, w.Code)
		assert.Contains(t, w.Body.String(), "authorization header required")
	})

	t.Run("Invalid Authorization Header Format", func(t *testing.T) {
		w := httptest.NewRecorder()
		req, _ := http.NewRequest("GET", "/protected", nil)
		req.Header.Set("Authorization", "InvalidTokenFormat")
		router.ServeHTTP(w, req)

		assert.Equal(t, http.StatusUnauthorized, w.Code)
		assert.Contains(t, w.Body.String(), "invalid authorization header format")
	})

	t.Run("Invalid Token String", func(t *testing.T) {
		w := httptest.NewRecorder()
		req, _ := http.NewRequest("GET", "/protected", nil)
		req.Header.Set("Authorization", "Bearer bad.token.string")
		router.ServeHTTP(w, req)

		assert.Equal(t, http.StatusUnauthorized, w.Code)
		assert.Contains(t, w.Body.String(), "invalid or expired token")
	})

	t.Run("Valid Token Succeeds and Populates Context", func(t *testing.T) {
		w := httptest.NewRecorder()
		req, _ := http.NewRequest("GET", "/protected", nil)
		req.Header.Set("Authorization", "Bearer "+validToken)
		router.ServeHTTP(w, req)

		assert.Equal(t, http.StatusOK, w.Code)
		assert.Contains(t, w.Body.String(), "user-uuid-123")
		assert.Contains(t, w.Body.String(), "admin")
	})
}