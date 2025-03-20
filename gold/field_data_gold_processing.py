from config.project_config import PROJECT_CONFIG
from models.field_silver_data import fetch_silver_results_by_file_id
from config.logger_config import logger
import json
import pandas as pd

from models.gold_data import log_gold_data_table
from osdu.osdu_client import OSDUClient

client = OSDUClient()

def fetch_and_filter_silver_data(file_id):
    """
    Fetch field data from the silver table and filter out rows based on severity.

    Parameters:
    - file_id (int): The unique file identifier.

    Returns:
    - DataFrame: The filtered data.
    """
    df = fetch_silver_results_by_file_id(file_id)

    # Apply filtering based on configuration
    if PROJECT_CONFIG["IGNORE_SILVER_WARNING"]:
        df = df[df['error_severity'].fillna('') != 'ERROR']
    else:
        df = df[~df['error_severity'].fillna('').isin(['ERROR', 'WARNING'])]

    # Log if no data is available after filtering
    if df.empty:
        logger.warning(f"No valid data found for file ID {file_id}. Processing stopped.")

    return df

def convert_row_to_osdu_format(row):
    osdu_json = {
        "kind": "osdu:wks:master-data--Field:1.1.0",
        "acl": PROJECT_CONFIG["ACL"],
        "legal": PROJECT_CONFIG["LEGAL"],
        "ancestry": {"parents": [row.ParentFieldOSDUId] if pd.notnull(row.ParentFieldOSDUId) else []},
        "meta": [json.loads(row.CRS)] if pd.notnull(row.CRS) else [],
        "data": {
            "Source": row.Source if pd.notnull(row.Source) else "Example Data Source",
            "SpatialLocation": {
                "AsIngestedCoordinates": json.loads(row.AsIngestedCoordinates) if pd.notnull(row.AsIngestedCoordinates) else {},
                "Wgs84Coordinates": json.loads(row.Wgs84Coordinates) if pd.notnull(row.Wgs84Coordinates) else {},
                "AppliedOperations": [],
                "SpatialParameterTypeID": ""
            },
            "FieldID": str(row.id),
            "FieldName": row.FieldName,
            "FieldDescription": "Example FieldDescription",
            "EffectiveDate": row.DiscoveryDate.isoformat() if pd.notnull(row.DiscoveryDate) else None,
            "TerminationDate": None,
            "ExtensionProperties": {}
        }
    }

    # Optional CRS parsing with None check:
    if pd.notnull(row.CRS):
        crs_data = json.loads(row.CRS)
        osdu_json["data"]["SpatialLocation"]["AsIngestedCoordinates"]["persistableReferenceCrs"] = crs_data.get("persistableReference", "")

    return [osdu_json]


def ingest_into_osdu(silver_row, payload, file_name):
    df_gold_data = pd.DataFrame([{
        "file_id": silver_row.file_id,
        "name": silver_row.FieldName
    }])

    try:
        record = client.storage(payload)

        # Extract the first record ID from response
        osdu_record_id = record.get("recordIds", [None])[0]

        df_gold_data["success"] = "TRUE"
        df_gold_data["osdu_record_id"] = osdu_record_id
        df_gold_data["response"] = json.dumps(record)  # Store full response as a JSON string
    except Exception as e:
        df_gold_data["success"] = "FALSE"
        df_gold_data["osdu_record_id"] = None
        df_gold_data["response"] = str(e)  # Convert error to string

    return df_gold_data


def process_single_field(silver_row, file_name):
    # Display all columns
    pd.set_option('display.max_columns', None)
    converted_json = convert_row_to_osdu_format(silver_row)
    return ingest_into_osdu(silver_row, converted_json, file_name)

def process_field_data_for_gold_zone(file_id, file_name):
    df = fetch_and_filter_silver_data(file_id)

    if df.empty:
        return pd.DataFrame()  # Return an empty DataFrame if no valid data is found

    all_results = []

    for row in df.itertuples():
        result_df = process_single_field(row, file_name)
        all_results.append(result_df)

    if all_results:  # Ensure there is data before concatenating
        df_gold_data = pd.concat(all_results, ignore_index=True)
        log_gold_data_table(df_gold_data, file_name)  # Pass DataFrame instead of list
    else:
        df_gold_data = pd.DataFrame()

    return df_gold_data


