package handlers

import (
	"admin-service/internal/models"
	"admin-service/internal/store"
	"fmt"
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

// create register request 
func (h RegisterRequestHandler) CreateRegisterRequest(c *gin.Context) {
	var req models.RegisterRequestPayload

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}


	requestID := uuid.New().String()

	regReq := &store.RegisterRequest{
		RequestID:      requestID,
		Username:       req.Username,
		Email:          req.Email,
		HashedPassword: req.HashedPassword,
		Status:         "pending",
	}

	if err := h.adminStore.CreateRegisterRequest(regReq); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": fmt.Sprintf("failed to send register request: %v", err)})
		return
	}

	response, err := h.adminStore.GetRegisterRequestsByID(requestID)
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

// fetch all register request 
func (h RegisterRequestHandler) FetchAllRegisterRequest(c *gin.Context) {
	response, err := h.adminStore.GetAllRegisterRequests()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"message":  fmt.Sprintf("failed to fetch all register requests: %v", err),
			"response": nil,
			"count":    0,
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message":  "fetched all register request",
		"response": response,
		"count":    len(response),
	})
}



// fetch register request by id
func (h RegisterRequestHandler) FetchRegisterRequestByID(c *gin.Context) {
	id := c.Param("id")

	response, err := h.adminStore.GetRegisterRequestsByID(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"message":  fmt.Sprintf("failed to fetch register request by id: %v", err),
			"response": nil,
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message":  "fetched register request by id",
		"response": response,
	})
}


// fetch register request by status
func (h RegisterRequestHandler) FilterRegisterRequestStatus(c *gin.Context) {

	status := c.Query("status")
	if status == "" {
		c.JSON(http.StatusBadRequest, gin.H{
            "message":  "status query parameter is required",
            "response": nil,
            "count":    0,
        })
        return
	}

	response, err := h.adminStore.FilterRegisterRequestsByStatus(status)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"message":  fmt.Sprintf("failed to fetch register request by status: %v", err),
			"response": nil,
			"count":    0,
		})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"message":  "fetched register requests by status successfully",
		"response": response,
		"count":    len(response),
	})
}

type UpdateStatusInput struct {
	Status string `json:"status" binding:"required"`
}

// update register request
func (h RegisterRequestHandler) UpdateRegisterRequest(c *gin.Context) {

	id := c.Param("id")

	var input UpdateStatusInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"message":  "invalid request body",
			"response": nil,
		})
		return
	}

	response, err := h.adminStore.UpdateRegisterRequestByID(id, input.Status)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"message":  fmt.Sprintf("failed to update register request by id: %v", err),
			"response": nil,
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message":  "register request updated successfully",
		"response": response,
	})

}

type ApproveUser struct {
	Id string `json:"id" binding:"required"`
	Role string `json:"role" binding:"required"`
	Status string `json:"status" binding:"required"`
	Organization string `json:"organization" binding:"required"`

}

// update register request
// Define a clear input struct for the approval payload
type ApproveRequestInput struct {
    Role         string `json:"role" binding:"required"`
    Status       string `json:"status" binding:"required"`       // Status for the register request (e.g., "approved")
    UserStatus   string `json:"user_status" binding:"required"`  // Status for the new user profile (e.g., "active")
    Organization string `json:"organization" binding:"required"`
}

func (h RegisterRequestHandler) ApproveRegisterRequest(c *gin.Context) {
    // Get the request ID from the URL path parameter (e.g., /admin/approve/:id)
    id := c.Param("id")

    var input ApproveRequestInput
    if err := c.ShouldBindJSON(&input); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{
            "message":  "invalid request body",
            "error":    err.Error(),
            "response": nil,
        })
        return
    }

    request, err := h.adminStore.UpdateRegisterRequestByID(id, input.Status)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{
            "message":  fmt.Sprintf("failed to update register request by id: %v", err),
            "response": nil,
        })
        return
    }

    newUser := store.User{
        UserID:         uuid.New().String(),
        Username:       request.Username,
        Email:          request.Email, 
        Role:           input.Role,
        Status:         input.UserStatus,
        HashedPassword: request.HashedPassword,
        Organization:   input.Organization,
    }

    err = h.adminStore.CreateUser(&newUser)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{
            "message":  fmt.Sprintf("failed to approve the user: %v", err),
            "response": nil,
        })
        return
    }

    c.JSON(http.StatusOK, gin.H{
        "message":  "user approved and created successfully",
        "response": newUser,
    })
}