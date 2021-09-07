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

create_user "create_admin_user" "admin"
clear_database "clear_financial_reports_database" "financial_reports"
clear_database "clear_financial_user_profiles_database" "financial_user_profiles"
clear_database "clear_recommendations_database" "recommendations"
clear_database "clear_backend_tasks_database" "backend_tasks"
clear_database "clear_users_database" "users"
create_user "create_data_gatherer_user" "data_gatherer"
create_user "create_recommender_user" "recommender"