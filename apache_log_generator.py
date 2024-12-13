import os
import random
from datetime import datetime, timedelta

# Base directory for all Apache server logs
base_directory = "apache_servers"

# Generate unique timestamps
# Start from the last known timestamp or the current time

def generate_timestamps(num_lines, start_time=None):
    base_time = start_time or datetime.now()
    return [(base_time + timedelta(seconds=i)).strftime("%d/%b/%Y:%H:%M:%S +0000") for i in range(num_lines)]

# Generate a random IP address
def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Generate access log entries
def generate_access_log(num_lines, start_time=None):
    methods = ["GET", "POST", "PUT", "DELETE"]
    urls = [
        "/index.html", "/login", "/dashboard", "/api/data", "/profile", "/settings", "/delete", "/search?q=test",
        "/contact", "/about", "/products", "/cart", "/checkout"
    ]
    statuses = [200, 201, 302, 404, 500, 403, 204]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
        "Mozilla/5.0 (Linux; Android 11)",
        "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
    ]
    timestamps = generate_timestamps(num_lines, start_time)

    return [
        f"{random_ip()} - - [{timestamps[i]}] \"{random.choice(methods)} {random.choice(urls)} HTTP/1.1\" {random.choice(statuses)} {random.randint(200, 2000)} \"http://example.com\" \"{random.choice(user_agents)}\""
        for i in range(num_lines)
    ]

# Generate error log entries
def generate_error_log(num_lines, start_time=None):
    error_levels = ["ERROR", "WARN", "INFO", "DEBUG", "CRITICAL"]
    error_messages = [
        "Client denied by server configuration",
        "File does not exist: /var/www/html/favicon.ico",
        "AH00126: Invalid URI in request GET / HTTP/1.1",
        "Connection reset by peer: mod_fcgid",
        "AH01630: client denied by server configuration",
        "Segmentation fault (core dumped)",
        "Memory allocation failed in mod_rewrite",
        "Disk quota exceeded",
        "SSL handshake failed: error:1408F10B:SSL routines:SSL3_GET_RECORD:wrong version number",
        "Could not establish connection to database"
    ]
    timestamps = generate_timestamps(num_lines, start_time)

    return [
        f"[{timestamps[i]}] [{random.choice(error_levels)}] {random.choice(error_messages)}"
        for i in range(num_lines)
    ]

# Get the last timestamp from a file or return None
def get_last_timestamp(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                timestamp = last_line.split('[')[1].split(']')[0]
                return datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
    except (IndexError, FileNotFoundError):
        pass
    return None

# Write logs to files for a specific server
def write_logs_for_server(server_name, num_lines=10000):
    server_directory = os.path.join(base_directory, server_name)
    os.makedirs(server_directory, exist_ok=True)

    access_log_path = os.path.join(server_directory, "access.log")
    error_log_path = os.path.join(server_directory, "error.log")

    # Get the last timestamps from existing logs or default to None
    access_last_time = get_last_timestamp(access_log_path)
    error_last_time = get_last_timestamp(error_log_path)

    # Generate logs starting from the last known timestamp
    access_logs = generate_access_log(num_lines, access_last_time)
    error_logs = generate_error_log(num_lines, error_last_time)

    # Append new logs to the files
    with open(access_log_path, 'a') as access_file:
        access_file.write("\n".join(access_logs) + "\n")

    with open(error_log_path, 'a') as error_file:
        error_file.write("\n".join(error_logs) + "\n")

# Main function to generate logs for multiple servers
def generate_logs_for_all_servers(num_servers=5, num_lines_per_file=10000):
    os.makedirs(base_directory, exist_ok=True)
    for i in range(1, num_servers + 1):
        server_name = f"apache_server_{i}"
        write_logs_for_server(server_name, num_lines_per_file)
    print(f"{num_lines_per_file} new log lines appended for {num_servers} servers.")

if __name__ == "__main__":
    generate_logs_for_all_servers()
