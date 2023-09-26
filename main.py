import os
import time
import threading
import subprocess
import psutil

# Set the path where XMRIG is located
XMRIG_PATH = os.environ.get('XMRIG_PATH')
PROCESS_PATH = os.path.join(XMRIG_PATH, 'xmrig')

# Global variable to hold the subprocess instance
subprocess_instance = None


def log_output(process, duration):
    """
    Log the standard output of a subprocess for a given duration.

    :param process: The subprocess object
    :param duration: Time in seconds for which to log output
    """
    if not process:
        print("Process not running. Cannot log output.")
        return

    start_time = time.time()
    print("LOGGING XMRIG OUTPUT")

    while time.time() - start_time < duration:
        line = process.stdout.readline()
        if line:
            print(line.strip())


def get_idle_time():
    """
    Calculate the system idle time using xprintidle.

    :return: Idle time in seconds
    """
    try:
        # Fetch idle time in milliseconds
        idle_time_ms = int(subprocess.check_output(['xprintidle']).strip())
        print(idle_time_ms / 1000.0)
        return idle_time_ms / 1000.0

    except Exception as e:
        print(f"Error: {e}")
        return 0


def should_start_process():
    """
    Determine whether the process should be started based on idle time.

    :return: True if idle time is more than 5 minutes, False otherwise
    """
    return get_idle_time() > 60 *5


def is_process_running(process_path):
    """
    Check if a process is running based on its executable path.

    :param process_path: The path to the process executable
    :return: True if the process is running, False otherwise
    """
    for process in psutil.process_iter(['pid', 'name', 'exe']):
        if process.info['exe'] == process_path:
            return True
    return False


def start_process():
    """
    Start the subprocess and store its instance in a global variable.
    """
    global subprocess_instance
    subprocess_instance = subprocess.Popen(
        [PROCESS_PATH],
        cwd=XMRIG_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print("Process started.")


def stop_process():
    """
    Stop the running subprocess.
    """
    global subprocess_instance
    if subprocess_instance:
        subprocess_instance.kill()
        subprocess_instance = None
    else:
        for process in psutil.process_iter(['pid', 'name', 'exe']):
            if process.info['exe'] == PROCESS_PATH:
                psutil.Process(process.info['pid']).kill()
    print("Process stopped.")


def main():
    """
    Main loop to control starting and stopping the subprocess.
    """
    print("Starting application")

    while True:
        if should_start_process() and not is_process_running(PROCESS_PATH):
            start_process()

        if not should_start_process() and is_process_running(PROCESS_PATH):
            stop_process()

        if is_process_running(PROCESS_PATH):
            print("Process is running.")
            threading.Thread(target=log_output, args=(subprocess_instance, 1)).start()

        time.sleep(5)


if __name__ == "__main__":
    main()
