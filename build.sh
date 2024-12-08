#!/bin/bash

echo "Setting up the build environment..."

# Step 1: Create a Virtual Environment
echo "Creating a virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
rm -rf build dist main.spec

# Step 7: Run PyInstaller
echo "Running PyInstaller..."
pyinstaller --onedir --noupx --noconsole --clean \
    --add-data "ui/assets:ui/assets" \
    --add-data "ui/data:ui/data" \
    --add-data "ui/ml:ui/ml" \
    --add-data "ui/pyqt/images:ui/pyqt/images" \
    --add-data "ui/pyqt:ui/pyqt" \
    --add-data "ui/utils:ui/utils" \
    --add-data "ui/controllers:ui/controllers" \
    --add-data "ui/ml/haarcascade_frontalface_default.xml:ui/ml" \
    --add-data "ui/ml/model.h5:ui/ml" \
    --add-data "$QT_PLUGIN_PATH:PyQt5/Qt/plugins" \
    $HIDDEN_IMPORTS \
    main.py

# Step 8: Check Build Success
if [ $? -eq 0 ]; then
    echo "Build completed successfully."
else
    echo "Build failed. Check the logs for errors."
    exit 1
fi

echo "Build process completed. Distribution folder is ready in ./dist"
