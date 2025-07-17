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
```bash
python -m venv mri_request_env 
source mri_request_env/bin/activate 
pip install pybids==0.15.2
```
### Step 1: Edit the `study_info.json` File

Create a JSON file named after your **study ID** inside the `study_info/` folder (e.g., `PSIBD.json`, `ASCEND.json`).

Fill it with the following metadata:

```json
{
  "study_id": "STUDY_ID",
  "study_name": "STUDY NAME",
  "pi_name": "PI NAME",
  "pi_email": "PI EMAIL",
  "lab_email": "LAB EMAIL"
}
```

#### Key	Description:
| Parameter     | Description                                        |
|---------------|----------------------------------------------------|
| `study_id`    | Your project ID.                                   |
| `study_name`  | Short description of the study.                    |
| `pi_name`     | Principal Investigator's full name.                |
| `pi_email`    | PI's email address.                                |
| `lab_email`   | RA or lab contact email address.   |

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
python run.py <BIDS_DIR> <STUDY_ID> \
       --subject_id <SUBJECT_ID> \
       --session_id <SESSION_ID> \
       --scan_date <YYYYMMDD> \
       --create_date <YYYYMMDD>

```
**Example**:
```bash
python run.py /archive/data/PSIOCD/data/bids PSIOCD \
       --subject_id CMH0001 \
       --session_id 01 \
       --scan_date 20250601 \
       --create_date 20250714
```

## 📊 Output Files

After running the script, you’ll find:

 - A .zip archive in the zips/ directory containing the selected T1w image(s)

 - This zip file is intended to be sent to the **requester**.

 - Inside the archive, there is a README.md file with instructions on how to view the image using the included HTML viewer (local_viewer.html), which can be opened in a web browser.

 - ⚠️ Reminder: The requester must unzip the archive before opening local_viewer.html, or the viewer will not work properly.

### 📁 Example Directory Structure
```bash
mri_request/
    ├── config.py
    ├── nii_template
    │   ├── data
    │   ├── images
    │   ├── local_viewer.html
    │   ├── README.md
    │   └── static
    ├── README.md
    ├── run.py
    ├── study_info
    │   ├── ASCEND.json
    │   └── PSIBD.json
    ├── transfer_file
    │   ├── ASCEND_CMH0045_01
    │   └── PSIBD_CMH0004_01
    └── zips
        ├── ASCEND_CMH0045_01.zip
        └── PSIBD_CMH0004_01.zip
```