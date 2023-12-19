# @echo off
# 
# usage: run <mode>
# 
# Modes:
# - debug
# - production|prod
# 
$envfile = "./.env"

./DotEnvLoad.ps1 $envfile -Remove #-Verbose
./DotEnvLoad.ps1 $envfile #-Verbose

$mainfile = "main"
$app = "app"
$fullapp = "$($mainfile):$($app)"

# Set defaults
# $env:FLASKPORT = If($env:FLASKPORT){$env:FLASKPORT}else{ "5555" }

Set-Location "./app"

$myenv = $args[0]
If ($myenv -eq "debug") {
	# Run flask dev server
	#python "$mainfile.py"
	python server.py
} else {
	# 'prod' or 'production'
	# Run waitress WSGI server
#	waitress-serve --host=0.0.0.0 --port=$env:FLASKPORT $fullapp
	echo Nothing.
}

Set-Location ..
