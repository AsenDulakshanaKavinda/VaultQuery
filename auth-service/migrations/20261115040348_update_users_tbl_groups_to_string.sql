-- +goose Up
ALTER TABLE users ALTER COLUMN groups TYPE TEXT USING groups::text;

-- +goose Down
ALTER TABLE users ALTER COLUMN groups TYPE TEXT[] USING groups::text[];