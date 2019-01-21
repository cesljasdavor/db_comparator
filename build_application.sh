#!/usr/bin/env bash
echo "Starting build of db_comparator application..."
echo "Deleting existing build directory"
rm -rf build
echo "Deleting existing dist directory"
rm -rf dist
echo "Building..."
if sudo pip3 install pyinstaller; then
    echo "Pyinstaller package successfully installed"
else
    if sudo pip install pyinstaller; then
        echo "Pyinstaller package successfully installed"
    else
        echo "Pip is not installed. Please install pip"
        exit -1
    fi
fi
if sudo pyinstaller -n db_comparator --log-level ERROR --hidden-import numpy.core._dtype_ctypes --onefile --windowed --icon=database_comparator.png --clean main.py; then
    echo "Build finished successfully"
else
    echo "Build failed"
    exit -1
fi

echo "Adding script to /usr/bin"
if sudo cp ./dist/db_comparator /usr/bin/; then
    echo "Script added to /usr/bin"
fi
echo "Adding icon to /usr/share/icons"
if sudo cp ./database_comparator.png /usr/share/icons; then
    echo "Icon added to /usr/share/icons"
fi
echo "Adding desktop entry to /usr/share/applications"
if sudo cp ./db_comparator.desktop /usr/share/applications; then
    echo "Desktop entry added to /usr/share/applications"
fi
echo "Done"