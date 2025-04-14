import subprocess

def build():
    """
    Build the project using Poetry.
    """
    print("Building the project...")
    subprocess.run(["pip", "install","-r","requirements.txt"], check=True)
    print("Dependencies Installed successfully.")
    subprocess.run(["python", "src/components/data_ingestion.py"], check=True)
    print("Data Ingestion completed successfully.")
    print("All Datasets are ready to use.")

build()