# GitHub CI/CD Workflow Documentation

## Overview

This document describes the GitHub Actions CI/CD workflow for the DBT (Data Build Tool) project. The workflow automates the build, test, and deployment process for DBT models using BigQuery as the data warehouse.

## Workflow Diagram

``git s`mermaid
flowchart TD
    A[Push to main / PR opened/synchronized] --> B[Checkout Code]
    B --> C[Setup Python 3.12]
    C --> D[Setup BigQuery Credentials]
    D --> E[Calculate Dataset Name]
    E --> F[Install UV Package Manager]
    F --> G[Download Previous Run Artifacts]
    G --> H[File Validation & Pre-commit]
    
    H --> I{Event Type?}
    I -->|Push/PR opened/sync| J[Run DBT Build]
    I -->|Other| K[Skip DBT Build]
    
    J --> L{Branch Type?}
    L -->|main| M[Full DBT Build]
    L -->|feature branch| N[Incremental DBT Build]
    
    M --> O{Push to main?}
    N --> O
    K --> O
    
    O -->|Yes| P[Generate DBT Docs]
    O -->|No| Q[Skip Docs]
    
    P --> R[Extract Release Version]
    R --> S[Create Git Tag]
    S --> T[Upload Release Assets]
    T --> U[Cleanup Resources]
    
    Q --> V{PR Closed?}
    V -->|Yes| U
    V -->|No| W[End]
    U --> W
    
    style A fill:#e1f5fe
    style J fill:#c8e6c9
    style P fill:#fff3e0
    style U fill:#ffebee
```

## Workflow Triggers

The workflow is triggered by:
- **Push to main branch**: Runs full pipeline including deployment
- **Pull Request events**: 
  - `opened`: Runs validation and incremental build
  - `synchronize`: Runs validation and incremental build  
  - `closed`: Runs cleanup only

## Detailed Step Breakdown

### 1. Environment Setup
- **Checkout**: Uses `actions/checkout@v4` to get the latest code
- **Python Setup**: Installs Python 3.12
- **BigQuery Authentication**: Decodes base64-encoded service account key from secrets

### 2. Dataset Name Calculation
- For PRs: Uses PR number as dataset suffix
- For main branch: Appends short commit hash
- Sanitizes name for BigQuery compatibility
- Format: `pr__{sanitized_name}`

### 3. Dependency Management
- Installs UV (fast Python package installer)
- Creates virtual environment
- Syncs dependencies from `uv.lock`
- Installs project in editable mode

### 4. Artifact Management
- Downloads previous run artifacts using `robinraju/release-downloader@v1`
- Used for incremental builds on feature branches

### 5. Validation Phase
- Runs `dbt deps` to install DBT packages
- Executes `dbt parse` to validate model syntax
- Runs `pre-commit` hooks for code quality checks

### 6. DBT Build Phase
**Conditional Execution**: Only runs for push events or PR open/sync events

**Environment Variables**:
- `DATASET_PREFIX`: "CI_"
- `DBT_SCHEMA`: "CI_DWH"
- `DBT_PROFILE_PROJECT`: From secrets
- `BIGQUERY_DATABASE`: From variables

**Build Strategy**:
- **Main Branch**: Full build (`dbt build`)
- **Feature Branches**: Incremental build (`dbt build --select "+state:modified+" --state ./target/last_run`)

### 7. Documentation Generation
**Conditional**: Only for push events to main

- Generates static DBT documentation
- Creates `docs_site` directory with:
  - `static_index.html`
  - `index.html`
  - `manifest.json`
  - `catalog.json`

### 8. Release Management
**Conditional**: Only for push events to main

- **Version Strategy**: `YYYY.MM.{increment}` format
- **Tag Creation**: Automatically increments based on existing tags
- **Asset Upload**: Uploads documentation files as release artifacts

### 9. Cleanup Phase
**Conditional**: Runs when PR is closed OR push to main

- Deletes temporary BigQuery datasets
- Cleans up branch-specific resources
- Uses `delete_database` DBT operation

## Environment Variables & Secrets

### Required Secrets
- `BIGQUERY_KEYFILE_JSON_BASE64`: Base64-encoded BigQuery service account key
- `DBT_PROFILE_PROJECT`: BigQuery project ID for DBT profile
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### Required Variables
- `BIGQUERY_DATABASE`: BigQuery database/project name
- `DBT_PROFILE_PROJECT`: DBT profile project configuration

### Environment Variables Set During Runtime
- `DB_NAME`: Dynamic dataset name based on branch/PR
- `BIGQUERY_KEYFILE_PATH`: Path to decoded service account key
- `RELEASE_VERSION`: Auto-generated version tag

## Key Features

### 🚀 **Incremental Builds**
Feature branches only build modified models and their dependencies, improving build times.

### 📊 **Automatic Documentation**
DBT documentation is automatically generated and published as GitHub releases.

### 🏷️ **Semantic Versioning**
Automatic version tagging using date-based versioning (YYYY.MM.increment).

### 🧹 **Resource Cleanup**
Automatic cleanup of temporary BigQuery datasets to manage costs.

### ✅ **Quality Gates**
Pre-commit hooks and DBT parsing ensure code quality before deployment.

## Build Artifacts

Each successful build produces:
- `static_index.html`: Static DBT documentation
- `index.html`: DBT documentation homepage  
- `manifest.json`: DBT model metadata
- `catalog.json`: DBT catalog information
- `run_results.json`: Build execution results

## Troubleshooting

### Common Issues

1. **BigQuery Authentication Failures**
   - Verify `BIGQUERY_KEYFILE_JSON_BASE64` secret is correctly set
   - Ensure service account has necessary BigQuery permissions

2. **DBT Build Failures**
   - Check DBT model syntax using `dbt parse`
   - Verify BigQuery dataset permissions
   - Review `dbt debug` output for configuration issues

3. **Pre-commit Failures**
   - Run `pre-commit run --all-files` locally
   - Fix formatting and linting issues before pushing

4. **Release Upload Failures**
   - Ensure `GITHUB_TOKEN` has necessary permissions
   - Check if release with same tag already exists

## Local Development

To run similar checks locally:

```bash
# Install dependencies
uv sync
uv pip install -e .

# Run validation
dbt deps
dbt parse
pre-commit run --all-files

# Test DBT build (requires BigQuery setup)
dbt debug
dbt build
```

## Monitoring

Monitor workflow execution through:
- GitHub Actions tab in repository
- Build logs for debugging failures
- Release artifacts for documentation updates
- BigQuery console for dataset management
