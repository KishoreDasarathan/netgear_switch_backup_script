import paramiko
import time
import os
from datetime import datetime

# SSH connection details
HOST = "10.1.1.11"
USERNAME = "admin"
PASSWORD = "pass"
ENABLE_PASSWORD = "your_enable_password"  # Set your enable password here, if needed

# Folder where you want to save backup (with dynamic folder structure)
BACKUP_BASE_FOLDER = r"E:\SWITCH"

# Create folder structure based on current date
date_str = datetime.now().strftime('%d-%m-%Y')  # Format: 27-04-2025
backup_folder = os.path.join(BACKUP_BASE_FOLDER, f"SWITCH-{date_str}")
os.makedirs(backup_folder, exist_ok=True)

# File name format (IP address + date_time)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
FILENAME = os.path.join(backup_folder, f"{HOST}_{timestamp}.cfg")

# Connect to the device
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USERNAME, password=PASSWORD, look_for_keys=False, allow_agent=False)

# Open shell
ssh_shell = client.invoke_shell()
time.sleep(1)

# Clear initial messages
if ssh_shell.recv_ready():
    ssh_shell.recv(1000).decode('utf-8')  # Discard the initial messages

# Send 'enable' command to enter privileged mode (if required)
ssh_shell.send('enable\n')
time.sleep(1)

# If the device asks for an enable password, send it
if ssh_shell.recv_ready():
    enable_output = ssh_shell.recv(1000).decode('utf-8')
    if "Password:" in enable_output:
        ssh_shell.send(ENABLE_PASSWORD + "\n")
        time.sleep(1)

# Now we’ll try to send commands and capture their responses.
commands = [
    'show running-config',  # We want to retrieve the configuration
    'show startup-config',  # Backup startup configuration, if running-config fails
    'show version',  # Additional command to retrieve version if needed
]

full_output = ""

for command in commands:
    ssh_shell.send(command + '\n')
    time.sleep(2)

    output = ""
    while True:
        # If data is received, capture it
        if ssh_shell.recv_ready():
            output_chunk = ssh_shell.recv(5000).decode('utf-8')
            output += output_chunk
            
            if "--More--" in output_chunk:
                # If there's a "more" prompt, send space to continue
                ssh_shell.send(" ")
                time.sleep(1)
            elif "#" in output_chunk or ">" in output_chunk:
                # Detect the prompt and break (indicates end of output)
                break
        else:
            time.sleep(1)  # Wait a bit before retrying if no data is ready

    # Save the output if we received something
    if output:
        full_output += output

# Save the final collected output to a file
if full_output:
    with open(FILENAME, "w", encoding="utf-8") as f:
        f.write(full_output)
    print(f"✅ Backup completed. File saved to: {FILENAME}")
else:
    print("❌ No configuration output received.")

# Close connection
client.close()
