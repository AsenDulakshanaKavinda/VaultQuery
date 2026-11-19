package handlers

import (
	"AuthService/internal/models"
	"AuthService/internal/services"
	"AuthService/internal/store"
	"fmt"
	"net/http"
	"strings"

	"github.com/google/uuid"

	"github.com/gin-gonic/gin"
)

type AuthHandler struct {
	userStore *store.UserStore
}

func NewAuthHandler(userStore *store.UserStore) *AuthHandler {
	return &AuthHandler{userStore: userStore}
}

// / create register request
// / get username, email and password and create a  user register request
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

	regReq := &models.RegisterRequest{
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

	c.JSON(http.StatusCreated, gin.H{
		"message": "user register request sent successfully",
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
		fmt.Println(err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database error"})
		return
	}
	if user == nil {
		// return generic error to prevent user enumeration attacks
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid username or password"})
		return
	}

	if !(services.CheckPasswordHash(req.Password, user.PasswordHash)) {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid username or password"})
		return
	}

	token, expiresIn, err := services.GenerateToken(user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to generate authentication token"})
		return
	}

	refreshToken, _, err := services.GenerateRefreshToken(user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to generate refresh token"})
		return
	}

	fmt.Printf("id: %s, name: %s, email: %s, role: %s \n", user.ID, user.Name, user.Email, user.Role)

	c.JSON(http.StatusOK, models.TokenResponse{
		AccessToken:  token,
		RefreshToken: refreshToken,
		TokenType:    "Bearer",
		ExpiresIn:    expiresIn,
		User:         models.ToUserResponse(user),
	})
}

// GetMe returns the currently authenticated user's details
func (h *AuthHandler) GetMe(c *gin.Context) {
	// get id set by AuthMiddleware
	userIDVal, exists := c.Get("id")
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

	fmt.Printf("id: %s, name: %s, email: %s, role: %s \n", user.ID, user.Name, user.Email, user.Role)

	// return user profile
	c.JSON(http.StatusOK, gin.H{
		"user": models.ToUserResponse(user),
	})
}

func (h *AuthHandler) PasswordForgot(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "PasswordForgot",
	})
}

func (h *AuthHandler) PasswordReset(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "PasswordReset",
	})
}

func (h *AuthHandler) Logout(c *gin.Context) {
	authHeader := c.GetHeader("Authorization")
	if authHeader == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "authorization header required"})
		return
	}

	parts := strings.Split(authHeader, " ")
	if len(parts) != 2 || parts[0] != "Bearer" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid authorization header format"})
		return
	}

	// tokenString := parts[1]

	// TODO: Add tokenString to your Redis/DB blacklist store
	// err := h.userStore.BlacklistToken(tokenString)
	// if err != nil { ... }

	c.JSON(http.StatusOK, gin.H{
		"message": "logged out successfully",
	})
}

type RefreshTokenRequest struct {
	RefreshToken string `json:"refresh_token" binding:"required"`
}

func (h *AuthHandler) RefreshToken(c *gin.Context) {
	var req RefreshTokenRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "invalid request payload",
		})
		return
	}

	claims, err := services.ValidateRefreshToken(req.RefreshToken)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error": "invalid or expired refresh token",
		})
		return
	}

	user, err := h.userStore.GetUserByID(claims.UserID)
	if err != nil || user == nil {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error": "user no longer exists",
			"id":    claims.UserID,
		})
		return
	}

	accessToken, expiresIn, err := services.GenerateToken(user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "failed to generate new authentication token",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"id":           user.ID,
		"access_token": accessToken,
		"token_type":   "Bearer",
		"expires_in":   expiresIn,
	})

}

func (h *AuthHandler) Verify(c *gin.Context) {
	userIDVal, exists := c.Get("id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
		return
	}

	roleVal, _ := c.Get("role")
	// emailVal, _ := c.Get("claims")

	c.JSON(http.StatusOK, gin.H{
		"status": "valid",
		"id":     userIDVal,
		"role":   roleVal,
	})

	c.JSON(http.StatusOK, gin.H{
		"message": "Verify",
	})
}
