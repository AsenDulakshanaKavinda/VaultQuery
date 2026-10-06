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
