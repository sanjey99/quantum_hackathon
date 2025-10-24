#!/bin/bash
# Maven Build Script for Unix/Linux/Mac

# Check if JAVA_HOME is set
if [ -z "$JAVA_HOME" ]; then
    echo "Error: JAVA_HOME is not set"
    echo "Please install Java and set JAVA_HOME"
    exit 1
fi

# Check if Maven exists in the tools directory
if [ ! -d "tools/apache-maven-3.9.5" ]; then
    echo "Downloading Maven..."
    mkdir -p tools
    curl -o tools/maven.zip https://dlcdn.apache.org/maven/maven-3/3.9.5/binaries/apache-maven-3.9.5-bin.zip
    cd tools
    unzip maven.zip
    rm maven.zip
    cd ..
fi

# Set Maven environment variables
export M2_HOME="$PWD/tools/apache-maven-3.9.5"
export PATH="$M2_HOME/bin:$PATH"

# Run Maven command
cd app
mvn "$@"