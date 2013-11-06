#!/bin/sh
R < fakeDataGen.R --vanilla
sqlite3 sample_repo.db < schema.sql

