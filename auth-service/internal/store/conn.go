package store

import (
	"database/sql"
	"fmt"
	"sync"
	"time"
)

var (
	instance *sql.DB
	once sync.Once
) 

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