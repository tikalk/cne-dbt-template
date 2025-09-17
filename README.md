# 🚀 Tikal CNE DBT Enterprise Template

[![DBT Version](https://img.shields.io/badge/dbt-1.9.3-FF694B?logo=dbt&logoColor=white)](https://docs.getdbt.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)
[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Enterprise-grade DBT template with advanced CLI tooling, automated workflows, and production-ready data pipelines**

An opinionated, battle-tested DBT project template designed for enterprise data teams. Features intelligent CLI automation, comprehensive validation, and seamless integration with modern data orchestration platforms like Dagster.

## ✨ Key Features

- 🎯 **Smart CLI Interface** - Interactive command-line tools for rapid development
- 🏗️ **Enterprise Architecture** - Staging → Marts data modeling patterns  
- 🔄 **Dagster Integration** - Native support for asset-based orchestration
- 🛡️ **Advanced Validation** - SQL linting, model validation, and data quality checks
- 🚀 **CI/CD Ready** - Production-grade GitHub Actions workflows
- 📊 **Multi-Warehouse Support** - BigQuery, Snowflake, and more
- 🔍 **Data Observability** - Built-in monitoring with Elementary Data
- 📝 **Auto-Documentation** - Self-documenting models and lineage

## 🎬 Quick Demo

```bash
# Set up your environment in seconds
task setup-env

# Launch the interactive CLI
task cli

# Create a new data domain with models
create domain security_tools --sub-domain crowdstrike
create model --domain security_tools --type staging --name endpoint_data

# Run your pipeline
task dbt:build
```

## 🏛️ Architecture Overview

```
📁 models/
├── 🔧 staging/          # Clean, standardized source data
│   ├── integration_tools/
│   │   ├── okta/        # Identity & access management
│   │   ├── crowdstrike/  # Endpoint security
│   │   └── active_directory/
│   └── infra/           # Pipeline metadata & metrics
└── 🏪 marts/            # Business-ready analytics tables
    ├── security/        # Security analytics
    ├── compliance/      # Compliance reporting
    └── operations/      # Operational insights
```

## 🚀 Quick Start

### Prerequisites

- [Go-task](https://taskfile.dev/installation/) - Task runner
- Python 3.12+
- Access to BigQuery or Snowflake

### 1. Environment Setup

```bash
# Automated setup (installs gh, uv, pre-commit)
task setup-env

# Or use dev container for containerized development
# (see .devcontainer configuration)
```

### 2. Configuration

```bash
# Copy and configure environment
cp .env_example .env
# Edit .env with your warehouse credentials

# Test your setup
task test-setup
```

### 3. Launch CLI

```bash
# Start interactive CLI with autocomplete
task cli

# Verify warehouse connection
task dbt:debug
```

## 🎛️ CLI Commands

Our intelligent CLI provides guided workflows for common tasks:

### 📊 **Data Modeling**
```bash
create domain <domain_name>              # Create new data domain
create model --domain <name> --type <staging|marts>  # Generate models
create integration-tool <tool_name>      # Add new data source
create macro --name <macro_name>         # Reusable SQL components
```

### 🔍 **Development & Testing**
```bash
task dbt:run --select <model>           # Run specific models
task dbt:test                           # Execute data tests
task dbt:build                          # Full build pipeline
task dbt:docs                           # Generate documentation
```

### 🛠️ **Quality & Validation**
```bash
validate all                            # Run all validations
task dbt:lint                          # SQL formatting
task dbt:format                        # Auto-fix formatting
```

### 📈 **Monitoring & Observability**
```bash
task dbt:edr-report                     # Elementary data report
learn catalog                          # Explore data catalog
select organization                     # Switch contexts
```

## 🏗️ Project Structure

### 📂 **Models Organization**
```
models/
├── staging/                    # 🧹 Data cleaning & standardization
│   ├── _sources.yml           # Source definitions
│   └── stg_<source>_<entity>.sql
├── marts/                      # 🎯 Business logic & analytics
│   ├── core/                  # Core business entities
│   ├── finance/               # Financial analytics
│   └── security/              # Security metrics
└── intermediate/              # 🔄 Reusable transformations
```

### 🔧 **Macros & Utilities**
```
macros/
├── create_database/           # Database management
├── generate_schema_name/      # Dynamic schema naming
├── get_custom_alias/          # Table aliasing
└── normalization/             # Data standardization
```

### 🧪 **Testing & Validation**
- **Generic Tests**: Uniqueness, not-null, referential integrity
- **Singular Tests**: Custom business logic validation
- **Data Quality**: Elementary data monitoring
- **SQL Linting**: SQLFluff integration

## 🔄 CI/CD Pipeline

Our GitHub Actions workflow provides:

- 🔍 **Slim CI** - Only test changed models
- 🧪 **Automated Testing** - Data quality validation
- 📊 **Documentation** - Auto-generated data catalog
- 🚀 **Deployment** - Multi-environment support
- 📈 **Monitoring** - Performance tracking

### Pipeline Stages
1. **Validation** → SQL linting, model validation
2. **Testing** → Unit tests, data quality checks  
3. **Build** → Compile and run models
4. **Deploy** → Environment-specific deployment
5. **Monitor** → Data freshness and quality alerts

## 🛡️ Data Quality & Governance

### Built-in Validations
- **Schema Enforcement** - Automatic schema validation
- **Data Freshness** - Source data recency checks
- **Referential Integrity** - Cross-table relationship validation
- **Custom Business Rules** - Domain-specific data quality tests

### Pre-commit Hooks
- 🔒 Security scanning (detect private keys)
- 📝 SQL formatting (SQLFluff)
- 🐍 Python code quality (black, isort, mypy)
- 🧪 DBT validations (parsing, testing)

## 🔧 Configuration

### Environment Variables
```bash
# Warehouse Configuration
SNOWFLAKE_ACCOUNT=your-account
SNOWFLAKE_USER=your-username
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_DATABASE=your-database

# BigQuery Configuration  
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
BQ_PROJECT=your-project-id
BQ_DATASET=your-dataset

# Pipeline Configuration
ORG_ID=your-organization-id
DBT_TARGET=dev  # dev, staging, prod
```

### Profiles Configuration
The project supports multiple target environments with automatic schema and database naming conventions.

## 📚 Documentation & Learning

### 📖 **Getting Started Guides**
- [Architecture Overview](docs/overview/11_2_2025_architecture.md)
- [DBT Task Commands](docs/overview/19_2_2025_task_dbt.md)  
- [Main Workflows](docs/overview/19_2_2025_workflow.md)
- [CI/CD Overview](docs/overview/19_2_2025_CI.md)

### 🎓 **Recommended Reading**
- [DBT Best Practices](https://docs.getdbt.com/best-practices)
- [DBT and Dagster Integration](https://docs.dagster.io/integrations/dbt)
- [Modern Data Stack Architecture](https://www.getdbt.com/product/what-is-dbt)

### 🔌 **IDE Extensions**
- [VS Code DBT Power User](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user)
- [IntelliJ DBT Plugin](https://plugins.jetbrains.com/plugin/23789-dbt)

## 🚨 Troubleshooting

### Common Issues

**Connection Problems**
```bash
task dbt:debug  # Validate warehouse connection
```

**Model Compilation Errors**
```bash
dbt build --debug  # Verbose logging
# Check compiled SQL in target/compiled/
```

**Performance Issues**
```bash
task dbt:run --select "+state:modified"  # Slim runs
```

### Debug Mode
Enable detailed logging for troubleshooting:
```bash
export DBT_LOG_LEVEL=debug
task dbt:run --debug
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork and clone the repository
2. Create a feature branch
3. Make your changes with tests
4. Run validation: `task validate`
5. Submit a pull request

## 📊 Monitoring & Observability

### Elementary Data Integration
- **Data Quality Monitoring** - Automated anomaly detection
- **Lineage Tracking** - Visual data flow representation  
- **Performance Metrics** - Query performance insights
- **Alerting** - Slack/email notifications for issues

### Usage Analytics
Track model usage, performance, and data freshness with built-in monitoring dashboards.

## 🏢 Enterprise Features

- **Multi-tenant Architecture** - Organization and instance isolation
- **Role-based Access Control** - Fine-grained permissions
- **Audit Logging** - Complete change tracking
- **Disaster Recovery** - Backup and restore procedures
- **Compliance Ready** - SOX, GDPR, HIPAA support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

Built with ❤️ by the Tikal CNE team using:
- [DBT](https://www.getdbt.com/) - Data transformation framework
- [Dagster](https://dagster.io/) - Data orchestration platform  
- [Elementary](https://www.elementary-data.com/) - Data observability
- [Go-task](https://taskfile.dev/) - Task automation
- [SQLFluff](https://sqlfluff.com/) - SQL linting

---

**Ready to transform your data pipeline?** 🚀 [Get started](#-quick-start) or [explore the docs](#-documentation--learning)!
