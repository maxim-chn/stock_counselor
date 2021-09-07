$ErrorActionPreference = 'Stop';

function Log-Error {
  param ($Message)

  Write-Output "ERROR -- $($Message)";
}

try {
  Set-ExecutionPolicy Unrestricted -Scope Process 2>$null;
  .\.venv\Scripts\Activate.ps1;
  py main.py $args[0];
  deactivate;
  Set-ExecutionPolicy Restricted -Scope Process 2>$null;
} catch {
  Log-Error("Failed during $($args[0]) service");
  exit(1);
}