import subprocess
import os
from collections import deque
from IPython.display import clear_output  # only for Jupyter/Colab

def run_and_log(exe_path, log_file, num_lines=3, cwd=None, args=None,
                update_every_n_lines=5, use_carriage_return_handling=False):
    """
    Run a command, log all output to a file, and display the last `num_lines`
    lines in the Jupyter/Colab cell, updating periodically.

    For commands that output progress using `\r` (e.g., long-running simulators),
    set use_carriage_return_handling=True (default) to capture every update.
    For commands that output plain lines with `\n` (e.g., make, compilers),
    set use_carriage_return_handling=False, and the display will update every
    `update_every_n_lines` new lines to reduce flickering.

    Args:
        exe_path (str): Path to the executable/command.
        log_file (str): File to save the full output.
        num_lines (int): Number of recent lines to show on screen.
        cwd (str, optional): Working directory.
        args (list, optional): Additional arguments.
        update_every_n_lines (int): Update screen every N new lines (only for
                                    normal `\n` output, ignored if \r handling).
        use_carriage_return_handling (bool): If True, handle `\r` byte-by-byte
                                             (for progress bars). If False,
                                             read line-by-line.

    Returns:
        int: Return code of the process.
    """
    cmd = [exe_path] + (args if args else [])

    with open(log_file, 'w', encoding='utf-8') as log_f:
        if use_carriage_return_handling:
            # ---- Byte-by-byte reading for progress bars with \r ----
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=cwd,
                bufsize=0
            )
            current_line = ""
            last_lines = deque(maxlen=num_lines)

            def update_display():
                clear_output(wait=True)
                for line in list(last_lines)[-num_lines:]:
                    print(line)

            while True:
                ch = proc.stdout.read(1)
                if not ch:
                    break
                try:
                    char = ch.decode('utf-8', errors='ignore')
                except UnicodeDecodeError:
                    continue

                if char == '\r':
                    if current_line:
                        log_f.write(current_line + '\n')
                        log_f.flush()
                        last_lines.append(current_line)
                        update_display()
                        current_line = ""
                else:
                    current_line += char

            if current_line:
                log_f.write(current_line + '\n')
                log_f.flush()
                last_lines.append(current_line)
                update_display()

            return_code = proc.wait()

        else:
            # ---- Line-by-line reading for normal \n output ----
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=cwd,
                text=True,
                bufsize=1
            )
            last_lines = deque(maxlen=num_lines)
            line_counter = 0

            for line in proc.stdout:
                # Write to log immediately
                log_f.write(line)
                log_f.flush()

                # Strip newline and store
                stripped = line.rstrip('\n')
                if stripped:
                    last_lines.append(stripped)
                    line_counter += 1

                # Update screen every N lines
                if line_counter % update_every_n_lines == 0:
                    clear_output(wait=True)
                    for l in list(last_lines)[-num_lines:]:
                        print(l)

            # Final update after process ends
            clear_output(wait=True)
            for l in list(last_lines)[-num_lines:]:
                print(l)
            return_code = proc.wait()

    # Print final completion message
    print(f"✅ Process finished (return code {return_code}). Full log saved to '{log_file}'.")
    return return_code