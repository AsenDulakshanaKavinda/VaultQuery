package config

import (
	"fmt"
	"os"

	"github.com/goccy/go-yaml"
)

type Config struct {
	App string `yaml:"app"`
}

type Settings struct {
	Env         string
	DatabaseURL string
	Port        string
}

func LoadConfig() (*Config, error) {
	configFile, err := os.ReadFile("./config/configs.yaml")
	if err != nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	var config Config

	err = yaml.Unmarshal(configFile, &config)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal YAML: %v", err)

	}

	return &config, nil
}

func LoadSettings() *Settings {
	return &Settings{
		Env:         getenv("ENV", "development"),
		DatabaseURL: getenv("DATABASE_URL", "postgres://postgres:postgrespassword@localhost:5432/vtl_pipeline?sslmode=disable"),
		Port:        getenv("PORT", "8080"),
	}
}

func getenv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
