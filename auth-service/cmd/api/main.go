package main

import (
	"AuthService/internal/config"
	"AuthService/internal/handlers"
	"AuthService/internal/middleware"
	"AuthService/internal/store"

	"fmt"
	"log"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

func main() {
	var err error
	// read configurations from the config YAML file and env variables from .env file
	cfg, err := config.LoadConfig()
	settings, err := config.LoadSettings()
	if err != nil {
		log.Printf("Warning: %v\n", err)
	}

	// read conn str from settings and create a db instance
	connStr := settings.DatabaseURL
	dbInstance, err := store.GetDB(connStr)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer dbInstance.Close()

	// create the database
	userStore := store.NewUserStore(dbInstance)

	// create the auth handler
	authHandler := handlers.NewAuthHandler(userStore)

	r := gin.Default()

	// Enable CORS for React frontend (Vite port 5173 / CRA port 3000)
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:5173", "http://localhost:3000"},
		AllowMethods:     []string{"GET", "POST", "PUT"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		AllowCredentials: true,
	}))

	// PUBLIC ROUTES (No Auth Middleware)
	publicRoutes := r.Group("/api/v1")
	{
		publicRoutes.POST("/auth/login", authHandler.Login)
		publicRoutes.POST("/auth/request-access", authHandler.CreateRegisterRequest)
		publicRoutes.POST("/auth/password/forgot", authHandler.PasswordForgot)
		publicRoutes.POST("/auth/password/reset", authHandler.PasswordReset)
	}

	// PROTECTED ROUTES (Requires Token)
	protectedRoutes := r.Group("/api/v1/")
	protectedRoutes.Use(middleware.AuthMiddleware())
	{
		protectedRoutes.GET("/auth/me", authHandler.GetMe)
		protectedRoutes.POST("/auth/logout", authHandler.Logout)
		protectedRoutes.POST("/auth/verify", authHandler.Verify)
		protectedRoutes.POST("/auth/refresh", authHandler.RefreshToken)

		
		// role base example
		// Admin-only route group
		/*
			adminRoutes := api.Group("/admin")
			adminRoutes.Use(middleware.RequireRole("admin"))
			{
				adminRoutes.GET("/users", func(c *gin.Context) {
					c.JSON(http.StatusOK, gin.H{"message": "List of all users"})
				})
				adminRoutes.DELETE("/users/:id", func(c *gin.Context) {
					c.JSON(http.StatusOK, gin.H{"message": "User deleted"})
				})
			}

			// Route accessible by multiple roles (e.g., admin or manager)
			api.GET("/reports", middleware.RequireRole("admin", "manager"), func(c *gin.Context) {
				c.JSON(http.StatusOK, gin.H{"message": "Manager/Admin analytics report"})
			})
		*/
	}

	// start the auth service API
	fmt.Println("==========================================")
	fmt.Println("<<< Hello, Welcome to the Auth-Service >>>")
	fmt.Println("==========================================")
	fmt.Printf("%s Running on :%s\n", cfg.App, settings.Port)
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to run Auth-Service: %v", err)
	}
}
