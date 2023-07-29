from pathlib import Path
from zipfile import ZipFile
import time
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Assets Grabber has been activated.")

CURRENT_PATH = Path(__file__).parent
RESULTS_PATH = CURRENT_PATH / "results"
RESULTS_PATH.mkdir(exist_ok=True)
GLOBAL_START_TIME = time.time()
GLOBAL_TOTAL_FILE_COUNT = 0

for jar_path in (CURRENT_PATH / "mods").glob("*.jar"):
    process_start_time = time.time()
    jar_name = jar_path.name
    logging.info(f"Find {jar_name}, process start.")

    current_result_path = RESULTS_PATH / jar_name.split("-")[0]
    current_result_path.mkdir(exist_ok=True)
    total_file_count = 0

    with ZipFile(jar_path, "r") as jar:
        for member in jar.namelist():
            if not member.endswith("/") and member.startswith("assets/"):
                current_file_path = current_result_path / member
                current_file_path.parent.mkdir(parents=True, exist_ok=True)
                jar.extract(member, current_file_path)
                total_file_count += 1
                GLOBAL_TOTAL_FILE_COUNT += 1
    if not [*current_result_path.iterdir()]:
        current_result_path.rmdir()
        logging.info(f"The result of process {jar_name} is empty, delete the directory")
    logging.info(
        f"Process {jar_name} completed in {round(time.time() - process_start_time, 3)} seconds, totaling {total_file_count} files."
    )

logging.info(
    f"All processes have been completed in {round(time.time() - GLOBAL_START_TIME, 3)} seconds, totaling {GLOBAL_TOTAL_FILE_COUNT} files."
)
