# 🧠 MRI Request Module

This module collects participant T1-weighted (T1w) MRI scans from a BIDS-compliant directory and packages them into a `.zip` file. The resulting archive can be viewed directly in a web browser using the included HTML viewer.

---

## 🚀 Quick Start

### Python Dependencies
- Python **3.10** or higher with the following packages:
    - pybids==0.15.2   
### 📁 Required Inputs

- A BIDS-formatted dataset
- A `study_info.json` file with project metadata

---

## 📝 Step-by-Step Instructions

### Step 0: Create python virtual environment and install package
python -m venv virtual_env 
source virtual_env/bin/activate 
pip install pybids=0.15.2

### Step 1: Edit the `study_info.json` File

Fill in the relevant study information:

```json
{
    "study_id": "STUDY_ID",           // Your project ID
    "study_name": "STUDY NAME",       // Short description of the study
    "pi_name": "PI NAME",             // Principal Investigator's full name
    "pi_email": "PI EMAIL",           // PI's email address
    "lab_email": "LAB EMAIL"          // RA or lab contact email
}

```
Example:

```json
{
    "study_id": "PSIBD",
    "study_name": "Psilocybin-Assisted Psychotherapy for Treatment-Resistant Depression Study",
    "pi_name": "Dr. Husain, Ishrat",
    "pi_email": "ishrat.husain@camh.ca",
    "lab_email": "thomas.tan@camh.ca"
  }
```

### Step 2: Run the main script
Run the script using the following command:
```bash
python patient_mri_request.py [BIDS_DIR] [STUDY_ID] \
       --subject_id [SUBJECT_ID] \
       --session_id [SESSION_ID] \
       --scan_date [YYYYMMDD] \
       --create_date [YYYYMMDD]
```
**Example**:
```bash
python patient_mri_request.py /archive/data/PSIOCD/data/bids PSIOCD \
       --subject_id CMH0001 \
       --session_id 01 \
       --scan_date 20250601 \
       --create_date 20250714
```

## 📊 Output Files

After running the script, you’ll find:

 - A .zip archive in the zips/ directory containing the selected T1w image(s)

 - The zip file is viewable using the included HTML file (local_viewer.html)

### 📁 Example Directory Structure
```bash
mri_request/
    ├── patient_mri_request.py
    ├── study_info/
    │   └── study_info.json
    ├── nii_template/
    │   ├── local_viewer.html
    │   ├── static/
    │   └── README.md
    │   └── images/
    ├── zips/
    │   └── TEST_CMH0001_01.zip
```