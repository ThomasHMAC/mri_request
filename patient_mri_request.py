import os
import shutil
import fileinput
import zipfile
import argparse
from bids import BIDSLayout
from config import validate_study_info

import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NII_TEMPLATE_DIR = os.path.join(BASE_DIR, "nii_template")
STUDY_INFO_DIR = os.path.join(BASE_DIR, "study_info")


def collect_subject_data(bids_dir, subject_id, session_id, scan_date, create_date, study_info):
    study_id = study_info["study_id"]
    study_name = study_info["study_name"]
    pi_name = study_info["pi_name"]
    pi_email = study_info["pi_email"]
    lab_email = study_info["lab_email"]

    if not isinstance(scan_date, str):
        scan_date = scan_date.isoformat()

    if not isinstance(create_date, str):
        create_date = create_date.isoformat()

    layout = BIDSLayout(
            bids_dir,
            validate=False,
            ignore=[f'(?!sub-{subject_id}).*']
        )
    t1w_imgs = layout.get(
            extension="nii.gz",
            suffix="T1w",
            subject=subject_id,
            session=session_id,
        )
    t1w_jsons = layout.get(
        extension="json",
        suffix="T1w",
        subject=subject_id,
        session=session_id,
    )

    if not t1w_imgs:
        raise FileNotFoundError(f"No T1w images found for sub-{subject_id}, ses-{session_id}")
    if not t1w_jsons:
        raise FileNotFoundError(f"No JSON files found for sub-{subject_id}, ses-{session_id}")
       
    t1w = t1w_imgs[0].path
    t1w_json = t1w_jsons[0].path
    # Compose output directory with study_id included
    subid = f"{study_id}_{subject_id}_{session_id}"
    OUT_DIR = os.path.join(BASE_DIR, "transfer_file", subid)

    # Create output directories
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    # Copy template
    for item in os.listdir(NII_TEMPLATE_DIR):
        source_item = os.path.join(NII_TEMPLATE_DIR, item)
        dest_item = os.path.join(OUT_DIR, item)
        if os.path.isdir(source_item):
            shutil.copytree(source_item, dest_item)
        else:
            shutil.copy2(source_item, dest_item)

    output_nii_path = os.path.join(OUT_DIR, "data", "T1w.nii.gz")
    output_json_path = os.path.join(OUT_DIR, "data", "T1w.json")
    
    shutil.copy2(t1w, output_nii_path)
    shutil.copy2(t1w_json, output_json_path)

    # Update README
    readme_path = os.path.join(OUT_DIR, "README.md")
    with fileinput.FileInput(readme_path, inplace=True) as file:
        for line in file:
            line = line.replace("rep_create_date", create_date)
            line = line.replace("rep_scan_date", scan_date)
            line = line.replace("rep_study_name", study_name)
            line = line.replace("rep_pi_name", pi_name)
            line = line.replace("rep_pi_email", pi_email)
            line = line.replace("rep_lab_email", lab_email)
            print(line, end="")

    # Compress the folder
    output_zip = OUT_DIR + ".zip"
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(OUT_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, OUT_DIR)
                zipf.write(file_path, arcname)

    # Move zip to current directory
    zips_dir = os.path.join(BASE_DIR, "zips")
    os.makedirs(zips_dir, exist_ok=True)
    shutil.move(output_zip, os.path.join(zips_dir, os.path.basename(output_zip)))
    print(f"[✓] Created package: {os.path.basename(output_zip)}")

def valid_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{date_str}'. Expected YYYYMMDD.")
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Collect and package subject data from BIDS")
    parser.add_argument('bids_dir', help='Study BIDS directory (e.g., /archive/data/PSIBD/data/bids)')
    parser.add_argument('study_id', help='Study ID code(e.g., PSIBD)')
    parser.add_argument('--subject_id', metavar='SUBJECT', required=True, help='BIDS Subject ID (e.g., CMH0004)')
    parser.add_argument('--session_id', metavar='SESSION', required=True, help='BIDS Session ID (e.g., 01)')
    parser.add_argument('--scan_date', metavar='DATE', required=True, type=valid_date, help='Scan date (e.g., 20250601)')

    args = parser.parse_args()
    # Load study_info JSON dynamically
    study_info_path = os.path.join(BASE_DIR, "study_info", f"{args.study_id}.json")
    study_info = validate_study_info(study_info_path)
    current_datetime = datetime.now()
    create_date = current_datetime.strftime("%Y-%m-%d")

    # Run main function
    collect_subject_data(
        bids_dir=args.bids_dir,
        subject_id=args.subject_id,
        session_id=args.session_id,
        scan_date=args.scan_date,
        create_date=create_date,
        study_info=study_info
    )
