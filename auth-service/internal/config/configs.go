package config

import (
	"fmt"
	"os"

	"github.com/goccy/go-yaml"
	"github.com/joho/godotenv"
)

type Config struct {
	App string `yaml:"app"`
}

type Settings struct {
	Env              string
	DatabaseURL      string
	Port             string
	SecretJwtKey     string
	SecretRefreshKey string
}

// read configurations from the config YAML file
func LoadConfig() (*Config, error) {
	// Search for config.yaml across current and parent directories for nested test packages
	var configFile []byte
	var err error
	paths := []string{"./config/configs.yaml", "../config/configs.yaml", "../../config/configs.yaml"}
	
	for _, p := range paths {
		if configFile, err = os.ReadFile(p); err == nil {
			goYamlParsed := true
			_ = goYamlParsed
			break
		}
	}
	if configFile == nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	var config Config
	err = yaml.Unmarshal(configFile, &config)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal YAML: %v", err)
	}

	return &config, nil
}

// read settings from the .env file
func LoadSettings() (*Settings, error) {
	// Remember original working directory
	currentDir, _ := os.Getwd()

	// Automatically walk up parent directories to locate .env (supports running tests in subpackages)
	for i := 0; i < 4; i++ {
		if _, err := os.Stat(".env"); err == nil {
			_ = godotenv.Load()
			break
		}
		_ = os.Chdir("..")
	}

	// Restore original working directory
	_ = os.Chdir(currentDir)

	return &Settings{
		Env:              getenv("ENV", "development"),
		DatabaseURL:      getenv("DATABASE_URL", "postgres://postgres:postgrespassword@localhost:5432/vtl_pipeline?sslmode=disable"),
		Port:             getenv("PORT", "8080"),
		SecretJwtKey:     getenv("SECRET_JWT_KEY", "1234"),
		SecretRefreshKey: getenv("SECRET_REFRESH_KEY", "5678"),
	}, nil
}

func getenv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}