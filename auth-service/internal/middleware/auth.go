package middleware

import (
	"AuthService/internal/services"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "authorization header required"})
			c.Abort()
			return 
		}

		// Header format: "Bearer <token>"
		parts := strings.Split(authHeader, " ")
		if len(parts) != 2 || parts[0] != "Bearer" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid authorization header format"})
			c.Abort()
			return
		}

		// Parse and validate token
		claims, err := services.ValidateToken(parts[1])
		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid or expired token"})
			c.Abort()
			return
		}

		// Store user claims in context for downstream handlers
		c.Set("user_id", claims.UserID)
		c.Set("role", claims.Role)
		c.Set("claims", claims)

		c.Next()
	}
}


// RequireRole restricts access to users who possess at least one of the allowed roles.
func RequireRole(allowedRoles ...string) gin.HandlerFunc {
	return func(c *gin.Context) {
		// get role set by AuthMiddleware
		roleInterface, exists := c.Get("role")
		if !exists {
			c.JSON(http.StatusForbidden, gin.H{"error": "role information missing"})
			c.Abort()
			return
		}

		userRole, ok := roleInterface.(string)
		if !ok {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "invalid role context type"})
			c.Abort()
			return
		}

		// check if user's role matches any allowed role
		for _, allowed := range allowedRoles {
			if userRole == allowed {
				c.Next()
				return
			}
		}

		// User does not have the required permission
		c.JSON(http.StatusForbidden, gin.H{"error": "access denied: insufficient permissions"})
		c.Abort()
	}
}
