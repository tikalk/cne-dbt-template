def model(dbt, session):

    my_sql_model_df = dbt.ref("my_sql_model")

    print(my_sql_model_df)

    return my_sql_model_df
