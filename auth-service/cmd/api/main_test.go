package main

import (
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"
	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestMain(m *testing.M) {
	os.Setenv("SECRET_REFRESH_KEY", "test-refresh-secret-key-12345")
	os.Setenv("SECRET_JWT_KEY", "test-jwt-secret-key-12345")
	gin.SetMode(gin.TestMode)
	os.Exit(m.Run())
}

func TestSetupRouter_PublicRoute(t *testing.T) {
	db, _, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	r := SetupRouter(db)

	w := httptest.NewRecorder()
	// Sending a request to login with an empty body should trigger a bad request (400)
	// confirming the route is properly registered and routed to the handler.
	req, _ := http.NewRequest("POST", "/api/v1/auth/login", nil)
	req.Header.Set("Content-Type", "application/json")

	r.ServeHTTP(w, req)

	assert.Equal(t, http.StatusBadRequest, w.Code)
}

func TestSetupRouter_ProtectedUnauthorized(t *testing.T) {
	db, _, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	r := SetupRouter(db)

	w := httptest.NewRecorder()
	// Accessing a protected route without a Bearer token should fail with 401 Unauthorized
	req, _ := http.NewRequest("GET", "/api/v1/auth/me", nil)

	r.ServeHTTP(w, req)

	assert.Equal(t, http.StatusUnauthorized, w.Code)
	assert.Contains(t, w.Body.String(), "authorization header required")
}