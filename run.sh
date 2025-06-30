#!/bin/bash

# Log Monitor Runner Script
# This script runs the log monitoring application with the provided log file

echo "Log Monitoring Application"
echo "=========================="
echo

# Check if log file exists
if [ ! -f "logs.log" ]; then
    echo "Error: logs.log file not found!"
    echo "Please ensure the log file is in the current directory."
    exit 1
fi

# Check if Python script exists
if [ ! -f "log_monitor.py" ]; then
    echo "Error: log_monitor.py not found!"
    echo "Please ensure the log monitor script is in the current directory."
    exit 1
fi

echo "Running log monitor on logs.log..."
echo "Warning threshold: 5 minutes"
echo "Error threshold: 10 minutes"
echo

# Run the log monitor
python log_monitor.py logs.log --verbose

echo
echo "Monitoring complete!"