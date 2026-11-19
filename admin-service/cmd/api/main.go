package main

import (
	"admin-service/internal/config"
	"admin-service/internal/handlers"
	"admin-service/internal/store"
	"database/sql"
	"fmt"
	"log"
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"

	_ "github.com/lib/pq"
)

// todo is a placeholder handler. Replace each call with the real handler,
// e.g. todo("dataSources.list") -> dataSourceHandler.List
func todo(name string) gin.HandlerFunc {
	return func(c *gin.Context) {
		c.JSON(http.StatusNotImplemented, gin.H{
			"code":    "NOT_IMPLEMENTED",
			"message": name + " is not implemented yet",
		})
	}
}

func AdminRouter(db *sql.DB) *gin.Engine {
	adminStore := store.NewAdminStore(db)
	registerRequestHandler := handlers.NewRegisterRequestHandler(adminStore)

	r := gin.Default()

	// Enable CORS
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:5173", "http://localhost:3000"},
		AllowMethods:     []string{"GET", "POST", "PUT"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		AllowCredentials: true,
	}))

	adminRoutes := r.Group("/api/v1/admin")
	{
		adminRoutes.POST("/create-user-register-req", registerRequestHandler.CreateRegisterRequest)
		adminRoutes.PUT("/register-requests-update/:id", registerRequestHandler.UpdateRegisterRequest)

		// fetch all register request endpoint
		adminRoutes.GET("/fetch-all-user-register-req", registerRequestHandler.FetchAllRegisterRequest)

		// fetch register request by id endpoint
		adminRoutes.GET("/fetch-user-register-req-id/:id", registerRequestHandler.FetchRegisterRequestByID)

		// fetch register request by status endpoint
		adminRoutes.GET("/register-requests", registerRequestHandler.FilterRegisterRequestStatus)

		// approve register request endpoint
		adminRoutes.PUT("/register-requests/:id/approve", registerRequestHandler.ApproveRegisterRequest)

	}

	// ---- data onboarding endpoints ----

	// Data sources (connectors): Data sources page + Configure drawer
	dataSourceRoutes := adminRoutes.Group("/data-sources")
	{
		dataSourceRoutes.GET("", todo("dataSources.list"))
		dataSourceRoutes.POST("", todo("dataSources.create"))
		dataSourceRoutes.GET("/:id/config", todo("dataSources.getConfig"))
		dataSourceRoutes.PUT("/:id/config", todo("dataSources.updateConfig"))
		dataSourceRoutes.POST("/:id/sync", todo("dataSources.sync"))
		dataSourceRoutes.POST("/:id/pause", todo("dataSources.pause"))
		dataSourceRoutes.POST("/:id/resume", todo("dataSources.resume"))
		dataSourceRoutes.POST("/:id/reauthorize", todo("dataSources.reauthorize"))
	}

	// Ingestion runs: table + run detail drawer
	ingestionRoutes := adminRoutes.Group("/ingestion-runs")
	{
		ingestionRoutes.GET("", todo("ingestion.list")) // ?source=&status=&mode=&from=&to=&page=
		ingestionRoutes.GET("/export", todo("ingestion.export")) // CSV
		ingestionRoutes.GET("/:id", todo("ingestion.get")) // stage timeline + failed documents
		ingestionRoutes.POST("/:id/retry", todo("ingestion.retry"))
	}

	// Connected-source summary (shown on Access management)
	connectorRoutes := adminRoutes.Group("/connectors")
	{
		connectorRoutes.GET("", todo("connectors.list"))
	}

	// ---- ACL Update ----

	// Policy version + history
	policyRoutes := adminRoutes.Group("/policy")
	{
		policyRoutes.GET("", todo("policy.current")) // {version, mode}
		policyRoutes.GET("/history", todo("policy.history"))
	}

	// ACL rules: ordered list, add/edit drawer, test a location
	aclRuleRoutes := adminRoutes.Group("/acl-rules")
	{
		aclRuleRoutes.GET("", todo("aclRules.list"))
		aclRuleRoutes.POST("", todo("aclRules.create")) // create + publish, bumps policy version
		aclRuleRoutes.PUT("/order", todo("aclRules.reorder")) // {ids: [...]}
		aclRuleRoutes.POST("/test", todo("aclRules.test")) // {source, path}, no side effects
		aclRuleRoutes.PUT("/:id", todo("aclRules.update"))
	}

	// Access matrix: Explicit vs Inherit preview, apply
	matrixRoutes := adminRoutes.Group("/access-matrix")
	{
		matrixRoutes.GET("", todo("accessMatrix.get"))
		matrixRoutes.GET("/export", todo("accessMatrix.export")) // CSV
		matrixRoutes.POST("/preview", todo("accessMatrix.preview")) // {mode: "Inherit"} -> proposed changes
		matrixRoutes.POST("/apply", todo("accessMatrix.apply"))
	}

	// Quarantine queue (unmatched locations)
	quarantineRoutes := adminRoutes.Group("/quarantine")
	{
		quarantineRoutes.GET("", todo("quarantine.list")) // ?source=&order=
		quarantineRoutes.POST("/:id/ignore", todo("quarantine.ignore"))
		// "Create rule from this" reuses POST /api/v1/admin/acl-rules
	}

	// View As (access simulator)
	viewAsRoutes := adminRoutes.Group("/view-as")
	{
		viewAsRoutes.POST("/simulate", todo("viewAs.simulate")) // {roleId, question}
	}

	// Access management: employee group mappings + platform administrators
	accessMgmtRoutes := adminRoutes.Group("/access-management")
	{
		accessMgmtRoutes.GET("/groups", todo("accessMgmt.listGroups"))
		accessMgmtRoutes.PUT("/groups", todo("accessMgmt.updateGroupMappings"))
		accessMgmtRoutes.GET("/administrators", todo("accessMgmt.listAdmins"))
		accessMgmtRoutes.PUT("/administrators", todo("accessMgmt.updateAdmins"))
	}

	// ---- Dashboard ----

	// Overview page: KPIs, charts, "needs attention"
	overviewRoutes := adminRoutes.Group("/overview")
	{
		overviewRoutes.GET("", todo("dashboard.overview")) // ?range=7d
	}

	// Audit log (read-only): table, filters, event drawer
	auditRoutes := adminRoutes.Group("/audit-events")
	{
		auditRoutes.GET("", todo("audit.list")) // ?from=&to=&user=&type=&role=&page=
		auditRoutes.GET("/export", todo("audit.export")) // CSV
		auditRoutes.GET("/:id", todo("audit.get"))
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

	r := AdminRouter(dbInstance)

	fmt.Println("==========================================")
	fmt.Println("<<<   Welcome to the Admin-Service    >>>")
	fmt.Println("==========================================")
	fmt.Printf("%s Running on :%s\n", cfg.App, settings.Port)

	if err := r.Run(fmt.Sprintf(":%s", settings.Port)); err != nil {
		log.Fatalf("Failed to run Admin-Service: %v", err)
	}
}