# ==========================================
# Stage 1: Build the Go binary
# ==========================================
FROM golang:alpine AS builder

WORKDIR /app

# Install git and certificates if needed
RUN apk add --no-cache git

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build a statically linked Go binary
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/auth-api cmd/api/main.go

# ==========================================
# Stage 2: Run the binary in a minimal image
# ==========================================
FROM alpine:latest

WORKDIR /app

# Install CA certificates for HTTPS/TLS requests if any
RUN apk add --no-cache ca-certificates tzdata

# Copy the compiled binary from the builder stage
COPY --from=builder /app/auth-api /app/auth-api

# Copy configuration files (required for config.LoadConfig())
COPY --from=builder /app/config /app/config

# Expose the application port
EXPOSE 8080

# Run the binary
CMD ["/app/auth-api"]



