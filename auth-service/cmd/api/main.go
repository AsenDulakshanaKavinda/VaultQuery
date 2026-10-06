package main

import (
	"AuthService/internal/handlers"
	"AuthService/internal/store"
	"log"
	"os"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Println("Warning: Error loading .env file, reading from environment")
	}

	connStr := os.Getenv("DATABASE_URL")
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
		AllowOrigins:     []string{"http://localhost:5174", "http://localhost:3000"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		AllowCredentials: true,
	}))

	// PUBLIC ROUTES (No Auth Middleware)
	publicRoutes := r.Group("/api/v1/auth")
	{
		publicRoutes.POST("/register", authHandler.Register)
		// publicRoutes.POST("/login", authHandler.Login)
	}

	// PROTECTED ROUTES (Requires Token)
	/*
	protectedRoutes := r.Group("/api/v1")
	protectedRoutes.Use(yourAuthMiddleware())
	{
		// protected endpoints here
	}
	*/

	log.Println("Server running on :8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to run server: %v", err)
	}
}