package pkg

import (
	"github.com/gin-gonic/gin"

)

func ErrorBody(code, message string) gin.H {
	return gin.H{
		"code": code, 
		"message": message,
	}
}
	