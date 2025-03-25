
/*
in production table name will be without [domain]_slv__
*/
with source as (

    select * from {{ ref('users_stg__user_cast') }}

)

select *
from source
