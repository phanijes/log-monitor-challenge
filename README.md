# Log Monitoring Application

This project aims to build a log monitoring application in Python that reads a log file, measures job durations, and reports on jobs exceeding predefined time thresholds.
To find more about the challenge look into "requirements" folder.

## Project Structure

- `log_monitor.py`: The main Python script for monitoring logs.
- `logs.log`: The input log file to be processed.
- `run.sh`: Script to test the Python script.
- `README.md`: This documentation.


## Features

- Parses CSV-formatted log entries.
- Tracks the start and end times of individual jobs identified by their Process ID (PID).
- Calculates the total duration for each job.
- Generates a report with the following alerts:
    - **WARNING**: If a job takes longer than 5 minutes.
    - **ERROR**: If a job takes longer than 10 minutes.
- Handles common log file issues such as missing START/END events or malformed lines.

## Log Structure

Each line in the `logs.log` file is expected to be in the following CSV format:

`HH:MM:SS,job_description,STATUS,PID`

- `HH:MM:SS`: Timestamp in hours, minutes, and seconds.
- `job_description`: A string describing the job (e.g., "scheduled task 032", "background job wmy").
- `STATUS`: Either "START" or "END", indicating the beginning or completion of a job.
- `PID`: A unique integer Process ID for the job.

## How to Run


1.  **Save the script:** Save the Python code provided as `log_monitor.py`.
2.  **Place the log file:** Ensure your log file (e.g., `logs.txt`) is in the same directory as the script, or update the `log_file_path` variable in `monitor_logs()` function call if your file is located elsewhere.
3.  **Run from terminal:** Open your terminal or command prompt, navigate to the directory where you saved the files, and run the script using Python:

    ```bash
    python log_monitor.py
    ```

## Example Output

The script will print the report directly to the console. Here's an example of what you might see:

Log Monitoring Application
==========================

Running log monitor on logs.log...
Warning threshold: 5 minutes
Error threshold: 10 minutes

2025-06-30 20:42:04 - INFO - --- Log Monitoring Report ---
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 051' (PID: 39547) took 11.48 minutes
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 515' (PID: 45135) took 12.38 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 074' (PID: 71766) took 5.78 minutes
2025-06-30 20:42:04 - ERROR - Job 'background job wmy' (PID: 81258) took 14.77 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 268' (PID: 87228) took 9.47 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 811' (PID: 50295) took 6.58 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 294' (PID: 27222) took 6.13 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 794' (PID: 87570) took 7.88 minutes
2025-06-30 20:42:04 - WARNING - Job 'background job sqm' (PID: 99672) took 5.22 minutes
2025-06-30 20:42:04 - WARNING - Job 'background job xfg' (PID: 86716) took 5.57 minutes
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 004' (PID: 22003) took 11.22 minutes
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 064' (PID: 85742) took 12.28 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 746' (PID: 98746) took 7.28 minutes
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 460' (PID: 39860) took 19.87 minutes
2025-06-30 20:42:04 - ERROR - Job 'background job tqc' (PID: 52532) took 13.88 minutes
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 936' (PID: 62401) took 10.40 minutes
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 374' (PID: 23703) took 13.43 minutes
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 182' (PID: 70808) took 33.72 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 672' (PID: 24482) took 8.60 minutes

2025-06-30 20:42:04 - INFO - --- Unfinished Jobs ---
2025-06-30 20:42:04 - INFO - Job 'scheduled task 333' (PID: 72029) started at 12:03:20 but did not have an END event.
2025-06-30 20:42:04 - INFO - Job 'scheduled task 016' (PID: 72897) started at 12:12:27 but did not have an END event.

2025-06-30 20:42:04 - INFO - SUMMARY: 9 warnings, 10 errors
2025-06-30 20:42:04 - INFO - --- Report End ---

Monitoring complete!
Check 'log_monitor_output.log' for detailed output.