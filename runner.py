import os
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor

# # Generate script paths dynamically
# scripts = [f"main.py" for i in range(1, num_folders + 1)]

# start = time.time()
# for i, script in enumerate(scripts, start=1):
#     print(f"\n===== Running Day{i}/{script} =====")
#     result = subprocess.run(["python", -u, script], capture_output=True, text=True, cwd=f"Day{i}")
#     print(result.stdout)  # Print the output from the script
#     print(result.stderr)
#     if result.returncode != 0:
#         print(f"⚠️ Warning: {script} exited with return code {result.returncode}")
#     print(f"===== Finished {script} =====\n")
# print(f"Total time for all days is {(time.time()-start)*1000:.2f} ms.")


def run_script(day):
    script = f"Day{day}/main.py"
    result = subprocess.run(
        ["python", "-u", "main.py"],
        capture_output=True,
        text=True,
        cwd=f"Day{day}"
    )
    return f"\n===== Running {script} =====\n{result.stdout}{result.stderr}===== Finished {script} =====\n\n"


if __name__ == "__main__":
    # Count all directories in the current folder
    num_folders = len([d for d in os.listdir() if os.path.isdir(d) and d.startswith("Day")])

    # Run up to 5 scripts at a time
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(run_script, range(1, num_folders + 1)))

    # Print results
    for result in results:
        print(result)

    print(f"🚀 Total execution time: {time.time() - start_time:.3f} seconds")