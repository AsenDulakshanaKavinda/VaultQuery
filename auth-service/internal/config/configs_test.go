package config

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestLoadSettings_Defaults(t *testing.T) {
	// Temporarily clear environment variables to test fallback default values
	t.Setenv("ENV", "")
	t.Setenv("PORT", "")
	t.Setenv("SECRET_JWT_KEY", "")
	t.Setenv("SECRET_REFRESH_KEY", "")

	settings, err := LoadSettings()
	require.NoError(t, err)
	assert.NotNil(t, settings)
	
	assert.Equal(t, "development", settings.Env)
	assert.Equal(t, "8080", settings.Port)
	assert.Equal(t, "1234", settings.SecretJwtKey)
	assert.Equal(t, "5678", settings.SecretRefreshKey)
}

func TestLoadSettings_CustomEnv(t *testing.T) {
	// Set custom environment variables using t.Setenv (thread-safe and auto-cleanup)
	t.Setenv("ENV", "production")
	t.Setenv("PORT", "9000")
	t.Setenv("SECRET_JWT_KEY", "custom-jwt-secret-key")
	t.Setenv("SECRET_REFRESH_KEY", "custom-refresh-secret-key")

	settings, err := LoadSettings()
	require.NoError(t, err)
	assert.NotNil(t, settings)
	
	assert.Equal(t, "production", settings.Env)
	assert.Equal(t, "9000", settings.Port)
	assert.Equal(t, "custom-jwt-secret-key", settings.SecretJwtKey)
	assert.Equal(t, "custom-refresh-secret-key", settings.SecretRefreshKey)
}

func TestLoadConfig(t *testing.T) {
	// Test loading configs.yaml using the parent-directory path walker
	cfg, err := LoadConfig()
	
	// If configs.yaml exists in the project root, it should load successfully
	if err == nil {
		assert.NotNil(t, cfg)
		assert.NotEmpty(t, cfg.App)
	} else {
		// If running in isolation where configs.yaml cannot be reached, it should return a wrapped error
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "failed to read config file")
	}
}