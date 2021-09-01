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
  $Current_Images = docker images 2>$null;
} catch {
  Log-Error("Failed to access local images");
  exit(1);
}
Log-Step("Accessed the local images");

if ($Current_Images -Match "stock_counselor_image") {
  Log-Step("stock_counselor_image was detected");
}
else {
  Log-Error("Please create a stock_counselor_image docker image");
  exit(1);
}

try {
  $Current_Containers = docker container ls 2>$null;
} catch {
  Log-Error("Failed to access local containers");
  exit(1);
}
Log-Step("Accessed the local containers");

if ($Current_Containers -Match "stock_counselor") {
  Log-Error("Please delete an existing stock_counselor container");
  exit(1);
}

try {
  docker run -it -d -p 8083:27017 --name stock_counselor stock_counselor_image 2>$null;
} catch {
  Log-Error("Failed to initialize a stock_counselor container");
  exit(1);
}
Log-Step("stock_counselor container was initialized");

try {
  $Response = docker exec stock_counselor mongod --fork --config /etc/mongod.conf 2>$null;
  if ($Response -Match "ERROR") {
    throw;
  }
} catch {
  Log-Error("Failed to start mongod service at stock_counselor container");
  exit(1);
}
Log-Step("Mongod service was started at stock_counselor container");

try {
  docker cp mongodb_init_scripts stock_counselor:/ 2>$null;
} catch {
  Log-Error("Failed to copy mongodb_init_scripts to the stock_counselor container");
  exit(1);
}
Log-Step("Copied the mongodb_init_scripts to the stock_counselor container");

try {
  docker exec -it stock_counselor bash -c "cd ./mongodb_init_scripts && ./mongodb.sh" 2>$null;
} catch {
  Log-Error("Failed to execute mongodb.sh at the stock_counselor container");
  exit(1);
}
Log-Step("Mongodb was configured at stock_counselor container");