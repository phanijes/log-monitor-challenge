# Log Monitoring Application

This project aims to build a log monitoring application in Python that reads a log file, measures job durations, and reports on jobs exceeding predefined time thresholds.
To find more about the challenge look into "requirements" folder.

## Project Structure

- `log_monitor.py`: The main Python script for monitoring logs.
- `logs.log`: The input log file to be processed.
- `run.sh`: Script to test the Python script.
- `sample_output.txt`: Test output when executed the script.
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

1. Clone or download the project files.
2. Ensure Python 3 is installed: ````bash python3 --version ```
3. Make the shell script (`run.sh`) executable: ````bash chmod +x run.sh ```
4. Run any of the below commands to execute the script
   ```bash
   bash run.sh
   ```
   ```bash
   python log_monitor.py logs.log
   ```

## Example Output

The script will print the report directly to the console. Here's an example of what you might see:

2025-06-30 20:42:04 - INFO - --- Log Monitoring Report ---
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 051' (PID: 39547) took 11.48 minutes
2025-06-30 20:42:04 - ERROR - Job 'scheduled task 515' (PID: 45135) took 12.38 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 074' (PID: 71766) took 5.78 minutes
2025-06-30 20:42:04 - ERROR - Job 'background job wmy' (PID: 81258) took 14.77 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 268' (PID: 87228) took 9.47 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 811' (PID: 50295) took 6.58 minutes
2025-06-30 20:42:04 - WARNING - Job 'scheduled task 294' (PID: 27222) took 6.13 minutes
----
You can find sample output in `sample_output.txt`