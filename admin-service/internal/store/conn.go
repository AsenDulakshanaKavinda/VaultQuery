package store

import (
	"database/sql"
	"fmt"
	"sync"
	"time"
)

// This package provides a singleton database connection to a PostgreSQL database using the provided connection string.
// It ensures that only one instance of the database connection is created and reused throughout the application.
var (
	instance *sql.DB
	once     sync.Once
)

// GetDB establishes a connection to the PostgreSQL database using the provided connection string.
func GetDB(connStr string) (*sql.DB, error) {
	var err error

	once.Do(func() {
		instance, err = sql.Open("postgres", connStr)
		if err != nil {
			return
		}

		// Configure connection pool settings
		instance.SetMaxOpenConns(25)
		instance.SetMaxIdleConns(25)
		instance.SetConnMaxLifetime(5 * time.Minute)

		// Verify connection
		err = instance.Ping()
	})

	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}

	return instance, nil

}
