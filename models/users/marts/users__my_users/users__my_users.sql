
/*
in production table name will be without [domain]__
*/
with staging as (

    select * from {{ ref('users_stg__all_users') }}

)

select * from staging
