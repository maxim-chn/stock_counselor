$ErrorActionPreference = 'Stop';

function Log-Error {
  param ($Message)

  Write-Output "ERROR -- $($Message)";
  Write-Output "";
}

function Log-Step {
  param ($Message)

  Write-Output "[x] $($Message)";
  Write-Output "";
}

try {
  if (Test-Path -Path .venv) {
    rm -r .venv;
    Log-Step("Removed an existing virtual environment for Python");
  }
  python -m venv .venv 2>$null;
  Set-ExecutionPolicy Unrestricted -Scope Process 2>$null;
  .\.venv\Scripts\Activate.ps1;
  pip install --upgrade pip;
  pip install bottle;
  pip install pika;
  pip install pymongo;
  pip install requests;
  deactivate;
  Set-ExecutionPolicy Restricted -Scope Process 2>$null;
} catch {
  Log-Error("Failed to initialize virtual environment for Python");
  exit(1);
}
Log-Step("Initialized virtual environment for Python");

try {
  $Current_Containers = docker container ls 2>$null;
} catch {
  Log-Error("Failed to access local containers");
  exit(1);
}
Log-Step("Accessed the local containers");

if ($Current_Containers -Match "mongo_local") {
  Log-Error("Please delete an existing mongo_local container");
  exit(1);
}
if ($Current_Containers -Match "rabbitmq_local") {
  Log-Error("Please delete an existing rabbitmq_local container");
  exit(1);
}


try {
  docker run -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root `
  -d -p 8083:27017 --name mongo_local mongo --auth 2>$null;
} catch {
  Log-Error("Failed to initialize the mongo_local container");
  exit(1);
}
Start-Sleep -Seconds 5
Log-Step("Initialized mongo_local container");

try {
  docker cp mongodb_init_scripts mongo_local:/ 2>$null;
} catch {
  Log-Error("Failed to copy mongodb_init_scripts to the container");
  exit(1);
}
Log-Step("Copied the mongodb_init_scripts to the container");

try {
  docker exec -it mongo_local bash -c "cd ./mongodb_init_scripts && ./mongodb.sh" 2>$null;
} catch {
  Log-Error("Failed to execute mongodb.sh at the container");
  exit(1);
}

Log-Step("Configured the mongo_local container");

try {
  docker run -d --hostname localhost -p 5672:5672 -p 15672:15672 `
  --name rabbitmq_local -e RABBITMQ_DEFAULT_USER=root -e RABBITMQ_DEFAULT_PASS=root `
  rabbitmq:3-management
} catch {
  Log-Error("Failed to initialize the rabbitmq_local container");
  exit(1);
}
Start-Sleep -Seconds 10
Log-Step("Initialized rabbitmq_local container");

try {
  docker cp rabbitmq_init_scripts rabbitmq_local:/ 2>$null;
} catch {
  Log-Error("Failed to copy rabbitmq_init_scripts to the container");
  exit(1);
}
Log-Step("Copied the rabbitmq_init_scripts to the container");

try {
  docker exec -it rabbitmq_local bash -c "cd ./rabbitmq_init_scripts && ./rabbitmq.sh" 2>$null;
} catch {
  Log-Error("Failed to execute rabbitmq.sh at the container");
  exit(1);
}

Log-Step("Configured the rabbitmq_local container");