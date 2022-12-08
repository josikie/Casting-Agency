#!/bin/bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/castingagency"
export AUTH0_DOMAIN="fsnd-tenant.us.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="castingagency"
echo "script executed successfully"