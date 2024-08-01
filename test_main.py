import os
import subprocess
import pytest


@pytest.fixture
def csv_file_path():
    return "vehicles_fixed.csv"


@pytest.fixture
def main_script_path():
    return "main.py"


def test_main(csv_file_path, main_script_path):
    # Ensure the CSV file exists
    assert os.path.exists(csv_file_path), f"CSV file not found: {csv_file_path}"

    # Run the main script to preprocess and upload the CSV file
    result = subprocess.run(['python3', main_script_path, '-p', csv_file_path, '-v'], capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # Check if the script ran successfully
    assert result.returncode == 0, f"Main script failed with return code {result.returncode}"
    assert "Die CSV-Datei wurde vorverarbeitet und überschrieben" in result.stdout
    assert "Datei erfolgreich hochgeladen" in result.stdout


if __name__ == "__main__":
    pytest.main()
