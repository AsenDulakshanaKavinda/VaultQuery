package handlers

import (
	"AuthService/internal/models"
	"AuthService/internal/services"
	"AuthService/internal/store"
	"net/http"
	"uuid"

	"github.com/gin-gonic/gin"
)

type AuthHandler struct {
	userStore *store.UserStore
}

func NewAuthHandler(userStore *store.UserStore) *AuthHandler {
	return &AuthHandler{userStore: userStore}
}

// Register handles user registration
func (h *AuthHandler) Register(c *gin.Context) {
	var req models.RegisterRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	hashedPassword, err := services.HashPassword(req.Password)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to process password"})
		return
	}

	user := &store.User{
		UserID:         uuid.New().String(),
		Username:       req.Username,
		Email:          req.Email,
		Role:           req.Role,
		HashedPassword: hashedPassword,
		Organization:   req.Organization,
	}

	if err := h.userStore.CreateUser(user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to register user"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"message": "user registered successfully",
		"user": models.UserResponse{
			UserID:       user.UserID,
			Username:     user.Username,
			Role:         user.Role,
			Organization: user.Organization,
			Status:       user.Status,
			CreatedAt:    user.CreatedAt,
		},
	})

}

// Login verifies user credentials and returns a JWT token
func (h *AuthHandler) Login(c *gin.Context) {
	var req models.LoginRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid username or password format"})
		return
	}

	user, err := h.userStore.GetUserByEmail(req.Email)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database error"})
		return
	}
	if user == nil {
		// return generic error to prevent user enumeration attacks
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid username or password"})
		return
	}

	if !(services.CheckPasswordHash(req.Password, user.HashedPassword)) {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid username or password"})
		return
	}

	token, expiresIn, err := services.GenerateToken(user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to generate authentication token"})
		return
	}

	c.JSON(http.StatusOK, models.TokenResponse{
		AccessToken: token,
		TokenType:   "Bearer",
		ExpiresIn:   expiresIn,
	})

}
