package handlers

import (
	"admin-service/internal/models"
	"admin-service/internal/services"
	"admin-service/internal/store"
	"net/http"
	"uuid"

	"github.com/gin-gonic/gin"
)

type RegisterRequestHandler struct {
	adminStore *store.AdminStore
}

func NewRegisterRequestHandler(adminStore *store.AdminStore) *RegisterRequestHandler {
	return &RegisterRequestHandler{adminStore: adminStore}
}

// fetch all the register request
func (h RegisterRequestHandler) FetchAllRegisterRequest(c *gin.Context) {
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
		UserName:       req.Username,
		Email:          req.Email,
		HashedPassword: hashedPassword,
		Status:         "pending",
	}

	if err := h.adminStore.CreateRegisterRequest(regReq); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to send register request"})
		return
	}

	response, err := h.adminStore.GetRegisterRequestsByID(requestID)
	if err != nil {
		c.JSON(http.StatusCreated, gin.H{
			"message":  "user registered successfully",
			"response": nil,
		})
	}

	c.JSON(http.StatusCreated, gin.H{
		"message":  "user register request sent successfully",
		"response": models.ToRegisterRequestResponse(response),
	})

}
