-- +goose Up
-- SQL in this section is executed when the migration is applied.
ALTER TABLE users 
ADD COLUMN status VARCHAR(10) NOT NULL DEFAULT 'active' 
CHECK (status IN ('active', 'inactive'));

-- +goose Down
-- SQL in this section is executed when the migration is rolled back.
ALTER TABLE users 
DROP COLUMN status;