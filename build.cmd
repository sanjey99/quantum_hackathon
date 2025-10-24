@echo off
REM Maven Build Script for Windows

REM Check if JAVA_HOME is set
if "%JAVA_HOME%" == "" (
    echo Error: JAVA_HOME is not set
    echo Please install Java and set JAVA_HOME
    exit /b 1
)

REM Check if Maven exists in the tools directory
if not exist "%~dp0tools\apache-maven-3.9.5" (
    echo Downloading Maven...
    mkdir tools 2>nul
    powershell -Command "& {Invoke-WebRequest -Uri 'https://archive.apache.org/dist/maven/maven-3/3.9.5/binaries/apache-maven-3.9.5-bin.zip' -OutFile 'tools\maven.zip'}"
    powershell -Command "& {Expand-Archive -Path 'tools\maven.zip' -DestinationPath 'tools'}"
    del tools\maven.zip
)

REM Set Maven environment variables
set "M2_HOME=%~dp0tools\apache-maven-3.9.5"
set "PATH=%M2_HOME%\bin;%PATH%"

REM Run Maven command
cd app
mvn %*