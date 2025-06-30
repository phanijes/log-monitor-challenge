# log_monitor.py

import datetime
import csv
from typing import Dict, Any, Optional

# --- Constants ---
# Define thresholds for job duration in minutes
WARNING_THRESHOLD_MINUTES = 5.0
ERROR_THRESHOLD_MINUTES = 10.0

# --- Helper Functions (can remain outside class if they don't need class state) ---
def parse_log_entry(row: list[str], line_num: int, report_timestamp: str) -> Optional[Dict[str, Any]]:
    """
    Parses a single row from the CSV log file into a structured dictionary.

    Args:
        row (list[str]): A list of strings representing a single row from csv.reader.
        line_num (int): The current line number for error reporting.
        report_timestamp (str): The current timestamp for logging internal errors.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing parsed log entry details:
              {'timestamp_str': 'HH:MM:SS', 'job_description': '...',
               'status': 'START/END', 'pid': int, 'log_datetime': datetime.datetime}
        None: If the row is malformed or cannot be parsed.
    """
    try:
        if len(row) != 4:
            print(f"{report_timestamp} - WARNING - Skipping malformed line {line_num}: {','.join(row)} (Incorrect number of parts)")
            return None

        # Strip whitespace from each part of the row
        timestamp_str, job_description, status, pid_str = [item.strip() for item in row]
        
        # Convert PID to integer
        pid = int(pid_str)

        # Combine today's date with the log's time for a full datetime object
        today = datetime.date.today()
        log_time = datetime.datetime.strptime(timestamp_str, "%H:%M:%S").time()
        log_datetime = datetime.datetime.combine(today, log_time)

        return {
            'timestamp_str': timestamp_str,
            'job_description': job_description,
            'status': status.upper(), # Ensure status is uppercase for consistent comparison
            'pid': pid,
            'log_datetime': log_datetime
        }

    except ValueError as e:
        print(f"{report_timestamp} - ERROR - Could not parse line {line_num}: {','.join(row)} - {e}")
        return None
    except IndexError as e:
        print(f"{report_timestamp} - ERROR - Malformed line {line_num} (index error): {','.join(row)} - {e}")
        return None
    except Exception as e: # Catch any other unexpected parsing errors
        print(f"{report_timestamp} - ERROR - Unexpected error parsing line {line_num}: {','.join(row)} - {e}")
        return None

def calculate_duration_minutes(start_datetime: datetime.datetime, end_datetime: datetime.datetime) -> float:
    """
    Calculates the duration between two datetime objects in minutes.

    Args:
        start_datetime (datetime.datetime): The start time.
        end_datetime (datetime.datetime): The end time.

    Returns:
        float: The duration in minutes.
    """
    duration = end_datetime - start_datetime
    return duration.total_seconds() / 60

