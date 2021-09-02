$ErrorActionPreference = 'Stop';

function Log-Error {
  param ($Message)

  Write-Output "ERROR -- $($Message)";
}

function Log-Step {
  param ($Message)

  Write-Output "[x] $($Message)";
}

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

try {
  docker run -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root `
  -d -p 8083:27017 --name mongo_local mongo --auth 2>$null;
} catch {
  Log-Error("Failed to initialize the mongo_local container");
  exit(1);
}
Start-Sleep -Seconds 2
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