#!/bin/bash
output=$(mongo < initiate_admin_user.txt);
if grep -q "Successfully added user" <<< $output; then
  echo "Mongodb -- admin user was created"
fi
