#!/bin/bash

create_user() {
  output=$(rabbitmqctl add_user $1 $2 2>/etc/null);
  
  if grep -q "Done. Don't forget to grant the user permissions" <<< $output; then
    echo "RabbitMq -- Created the $1 user"
  else
    echo "RabbitMq -- ERROR -- Failed to create the $1 user"
    echo $output
    exit 1
  fi
}

remove_user () {
  output=$(rabbitmqctl delete_user $1 2>/etc/null);
  
  if grep -q "Deleting user \"$1\"" <<< $output; then
    echo "RabbitMq -- Removed the $1 user"
  else
    echo "RabbitMq -- ERROR -- Failed to remove the $1 user"
    echo $output
    exit 1
  fi
}

set_permissions () {
  output=$(rabbitmqctl set_permissions -p $1 $2 "amq\.direct|$3" "amq\.direct|$4" "amq\.direct|$5");
  
  if grep -q "Setting permissions for user \"$2\" in vhost \"$1\"" <<< $output; then
    echo "RabbitMq -- Permissions for the $2 user have been set"
  else
    echo "RabbitMq -- ERROR -- Failed to set permissions for the $2 user"
    echo $output
    exit 1
  fi
}

remove_user "data_gatherer_main"
remove_user "data_gatherer_worker"
remove_user "recommendation_main"
remove_user "recommendation_worker"
create_user "data_gatherer_main" "data_gatherer_main"
create_user "data_gatherer_worker" "data_gatherer_worker"
create_user "recommendation_main" "recommendation_main"
create_user "recommendation_worker" "recommendation_worker"
set_permissions "/" "data_gatherer_main" "data-gathering" "data-gathering" "data-gathering"
set_permissions "/" "data_gatherer_worker" "data-gathering" "data-gathering" "data-gathering"
set_permissions "/" "recommendation_main" "recommendation" "recommendation" "recommendation"
set_permissions "/" "recommendation_worker" "recommendation" "recommendation" "recommendation"