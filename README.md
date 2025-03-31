# MIVAA Golden Zone

The **MIVAA Golden Zone** repository is the third phase in the MIVAA data processing pipeline, following the [MIVAA Bronze Zone](https://github.com/MIVAA-ai/mivaa-bronze-zone) and [MIVAA Golden Zone](https://github.com/MIVAA-ai/mivaa-golden-zone) repositories. This phase focuses on advanced data analytics and modeling to extract valuable insights from processed data.
---

## Prerequisites

1. **Download the Repository**:
   - [Clone](https://github.com/MIVAA-ai/mivaa-golden-zone.git) or download the repository as a [ZIP](https://github.com/MIVAA-ai/mivaa-golden-zone/archive/refs/heads/main.zip) file.

2. **Unzip the Repository**:
   - Extract the downloaded ZIP file to a folder on your system.

3. **Install Python**:
   - Ensure Python 3.9+ is installed on your machine. You can download Python [here](https://www.python.org/downloads/).

4. **Install Docker**:
   - Ensure Docker and Docker Compose are installed and running on your machine. You can download Docker [here](https://www.docker.com/).

---

## Steps to Run the Application Using the Startup Script

### 1. Configuration Setup
Before running the application, ensure the following configurations are correctly set:

#### A. OSDU Configuration

1. Navigate to `osdu-config/` (or move it to `config/` if needed).
2. Edit `osdu_client.py` to ensure correct API keys and endpoints.
3. Example:
```json
{
    "base_url": "https://osdu.example.com/api",
    "headers": {
        "accept": "application/json",
        "data-partition-id": "osdu",
        "Authorization": "Bearer ${OSDU_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
}
```

#### B. Project Configuration

Edit `config/project_config.py` to define project-wide settings and governance metadata.

##### Governance Metadata

**ACL (Access Control List)**:
- Defines who owns and who can view the data.
- Sourced dynamically from `PROJECT_CONFIG["ACL"]`
- Injected into every record before ingestion
- Can be customized per dataset, project, or environment

```json
"acl": {
  "owners": ["data.eng@company.com"],
  "viewers": ["geo.team@company.com"]
}
```

**Legal Tags**:
- Ensures compliance with data residency laws, GDPR, and internal ownership policies.
- Pulled from `PROJECT_CONFIG["LEGAL"]`

```json
"legal": {
  "legaltags": ["mivaa-northamerica"],
  "otherRelevantDataCountries": ["US"]
}
```

These governance settings ensure each record is aligned with corporate policies and global compliance requirements.

### 2. Setup the Environment

#### For Windows:
1. Open Command Prompt.
2. Navigate to the repository directory and run:
   ```cmd
   startup-windows.bat D:/MIVAA-ai/mivaa-golden-directory
   ```
   Replace `D:/MIVAA-ai/mivaa-golden-directory` with your desired base directory.

#### For Linux:
1. Open a terminal.
2. Navigate to the repository directory.
3. Make the script executable (only needed the first time):
   ```bash
   chmod +x startup-linux.sh
   ```
4. Run the command:
   ```bash
   ./startup-linux.sh /path/to/mivaa-golden-directory
   ```
   Replace `/path/to/mivaa-golden-directory` with your desired base directory.

### 3. Initialize the Database

Run the following command in your terminal:
```bash
python startup.py
```
This will initialize the database and prepare the application for use. Example log output:
```plaintext
INFO - Initialize the database from the JSON Schema file.
INFO - Database initialization completed successfully.
INFO - Starting application...
```

### 4. Start the Application Using Docker Compose

Run the following command to start the application:
```bash
docker-compose --env-file .env up --build
```

### Error Logging
Errors are logged in the database with severity levels (`WARNING`, `ERROR`). Detailed logs are generated to help users identify and resolve issues efficiently.

---

## Accessing Logs and Outputs

- **Uploads Directory**:
  Place your CSV files in the directory specified in the `UPLOADS_DIR` path in your `.env` file.
- **Processed Directory**:
  The validated and processed files will be saved in the directory specified in the `OUTPUT_DIR` path.
     The utility creates two processed files as follows:
     1. The first file contains the results of the data processed in bronze zone. File name ends with suffix "csv_validation_results"
     2. The second file contains the results of the data which has been evaluated for golden zone. File name ends with suffix "csv_golden_data_results".
- **Error Logs**:
  Detailed error logs are saved in the database and corresponding output folders for review.


---


## Project Structure

```
mivaa-golden-zone/
├── app.py                     # Main application script
├── bronze/                    # Bronze Zone data ingestion components
├── silver/                    # Silver Zone data transformation components
├── gold/                      # Golden Zone advanced analytics and modeling
├── config/                    # Configuration settings
│   ├── osdu_config.py         # Configuration for OSDU integration
│   ├── project_config.py      # Project-wide settings and environment variables
├── models/                    # Database models
├── crawler/                   # External data collection tools
├── file_processor/            # File parsing and format conversion utilities
├── osdu/                      # OSDU integration utilities
├── utils/                     # Helper functions and common utilities
├── logs/                      # Log files
├── uploads/                   # Uploads and staging
├── output/                    # Final processed outputs
├── sample-data/               # Sample input data
├── sample-data-output/        # Sample processed output data
├── docker/                    # Docker configuration (if separate Docker folder)
│   ├── Dockerfile             # Docker image setup
│   ├── docker-compose.yml     # Docker Compose settings
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── startup.py                 # Entry script for initializing pipelines
├── startup-linux.sh           # Shell script for Linux startup
├── startup-windows.bat        # Batch script for Windows startup
├── README.md                  # Project documentation
```

---

## Troubleshooting

- **Check Environment Variables**:
  Ensure the directories specified in the `.env` file exist and are accessible.
- **Inspect Docker Logs**:
  Run the following command to view Docker logs:
  ```bash
  docker-compose logs
  ```
- **Rebuild Containers**:
  If you encounter issues, rebuild the containers using:
  ```bash
  docker-compose --env-file .env up --build
  ```

---

## Additional Resources
- **Blog**: Read the detailed blog post about this application: 
- **Medallion Architecture**: Learn more about the principles of Medallion Architecture [here](https://deepdatawithmivaa.com/2024/12/03/unlocking-subsurface-insights-how-medallion-architecture-elevates-data-management-in-oil-and-gas/).
- **Bronze Zone**: Solution to validate data in bronze zone [here](https://deepdatawithmivaa.com/2025/01/15/bronze-zone-vol-1-medallion-architecture-for-osdu-data-ingestion-use-case/).
- **Silver Zone**: Solution to validate data in silver zone [here](https://deepdatawithmivaa.com/2025/02/16/silver-zone-vol-2-medallion-architecture-for-osdu-data-ingestion-use-case/).
---

## Notes

- This application requires Docker Compose.
- This application is currently tested in the windows environment, incase you face any issues running it in Linux, feel free to reach out.

Feel free to raise any issues or suggestions for improvement! Reach out at [info@deepdatawithmivaa.com](mailto:info@deepdatawithmivaa.com) for more help, comments, or feedback.
