FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
  git \
  postgresql-client \
  curl \
  && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dbt
RUN pip install --no-cache-dir \
  dbt-core \
  dbt-postgres \
  dbt-bigquery 
# Create non-root user
RUN useradd -ms /bin/bash vscode
USER vscode
WORKDIR /home/vscode

# Configure dbt profiles directory
RUN mkdir -p /home/vscode/.dbt

# Create a basic profiles.yml template
RUN echo "default:\n\
  target: dev\n\
  outputs:\n\
  dev:\n\
  type: postgres\n\
  host: localhost\n\
  user: dbt_user\n\
  password: dbt_password\n\
  port: 5432\n\
  dbname: dbt\n\
  schema: dbt_schema\n\
  threads: 4" > /home/vscode/.dbt/profiles.yml

# Add dbt to PATH
ENV PATH="/home/vscode/.local/bin:${PATH}"
