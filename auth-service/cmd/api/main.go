package main

import (
	"database/sql"
	"fmt"
	"log"

	"AuthService/internal/config"
	"AuthService/internal/handlers"
	"AuthService/internal/middleware"
	"AuthService/internal/store"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

// SetupRouter initializes dependencies, middleware, and routes, returning the Gin engine.
func SetupRouter(db *sql.DB) *gin.Engine {
	userStore := store.NewUserStore(db)
	authHandler := handlers.NewAuthHandler(userStore)

	r := gin.Default()

	// Enable CORS
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:5173", "http://localhost:3000"},
		AllowMethods:     []string{"GET", "POST", "PUT"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		AllowCredentials: true,
	}))

	// PUBLIC ROUTES
	publicRoutes := r.Group("/api/v1")
	{
		publicRoutes.POST("/auth/login", authHandler.Login)
		publicRoutes.POST("/auth/request-access", authHandler.CreateRegisterRequest)
		publicRoutes.POST("/auth/password/forgot", authHandler.PasswordForgot)
		publicRoutes.POST("/auth/password/reset", authHandler.PasswordReset)
	}

	// PROTECTED ROUTES
	protectedRoutes := r.Group("/api/v1")
	protectedRoutes.Use(middleware.AuthMiddleware())
	{
		protectedRoutes.GET("/auth/me", authHandler.GetMe)
		protectedRoutes.POST("/auth/logout", authHandler.Logout)
		protectedRoutes.POST("/auth/verify", authHandler.Verify)
		protectedRoutes.POST("/auth/refresh", authHandler.RefreshToken)
	}

	return r
}

func main() {
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	settings, err := config.LoadSettings()
	if err != nil {
		log.Printf("Warning: %v\n", err)
	}

	dbInstance, err := store.GetDB(settings.DatabaseURL)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer dbInstance.Close()

	r := SetupRouter(dbInstance)

	fmt.Println("==========================================")
	fmt.Println("<<< Hello, Welcome to the Auth-Service >>>")
	fmt.Println("==========================================")
	fmt.Printf("%s Running on :%s\n", cfg.App, settings.Port)

	if err := r.Run(fmt.Sprintf(":%s", settings.Port)); err != nil {
		log.Fatalf("Failed to run Auth-Service: %v", err)
	}
}