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
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Printf("Warning: %v\n", err)
	}

	settings := config.LoadSettings()

	if err != nil {
		log.Println("Warning: Error loading .env file, reading from environment")
	}

	connStr := settings.DatabaseURL
	dbInstance, err := store.GetDB(connStr)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer dbInstance.Close()

	userStore := store.NewUserStore(dbInstance)
	authHandler := handlers.NewAuthHandler(userStore)

	r := gin.Default()

	// Enable CORS for React frontend (Vite port 5173 / CRA port 3000)
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:5173", "http://localhost:3000"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		AllowCredentials: true,
	}))

	// PUBLIC ROUTES (No Auth Middleware)
	publicRoutes := r.Group("/api/v1/auth")
	{
		publicRoutes.POST("/register", authHandler.Register)
		publicRoutes.POST("/login", authHandler.Login)
		publicRoutes.POST("/create-user-register-req", authHandler.CreateRegisterRequest)
	}

	// PROTECTED ROUTES (Requires Token)
	
	protectedRoutes := r.Group("/api/v1/auth")
	protectedRoutes.Use(middleware.AuthMiddleware())
	{
		// protected endpoints here
		protectedRoutes.GET("/me", authHandler.GetMe)

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
	

	log.Printf("%s running on :8080\n", cfg.App)
	fmt.Println(cfg.App)
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to run server: %v", err)
	}
}