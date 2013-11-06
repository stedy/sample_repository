#!/bin/sh
R < fakeDataGen.R --vanilla
sqlite3 sample_repo.db < schema.sql
python mksql/schema_demo.py
python mksql/schema_movement.py
