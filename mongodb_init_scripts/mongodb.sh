#!/bin/bash
clear_database () {
  output=$(mongo < $1.txt);
  
  if grep -q "{ \"ok\" : 1 }" <<< $output; then
    echo "MongoDb -- Cleared the $2 database"
  else
    echo "MongDb -- ERROR -- Failed to clear the $2 database"
    echo $output
    exit 1
  fi
}

create_user () {
  output=$(mongo < $1.txt);
  
  if grep -q "Successfully added user" <<< $output; then
    echo "MongoDb -- Created $2 user"
  else
    echo "MongoDb -- ERROR -- Failed to create $2 user"
    echo $output
    exit 1
  fi
}

populate_database () {
  output=$(mongo < $1.txt);

  if grep -q "\"writeErrors\" : \[ \]" <<< $output; then
    echo "MongoDb -- Populated $2 database"
  else
    echo "MongoDb -- ERROR -- Failed to populated $2 database"
    echo $output
    exit 1
  fi
}

create_user "create_admin_user" "admin"
clear_database "clear_non_applicative_users_database" "non_applicative_users"
clear_database "clear_applicative_users_database" "applicative_users"
clear_database "clear_backend_tasks_database" "backend_tasks"
clear_database "clear_investment_recommendations_database" "investment_recommendations"
clear_database "clear_financial_reports_database" "financial_reports"
clear_database "clear_financial_user_profiles_database" "financial_user_profiles"
create_user "create_applicative_users_service_user" "applicative_users_service"
create_user "create_data_gathering_main_service_user" "data_gathering_main_service"
create_user "create_data_gathering_worker_service_user" "data_gathering_worker_service"
create_user "create_recommendation_main_service_user" "recommendation_main_service"
create_user "create_recommendation_worker_service_user" "recommendation_worker_service"
populate_database "populate_applicative_users_database" "applicative_users"
populate_database "populate_financial_user_profiles_database" "financial_user_profiles"