# --- LogMonitor Class ---
class LogMonitor:
    def __init__(self):
        """
        Initializes the LogMonitor with empty tracking data.
        """
        # Stores {pid: parsed_entry_dict_for_start_event} for currently active jobs
        self.active_jobs: Dict[int, Dict[str, Any]] = {} 
        self.warnings_count: int = 0
        self.errors_count: int = 0
        # To keep track of jobs that start but never end, used for final summary
        self.unfinished_jobs: Dict[int, Dict[str, Any]] = {} 

        # For consistent reporting timestamp throughout the run
        self.report_timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_log_file(self, log_file_path: str = "logs.log"):
        """
        Reads and processes the log file, tracking job durations and reporting issues.

        Args:
            log_file_path (str): The path to the log file.
        """
        print(f"{self.report_timestamp} - INFO - --- Log Monitoring Report ---")

        try:
            with open(log_file_path, 'r', newline='') as f:
                reader = csv.reader(f)
                for line_num, row in enumerate(reader, 1):
                    self._process_log_line(row, line_num)

        except FileNotFoundError:
            print(f"{self.report_timestamp} - ERROR - Log file not found at {log_file_path}")
            self.errors_count += 1
        except Exception as e:
            print(f"{self.report_timestamp} - ERROR - An unexpected error occurred: {e}")
            self.errors_count += 1
        finally:
            self._generate_final_report()

    def _process_log_line(self, row: list[str], line_num: int):
        """
        Processes a single parsed log entry to update job states and report durations.

        Args:
            row (list[str]): The raw row from the CSV reader.
            line_num (int): The line number of the row.
        """
        parsed_entry = parse_log_entry(row, line_num, self.report_timestamp)
        if not parsed_entry:
            # parse_log_entry already prints its own error/warning messages.
            # We increment counts based on simple check related to parsing failure.
            # A more robust solution might have parse_log_entry return a tuple of (parsed_data, error_level)
            if len(row) != 4: # Assuming this is the primary malformed line type caught as WARNING
                self.warnings_count += 1
            else: # Other parsing errors caught as ERROR
                self.errors_count += 1
            return

        pid = parsed_entry['pid']
        status = parsed_entry['status']
        job_description = parsed_entry['job_description']
        log_datetime = parsed_entry['log_datetime']
        timestamp_str = parsed_entry['timestamp_str']

        if status == "START":
            if pid in self.active_jobs:
                print(f"{self.report_timestamp} - WARNING - Job '{job_description}' (PID: {pid}) started at {self.active_jobs[pid]['timestamp_str']} but a new START event was logged at {timestamp_str}. Overwriting start time.")
                self.warnings_count += 1
            self.active_jobs[pid] = parsed_entry # Store the full parsed entry
            self.unfinished_jobs[pid] = parsed_entry # Add to unfinished list initially
        elif status == "END":
            if pid in self.active_jobs:
                start_entry = self.active_jobs.pop(pid) # Remove from active jobs
                if pid in self.unfinished_jobs:
                    self.unfinished_jobs.pop(pid) # Remove from unfinished jobs as it completed

                duration_minutes = calculate_duration_minutes(start_entry['log_datetime'], log_datetime)

                if duration_minutes > ERROR_THRESHOLD_MINUTES:
                    print(f"{self.report_timestamp} - ERROR - Job '{job_description}' (PID: {pid}) took {duration_minutes:.2f} minutes")
                    self.errors_count += 1
                elif duration_minutes > WARNING_THRESHOLD_MINUTES:
                    print(f"{self.report_timestamp} - WARNING - Job '{job_description}' (PID: {pid}) took {duration_minutes:.2f} minutes")
                    self.warnings_count += 1
                # Optional: INFO for jobs that complete within thresholds
                # else:
                #     print(f"{self.report_timestamp} - INFO - Job '{job_description}' (PID: {pid}) completed in {duration_minutes:.2f} minutes.")
            else:
                print(f"{self.report_timestamp} - WARNING - END event for job '{job_description}' (PID: {pid}) found at {timestamp_str}, but no corresponding START event was recorded.")
                self.warnings_count += 1
        # No 'else' needed for unknown status, as parse_log_entry already filters/warns
    
    def _generate_final_report(self):
        """
        Generates and prints the final summary report.
        """
        # Report on any jobs that started but never ended
        if self.unfinished_jobs:
            print(f"\n{self.report_timestamp} - INFO - --- Unfinished Jobs ---")
            for pid, entry in self.unfinished_jobs.items():
                print(f"{self.report_timestamp} - INFO - Job '{entry['job_description']}' (PID: {pid}) started at {entry['timestamp_str']} but did not have an END event.")

        print(f"\n{self.report_timestamp} - INFO - SUMMARY: {self.warnings_count} warnings, {self.errors_count} errors")
        print(f"{self.report_timestamp} - INFO - --- Report End ---")

# --- Main Execution ---
if __name__ == "__main__":
    monitor = LogMonitor()
    monitor.process_log_file()