@echo off
rem 
rem usage: run.bat <mode>
rem 
rem Modes:
rem - debug
rem - production|prod
rem 
rem Available ENV:
rem - FLASKHOST : hostname (default: 0.0.0.0)
rem - FLASKPORT : server port (default: 5000)
rem - MAINFILE : (full) module name (default: main)
rem - APP : WSGI app object (default: app)
rem 

set SRCDIR=".\app"

IF "%FLASKHOST%"=="" set "FLASKHOST=0.0.0.0"
IF "%FLASKPORT%"=="" set "FLASKPORT=5000"
IF "%MAINFILE%"=="" set "MAINFILE=main"
IF "%APP%"=="" set "APP=app"

set conf="%~1"
if %conf%=="" set "conf=production"

cd %SRCDIR%

if %conf%=="debug" (
	rem Run flask dev server
	python %MAINFILE%.py
) else (
	rem 'prod' or 'production'
	rem Run waitress WSGI server
	waitress-serve --host=%FLASKHOST% --port=%FLASKPORT% %MAINFILE%:%APP%
)

cd ..
echo.