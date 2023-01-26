[Environment]::SetEnvironmentVariable('IE_D_DB_HOST','')
[Environment]::SetEnvironmentVariable('IE_D_DB_PORT','5432')
[Environment]::SetEnvironmentVariable('IE_D_DB_DBNAME','')
[Environment]::SetEnvironmentVariable('IE_D_DB_USER','')
[Environment]::SetEnvironmentVariable('IE_D_DB_PASSWORD','')

alembic revision --autogenerate