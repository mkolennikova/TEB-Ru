import subprocess
import os
from collections import deque
from IPython.display import clear_output  # only for Jupyter/Colab

def run_executable(exe_path, log_file, num_lines=3, cwd=None, args=None):
    """
    Run an executable, capture its output to a log file, and display the last
    `num_lines` lines in real-time (updated in the same cell).

    Args:
        exe_path (str): Path to the executable.
        log_file (str): Name/path of the log file to write full output to.
        num_lines (int): Number of recent lines to display on screen (default 3).
        cwd (str, optional): Working directory for the process (default: current).
        args (list, optional): Additional command-line arguments.

    Returns:
        int: The return code of the process.
    """
    # Build the full command list
    cmd = [exe_path] + (args if args else [])

    # Open the log file (overwrite if exists)
    with open(log_file, 'w', encoding='utf-8') as log_f:
        # Start the process, merging stdout and stderr
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            bufsize=0          # unbuffered for byte-by-byte reading
        )

        # Buffer for the current line (between \r or \n)
        current_line = ""
        # Deque to keep the last `num_lines` lines for display
        last_lines = deque(maxlen=num_lines)

        def update_display():
            """Refresh the cell output with the latest lines."""
            clear_output(wait=True)
            # Show only the most recent lines (last `num_lines`)
            for line in list(last_lines)[-num_lines:]:
                print(line)

        # Read the output byte by byte to handle both \r and \n properly
        while True:
            chunk = proc.stdout.read(1)
            if not chunk:
                break
            try:
                char = chunk.decode('utf-8', errors='ignore')
            except UnicodeDecodeError:
                continue

            if char == '\r':
                # Carriage return – finalise the current line (progress update)
                if current_line:
                    # Write to log file (each update as a separate line)
                    log_f.write(current_line + '\n')
                    log_f.flush()
                    # Store and update the display
                    last_lines.append(current_line)
                    update_display()
                    current_line = ""
            elif char == '\n':
                # Newline – finalise the line if it has content
                if current_line:
                    log_f.write(current_line + '\n')
                    log_f.flush()
                    last_lines.append(current_line)
                    update_display()
                    current_line = ""
                else:
                    # Empty line – just write a newline to the log
                    log_f.write('\n')
                    log_f.flush()
            else:
                # Ordinary character – accumulate to the current line
                current_line += char

        # Process finished – handle any remaining output
        if current_line:
            log_f.write(current_line + '\n')
            log_f.flush()
            last_lines.append(current_line)
            update_display()

        # Wait for the process to finish and get its return code
        return_code = proc.wait()

    # Final screen update: show the last lines and a completion message
    clear_output(wait=True)
    for line in list(last_lines)[-num_lines:]:
        print(line)
    print(f"✅ Process finished (return code {return_code}). Full log saved to '{log_file}'.")
    return return_code