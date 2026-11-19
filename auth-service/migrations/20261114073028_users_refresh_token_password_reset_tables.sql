-- +goose Up
DROP TABLE users;
CREATE TABLE users (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email         text UNIQUE NOT NULL,
  name          text NOT NULL,
  password_hash text,                       -- null for SSO-only users
  status        text NOT NULL DEFAULT 'pending',  -- pending | active | disabled
  role          text NOT NULL DEFAULT 'employee', -- employee | admin
  groups        text[] NOT NULL DEFAULT '{}',     -- e.g. grp_account_managers
  title text, 
  location text,
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE refresh_tokens (
  id          uuid PRIMARY KEY,
  user_id     uuid NOT NULL REFERENCES users(id),
  family_id   uuid NOT NULL,                -- for reuse detection
  token_hash  bytea NOT NULL UNIQUE,        -- SHA-256 of the opaque token
  expires_at  timestamptz NOT NULL,
  revoked_at  timestamptz,
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE password_resets (
  token_hash bytea PRIMARY KEY, 
  user_id uuid NOT NULL REFERENCES users(id),
  expires_at timestamptz NOT NULL, 
  used_at timestamptz
);

-- +goose Down
DROP TABLE users;
DROP TABLE refresh_tokens;
DROP TABLE password_resets;
