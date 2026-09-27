# Database

The MySQL 8 schema is in `database/schema.sql`. Create the `agrivision_x` database in your MySQL server and apply that file manually. It defines users, fields, analyses, and alerts with ownership/field foreign keys and lookup indexes. `database/seed.sql` is intentionally empty to avoid inventing users or farm measurements.

Configure `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` in `server/.env`. Keep real credentials out of version control. Add migrations before making schema changes in shared environments.
