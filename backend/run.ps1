# @echo off
# 
# usage: run <mode>
# 
# Modes:
# - dev
# - production|prod
# 

$envfile = "./.env"

./DotEnvLoad.ps1 $envfile -Remove # -Verbose
./DotEnvLoad.ps1 $envfile # -Verbose

# $mainfile = "main"
# $app = "app"
# $fullapp = "$($mainfile):$($app)"

# Set defaults
# $env:FLASKPORT = If($env:FLASKPORT){$env:FLASKPORT}else{"5555"}

Set-Location "./app"

$myenv = $args[0]
If ($myenv -eq "dev") {
	echo "Starting Flask dev server..."
	python main.py
} else {
	# 'prod' or 'production'
	echo "Starting CherryPy production server..."
	python server.py
}

Set-Location ..
