import os
import shutil
import urllib.request
import zipfile
import json
from pathlib import Path
from typing import Dict, List, Any

from schema_engine import SchemaEngine
from sqlalchemy import create_engine
from utils import write_jsonl_file


def download_with_progress(url: str, path: Path) -> None:
    """Download file with progress bar."""
    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, (downloaded * 100) // total_size)
            downloaded_mb = downloaded / (1024 * 1024)
            total_mb = total_size / (1024 * 1024)
            print(f"\rProgress: {percent}% ({downloaded_mb:.1f}/{total_mb:.1f} MB)", end="", flush=True)
    
    urllib.request.urlretrieve(url, path, reporthook=show_progress)
    print()  # New line after progress


def extract_and_organize_files(data_dir: Path) -> None:
    """Extract dataset and organize files into expected structure."""
    # zip_path = data_dir / "dev.zip"
    extracted_dir = data_dir / "dev_corrected"
    
    # Extract main dataset
    # if not extracted_dir.exists():
    #     print("Extracting dataset...")
    #     with zipfile.ZipFile(zip_path, "r") as zip_ref:
    #         zip_ref.extractall(data_dir)
    
    # Copy and rename main files
    file_mappings = [
        ("dev.json", "test_all.json"),
        ("dev_tables.json", "test_tables.json"),
        ("dev.sql", "test_gold_sqls.txt"),
    ]
    
    for source, dest in file_mappings:
        src_path = extracted_dir / source
        dest_path = data_dir / dest
        if src_path.exists() and not dest_path.exists():
            shutil.copy2(src_path, dest_path)
    
    # Extract and rename database files
    db_dest = data_dir / "test_databases"
    if not db_dest.exists():
        # db_zip = extracted_dir / "dev_databases.zip"
        # if db_zip.exists():
        #     print("Extracting database files...")
        #     with zipfile.ZipFile(db_zip, "r") as zip_ref:
        #         zip_ref.extractall(data_dir)
        #     (data_dir / "dev_databases").rename(db_dest)
        (extracted_dir / "dev_databases").rename(db_dest)
    
    # Cleanup temporary files
    # zip_path.unlink(missing_ok=True)
    # shutil.rmtree(extracted_dir, ignore_errors=True)


def generate_database_schema(db_path: str, db_id: str) -> None:
    """Generate and cache database schema in mschema format."""
    mschema_path = db_path + ".mschema"
    
    if not os.path.exists(mschema_path):
        db_engine = create_engine(f"sqlite:///{db_path}")
        schema_engine = SchemaEngine(engine=db_engine, db_name=db_id)
        mschema_str = schema_engine.mschema.to_mschema()
        
        with open(mschema_path, "w", encoding="utf-8") as f:
            f.write(mschema_str)


def process_dataset_entries(data: List[Dict[str, Any]], data_dir: str) -> List[Dict[str, Any]]:
    """Add required metadata fields to dataset entries."""
    for i, entry in enumerate(data):
        # Add database path
        entry["db_path"] = str(
            Path(data_dir) / "test_databases" / entry["db_id"] / f"{entry['db_id']}.sqlite"
        )
        
        # Add missing fields with defaults
        entry.setdefault("question_id", str(i))
        entry.setdefault("difficulty", "easy")
        entry.setdefault("SQL", "")
    
    return data


def preprocess_data(data_dir: Path) -> None:
    """Process dataset entries and generate database schemas."""
    # Load dataset
    data_file = data_dir / "test_all.json"
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Processing {len(data)} entries...")
    
    # Add metadata to entries
    data = process_dataset_entries(data, str(data_dir))
    
    # Generate schemas for unique databases
    db_paths = {entry["db_id"]: entry["db_path"] for entry in data}
    print(f"Generating schemas for {len(db_paths)} databases...")
    
    for i, (db_id, db_path) in enumerate(db_paths.items(), 1):
        if os.path.exists(db_path):
            print(f"[{i}/{len(db_paths)}] {db_id}")
            generate_database_schema(db_path, db_id)
        else:
            print(f"Warning: Database not found: {db_path}")
    
    # Save processed data
    output_file = data_dir / "test_all.jsonl"
    write_jsonl_file(str(output_file), data)
    print(f"Saved processed data to {output_file}")


def setup_bird_dataset(data_dir: str = "data") -> None:
    """
    Download, extract, and preprocess the BIRD benchmark dataset.
    
    This function:
    1. Downloads the BIRD development dataset
    2. Extracts and organizes files
    3. Generates database schemas
    4. Creates processed JSONL output
    
    Args:
        data_dir: Directory to store the dataset (default: "data")
    """
    data_dir = Path(data_dir)
    # data_dir.mkdir(exist_ok=True)
    
    print("=== BIRD Dataset Setup ===")
    
    # Step 1: Download dataset
    # zip_path = data_dir / "dev.zip"
    # if not zip_path.exists():
    #     print("Downloading BIRD dataset...")
    #     download_with_progress(
    #         "https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip",
    #         zip_path
    #     )
    
    # Step 2: Extract and organize files
    extract_and_organize_files(data_dir)
    
    # Step 3: Process data and generate schemas
    preprocess_data(data_dir)
    
    print("✓ Dataset setup complete!")


if __name__ == "__main__":
    setup_bird_dataset()
