package main

import (
	"admin-service/internal/config"
	"admin-service/internal/handlers"
	"admin-service/internal/store"
	"log"

	"github.com/gin-gonic/gin"

	_ "github.com/lib/pq"
)


func main()  {

	cfg, err := config.LoadConfig()

	if err != nil {
		log.Printf("Warning: %v\n", err)
	}

	settings := config.LoadSettings()

	connStr := settings.DatabaseURL
	dbInstance, err := store.GetDB(connStr)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer dbInstance.Close()

	adminStore := store.NewAdminStore(dbInstance)
	registerRequestHandler := handlers.NewRegisterRequestHandler(adminStore)


	r := gin.Default()

	

	adminRoutes := r.Group("/api/v1/admin")
	{
		adminRoutes.POST("/create-user-register-req", registerRequestHandler.CreateRegisterRequest)
		adminRoutes.GET("/fetch-all-user-register-req", registerRequestHandler.FetchAllRegisterRequest)
		adminRoutes.GET("/fetch-user-register-req-id/:id", registerRequestHandler.FetchRegisterRequestByID)
		adminRoutes.GET("/register-requests", registerRequestHandler.FilterRegisterRequestStatus)
		adminRoutes.PUT("/register-requests/:id", registerRequestHandler.UpdateRegisterRequest)
	}


	log.Printf("%s running on :8085\n", cfg.App)
	if err := r.Run(":8085"); err != nil {
		log.Fatalf("Failed to run server: %v", err)
	}
}