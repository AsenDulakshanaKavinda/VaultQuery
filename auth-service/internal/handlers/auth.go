package handlers

import (
	"AuthService/internal/models"
	"AuthService/internal/services"
	"AuthService/internal/store"
	"fmt"
	"net/http"

	"github.com/google/uuid"

	"github.com/gin-gonic/gin"
)

type AuthHandler struct {
	userStore *store.UserStore
}

func NewAuthHandler(userStore *store.UserStore) *AuthHandler {
	return &AuthHandler{userStore: userStore}
}

// create register request
func (h AuthHandler) CreateRegisterRequest(c *gin.Context) {
	var req models.RegisterRequestPayload

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	hashedPassword, err := services.HashPassword(req.Password)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to process password"})
		return
	}

	requestID := uuid.New().String()

	regReq := &store.RegisterRequest{
		RequestID:      requestID,
		Username:       req.Username,
		Email:          req.Email,
		HashedPassword: hashedPassword,
		Status:         "pending",
	}

	if err := h.userStore.CreateRegisterRequest(regReq); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": fmt.Sprintf("failed to send register request: %v", err)})
		return
	}

	response, err := h.userStore.GetRegisterRequestsByID(requestID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"message":  fmt.Sprintf("failed to create user register request: %v", err),
			"response": nil,
		})
	}

	c.JSON(http.StatusCreated, gin.H{
		"message":  "user register request sent successfully",
		"response": response,
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

	fmt.Printf("id: %s, name: %s, email: %s, role: %s \n", user.UserID, user.Username, user.Email, user.Role)

	c.JSON(http.StatusOK, models.TokenResponse{
		AccessToken: token,
		TokenType:   "Bearer",
		ExpiresIn:   expiresIn,
		User:        models.ToUserResponse(user),
	})

}

// GetMe returns the currently authenticated user's details
func (h *AuthHandler) GetMe(c *gin.Context) {
	// get user_id set by AuthMiddleware
	userIDVal, exists := c.Get("user_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
		return
	}

	// fetch fresh user data from DB
	userID, ok := userIDVal.(string)
	if !ok {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "invalid user ID type in context"})
		return
	}

	user, err := h.userStore.GetUserByID(userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to fetch user details"})
		return
	}
	if user == nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
		return
	}

	fmt.Printf("id: %s, name: %s, email: %s, role: %s \n", user.UserID, user.Username, user.Email, user.Role)

	// return user profile
	c.JSON(http.StatusOK, gin.H{
		"user": models.ToUserResponse(user),
	})
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
		HashedPassword: hashedPassword,
		// this should be
		Role:         req.Role,
		Organization: req.Organization,
	}

	if err := h.userStore.CreateUser(user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to register user"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"message": "user registered successfully",
		"user":    models.ToUserResponse(user),
	})

}
