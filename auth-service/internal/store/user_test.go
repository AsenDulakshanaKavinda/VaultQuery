package store

import (
	"AuthService/internal/models"
	"database/sql"
	"errors"
	"testing"
	"time"

	"github.com/DATA-DOG/go-sqlmock"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestUserStore_CreateUser(t *testing.T) {
	db, mock, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	s := NewUserStore(db)

	now := time.Now().UTC().Format(time.RFC3339)
	u := &models.User{
		ID:           "user-123",
		Email:        "test@example.com",
		Name:         "John Doe",
		PasswordHash: "hashed_pass",
		Status:       "active",
		Role:         "user",
		Groups:       "group1",
		Title:        "Engineer",
		Location:     "New York",
		Organization: "Tech Corp",
		CreatedAt:    now,
	}

	// Expect the INSERT query and RETURNING clause, returning updated fields (CreatedAt, Status, Role, Groups)
	mock.ExpectQuery(`INSERT INTO users`).
		WithArgs(
			u.ID,
			u.Email,
			u.Name,
			u.PasswordHash,
			u.Status,
			u.Role,
			u.Groups,
			u.Title,
			u.Location,
			u.Organization,
			u.CreatedAt,
		).
		WillReturnRows(sqlmock.NewRows([]string{"created_at", "status", "role", "groups"}).
			AddRow(now, "active", "user", "group1"))

	err = s.CreateUser(u)
	assert.NoError(t, err)
	assert.NoError(t, mock.ExpectationsWereMet())
}

func TestUserStore_GetUserByEmail(t *testing.T) {
	db, mock, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	s := NewUserStore(db)
	now := time.Now()

	t.Run("Success", func(t *testing.T) {
		rows := sqlmock.NewRows([]string{
			"id", "email", "name", "password_hash", "status", "role", "groups", "title", "location", "organization", "created_at",
		}).AddRow(
			"user-123", "test@example.com", "John Doe", "hash", "active", "user", "group1", "Eng", "NY", "Corp", now,
		)

		mock.ExpectQuery(`SELECT .* FROM users WHERE email = \$1 AND status = 'active'`).
			WithArgs("test@example.com").
			WillReturnRows(rows)

		user, err := s.GetUserByEmail("test@example.com")
		assert.NoError(t, err)
		assert.NotNil(t, user)
		assert.Equal(t, "user-123", user.ID)
		assert.Equal(t, "test@example.com", user.Email)
		assert.NoError(t, mock.ExpectationsWereMet())
	})

	t.Run("NotFound", func(t *testing.T) {
		mock.ExpectQuery(`SELECT .* FROM users WHERE email = \$1 AND status = 'active'`).
			WithArgs("unknown@example.com").
			WillReturnError(sql.ErrNoRows)

		user, err := s.GetUserByEmail("unknown@example.com")
		assert.NoError(t, err)
		assert.Nil(t, user)
		assert.NoError(t, mock.ExpectationsWereMet())
	})
}

func TestUserStore_GetUserByID(t *testing.T) {
	db, mock, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	s := NewUserStore(db)
	now := time.Now()

	t.Run("Success", func(t *testing.T) {
		rows := sqlmock.NewRows([]string{
			"id", "email", "name", "password_hash", "status", "role", "groups", "title", "location", "organization", "created_at",
		}).AddRow(
			"user-123", "test@example.com", "John Doe", "hash", "active", "user", "group1", "Eng", "NY", "Corp", now,
		)

		mock.ExpectQuery(`SELECT .* FROM users WHERE id = \$1 AND status = 'active'`).
			WithArgs("user-123").
			WillReturnRows(rows)

		user, err := s.GetUserByID("user-123")
		assert.NoError(t, err)
		assert.NotNil(t, user)
		assert.Equal(t, "user-123", user.ID)
		assert.NoError(t, mock.ExpectationsWereMet())
	})

	t.Run("DatabaseError", func(t *testing.T) {
		mock.ExpectQuery(`SELECT .* FROM users WHERE id = \$1 AND status = 'active'`).
			WithArgs("user-123").
			WillReturnError(errors.New("connection reset"))

		user, err := s.GetUserByID("user-123")
		assert.Error(t, err)
		assert.Nil(t, user)
		assert.Contains(t, err.Error(), "failed to get user")
		assert.NoError(t, mock.ExpectationsWereMet())
	})
}

func TestUserStore_CreateRegisterRequest(t *testing.T) {
	db, mock, err := sqlmock.New()
	require.NoError(t, err)
	defer db.Close()

	s := NewUserStore(db)
	
	// Ensure 'now' is a string matching your model type
	now := time.Now().UTC().Format(time.RFC3339)

	req := &models.RegisterRequest{
		RequestID:      "req-1",
		Username:       "johndoe",
		Email:          "test@example.com",
		HashedPassword: "hash",
		Status:         "pending",
	}

	mock.ExpectQuery(`INSERT INTO register_request`).
		WithArgs(
			req.RequestID,
			req.Username,
			req.Email,
			req.HashedPassword,
			req.Status,
		).
		WillReturnRows(sqlmock.NewRows([]string{"requested_at", "updated_at"}).
			AddRow(now, now))

	err = s.CreateRegisterRequest(req)
	assert.NoError(t, err)
	assert.Equal(t, now, req.RequestedAt)
	assert.Equal(t, now, req.UpdatedAt)
	assert.NoError(t, mock.ExpectationsWereMet())
}