package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)


func main() {
	r := gin.Default()

	// public routes
	r.POST("/login", func(ctx *gin.Context) {
		token, err := GenerateToken()
		if err != nil {
			ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to generate token"})
		}
		ctx.JSON(http.StatusOK, gin.H{"token": token})
	})

	r.POST("/register", func(ctx *gin.Context) {
		// add user to database 
	})
}