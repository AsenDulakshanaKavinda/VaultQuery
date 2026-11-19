package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
	"time"

	"AuthService/internal/models"
	"AuthService/internal/services"
	"AuthService/internal/store"

	"github.com/DATA-DOG/go-sqlmock"
	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestMain(m *testing.M) {
	// Shift working directory to project root so config.LoadSettings() finds the .env file
	_ = os.Chdir("../../")
	os.Setenv("SECRET_REFRESH_KEY", "test-refresh-secret-key-12345")
	os.Setenv("SECRET_JWT_KEY", "test-jwt-secret-key-12345")
	gin.SetMode(gin.TestMode)
	os.Exit(m.Run())
}

func TestAuthHandler_CreateRegisterRequest(t *testing.T) {
	db, mock, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	userStore := store.NewUserStore(db)
	handler := NewAuthHandler(userStore)

	router := gin.New()
	router.POST("/register", handler.CreateRegisterRequest)

	payload := models.RegisterRequestPayload{
		Username: "johndoe",
		Email:    "test@example.com",
		Password: "Password123!",
	}
	body, _ := json.Marshal(payload)

	now := time.Now().UTC().Format(time.RFC3339)
	mock.ExpectQuery(`INSERT INTO register_request`).
		WillReturnRows(sqlmock.NewRows([]string{"requested_at", "updated_at"}).AddRow(now, now))

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/register", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")

	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusCreated, w.Code)
	assert.Contains(t, w.Body.String(), "user register request sent successfully")
	assert.NoError(t, mock.ExpectationsWereMet())
}

func TestAuthHandler_Login_Success(t *testing.T) {
	db, mock, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	userStore := store.NewUserStore(db)
	handler := NewAuthHandler(userStore)

	router := gin.New()
	router.POST("/login", handler.Login)

	hashedPass, _ := services.HashPassword("Password123!")
	now := time.Now().UTC().Format(time.RFC3339)

	rows := sqlmock.NewRows([]string{
		"id", "email", "name", "password_hash", "status", "role", "groups", "title", "location", "organization", "created_at",
	}).AddRow(
		"user-123", "test@example.com", "John Doe", hashedPass, "active", "user", "group1", "Eng", "NY", "Corp", now,
	)

	mock.ExpectQuery(`SELECT .* FROM users WHERE email = \$1 AND status = 'active'`).
		WithArgs("test@example.com").
		WillReturnRows(rows)

	loginReq := models.LoginRequest{
		Email:    "test@example.com",
		Password: "Password123!",
	}
	body, _ := json.Marshal(loginReq)

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/login", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")

	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.Contains(t, w.Body.String(), "access_token")
	assert.Contains(t, w.Body.String(), "refresh_token")
	assert.NoError(t, mock.ExpectationsWereMet())
}

func TestAuthHandler_Login_InvalidCredentials(t *testing.T) {
	db, mock, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	userStore := store.NewUserStore(db)
	handler := NewAuthHandler(userStore)

	router := gin.New()
	router.POST("/login", handler.Login)

	hashedPass, _ := services.HashPassword("CorrectPassword!")
	now := time.Now().UTC().Format(time.RFC3339)

	rows := sqlmock.NewRows([]string{
		"id", "email", "name", "password_hash", "status", "role", "groups", "title", "location", "organization", "created_at",
	}).AddRow(
		"user-123", "test@example.com", "John Doe", hashedPass, "active", "user", "group1", "Eng", "NY", "Corp", now,
	)

	mock.ExpectQuery(`SELECT .* FROM users WHERE email = \$1 AND status = 'active'`).
		WithArgs("test@example.com").
		WillReturnRows(rows)

	loginReq := models.LoginRequest{
		Email:    "test@example.com",
		Password: "WrongPassword!",
	}
	body, _ := json.Marshal(loginReq)

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/login", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")

	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusUnauthorized, w.Code)
	assert.Contains(t, w.Body.String(), "invalid username or password")
	assert.NoError(t, mock.ExpectationsWereMet())
}

func TestAuthHandler_GetMe(t *testing.T) {
	db, mock, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	userStore := store.NewUserStore(db)
	handler := NewAuthHandler(userStore)

	router := gin.New()
	router.GET("/me", func(c *gin.Context) {
		c.Set("id", "user-123")
		c.Next()
	}, handler.GetMe)

	now := time.Now().UTC().Format(time.RFC3339)
	rows := sqlmock.NewRows([]string{
		"id", "email", "name", "password_hash", "status", "role", "groups", "title", "location", "organization", "created_at",
	}).AddRow(
		"user-123", "test@example.com", "John Doe", "hash", "active", "admin", "group1", "Eng", "NY", "Corp", now,
	)

	mock.ExpectQuery(`SELECT .* FROM users WHERE id = \$1 AND status = 'active'`).
		WithArgs("user-123").
		WillReturnRows(rows)

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/me", nil)

	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.Contains(t, w.Body.String(), "test@example.com")
	assert.Contains(t, w.Body.String(), "admin")
	assert.NoError(t, mock.ExpectationsWereMet())
}