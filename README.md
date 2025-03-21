# DBT Project

This DBT project is designed to be used in conjunction with Dagster as an orchestrator. Conceptually, DBT models map to Dagster Assets.


### Setup Local Development

Before using this setup, ensure you have the following installed:

- [Go-task](https://taskfile.dev/installation/)


To create the local environment, the developer can either use:

1. `task setup-env` (this will install the following: )        
    * [gh](https://cli.github.com)
    * [uv](https://astral.sh)
    * [pre-commit](https://pre-commit.com/)
2. Use dev container

To test your setup run:

`task test-setup`

This command will also check to see if the environment parameters are set

This will do dbt debug and also login to github cli

If you have already done this in the past, to re-activate your environment run:
```
source ./.venv/bin/activate  
```

## Test setup
Copy .env_example to .env and update the values

Once you have finished `task test-setup` successfully run the following command

`task cli`

This should run the cli.

Now run:

`tasks dbt:debug`

This will validate the dbt connection to wharehouse.


## Basic Usage
* Run --help to see all methods.
* Using the tab will enable autocomplete
* If you have parameters for the methods you can enter them inline, or enter and you will be prompted


## Project documentation

If you are read to jump in read the following documentation:

* [Overview](docs/overview/11_2_2025_architecture.md)
* [DBT Task Commands](docs/overview/19_2_2025_task_dbt.md)
* [Main Workflows](docs/overview/19_2_2025_workflow.md)
* [CI Overview](docs/overview/19_2_2025_CI.md)


## Getting started

Prior to writing models, it's important to understand some of the concepts. Recommended reading:

- [DBT and Dagster](https://docs.dagster.io/integrations/dbt)
- [What is DBT](https://www.getdbt.com/product/what-is-dbt)

There are a couple of useful plugins when writing models:

- [VS Code](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user)
- [IntelliJ](https://plugins.jetbrains.com/plugin/23789-dbt)

You might run into autoformatting issues when writing SQL models. Please check that your editor recognizes the file as "Jinja SQL templates" rather than raw SQL.

## Project structure

The project structure follows dbt recommendations.

- [Staging views](https://docs.getdbt.com/best-practices/how-we-structure/4-marts)
- [Marts - Business Defined Entities](https://docs.getdbt.com/best-practices/how-we-structure/4-marts)

## Debugging issues

Often any issues presented will be visible via the UI in Dagster in logs. However, if you require a bit more in-depth debugging, you can perform the following steps:

- Run `dbt build --debug` to output more verbose logs from this folder
- Check out the compiled models in the `target/compiled/dbt_project_models` folder and try to run the compiled steps in warehouse.


## Components

### DBT Models

DBT models are SQL files that define transformations on your data. These models are organized into different layers:

- **Staging**: Raw data is cleaned and transformed into a more usable format.
- **Marts**: Business-defined entities that are used for reporting and analysis.

#### Folder Structure
    Area:
        data collection, integrations, infra, ....)
    Realm (sub area - can be nested directories):
        integration_tools:
            okkta 
                anonymization (staging)
                scoring (marts)
            active directory
                anonymization (staging)
                scoring (marts)
            crowd strike
                anonymization (staging)
                scoring (marts)
        infra:
            pipeline_metadata
            metrics
        
        

### Macros

Macros are reusable SQL snippets that can be used across multiple models. They help to avoid repetition and make your SQL code more maintainable.

#### Infra macros   
    * create_database - create your warehouse db if not exists
    * delete_database - delete your warehouse db if exists (allows you to reset your db)
    * [generate_schema_name](https://docs.getdbt.com/docs/build/custom-schemas) - allow you do definee location of tables in schema by code
    * [get_custom_alias](https://docs.getdbt.com/docs/build/custom-aliases) - allow you do define name of table in schema by code

### Seeds

Seeds are CSV files that are loaded into your data warehouse as tables. They are useful for static data that doesn't change often.

### Snapshots

Snapshots are used to capture the state of your data at a specific point in time. They are useful for tracking changes to your data over time.

### Tests

Tests are used to validate the quality of your data. They can be used to check for things like null values, unique constraints, and referential integrity.

### Documentation

Documentation is used to describe your models, macros, seeds, and snapshots. It helps to provide context and understanding for your data transformations.


### Pre-commit Hooks

Pre-commit hooks are used to enforce code quality standards. They can be used to run linters, formatters, and other checks before code is committed.

The pre commit hooks that we use are:

On commit:
    security hooks (detect-private-key, no-commit-to-branch)
    bad file hooks (check-merge-conflict, check-toml, check-added-large-files)
    sql related hooks (sqlfluff)
    python related hooks for python models (isort, black flake8, flake8, mypy)
    dbt checks (check-script-semicolon)

On Push (since these checkes take time, they are moved to pre push):
    dbt checks (check-script-has-no-table-name, check-macro-arguments-have-desc, check-macro-arguments-have-desc,   check-script-has-no-table-name, dbt-parse, dbt-test)



### CI/CD

Continuous Integration and Continuous Deployment (CI/CD) pipelines are used to automate the testing and deployment of your DBT models. They help to ensure that your data transformations are always in a deployable state.


### Validation / PreCommit

In order to get better code, we have added the following validations:

1. SQL formatting using [sqlfluff](https://sqlfluff.com/)
2. Python formatting for DBT Python modules
3. [dbt-checkpoint](https://github.com/dbt-checkpoint/dbt-checkpoint)



19_2_2025_workflow.md

### Resources

- [Slim CI with DBT Core and Snowpark](https://medium.com/@thiernomadiariou/slim-ci-with-dbt-core-and-snowpark-ffbb80b81fec)

## Contributing

Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License.


This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
