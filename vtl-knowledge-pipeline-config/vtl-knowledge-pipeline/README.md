# VTL Knowledge Pipeline

Permission-aware data onboarding pipeline for Vanguard Transit & Logistics (VTL).

```bash
cp .env.example .env
make sync
make up
make test
```

See `config/` for tunables and ACL policy, and `docs/acl-design.md` for the group-inheritance decision.
