import os

from config.logger_config import logger
from config.project_config import PROJECT_CONFIG
from utils.db_util import get_session
from utils.generate_sqlalchemy_model import generate_model_for_table
import pandas as pd

GoldTableModel = None
# Generate the SQLAlchemy model class dynamically for the 'field_bronze_table' table
try:
    if GoldTableModel is None:
        GoldTableModel = generate_model_for_table("gold_data")
        logger.info(f"Generated model class for table: {GoldTableModel.__tablename__}")
except Exception as e:
    logger.error(f"Error generating model class for table 'gold_data': {e}")
    # Ensure FieldSilverTableModel is defined as None if generation fails


def log_gold_data_table(df: pd.DataFrame, file_name):
    if isinstance(df, list):  # Convert list to DataFrame
        df = pd.DataFrame(df)

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected DataFrame, got {type(df)}")

    if df.empty:
        logger.error("Warning: DataFrame is empty! Nothing to log.")
        return

    if GoldTableModel is None:
        logger.error("GoldTableModel is not defined. Cannot log data.")
        return

    with get_session() as session:
        try:

            # Determine the starting ID for the new rows
            max_id = session.query(GoldTableModel.id).order_by(GoldTableModel.id.desc()).first()
            max_id = max_id[0] if max_id else 0

            # Add required columns to the DataFrame
            df["id"] = range(max_id + 1, max_id + 1 + len(df))

            # Convert response to a string to avoid list/dict issues
            df["response"] = df["response"].astype(str)

            # Convert NaN values to None explicitly
            df = df.astype(object).where(pd.notna(df), None)

            # Convert the DataFrame to a list of dictionaries
            data_to_insert = df.to_dict(orient="records")

            # Use bulk_insert_mappings for efficient insertion
            session.bulk_insert_mappings(GoldTableModel, data_to_insert)
            session.commit()
            logger.info("Gold data logged successfully.")

            # Ensure output directory exists
            output_dir = PROJECT_CONFIG.get("OUTPUT_DIRECTORY", "output")
            os.makedirs(output_dir, exist_ok=True)

            # Save the processed data to a CSV file
            result_file = f"{output_dir}/{file_name}_gold_data_results.csv"
            df.to_csv(result_file, index=False)
            logger.info(f"Results saved to '{result_file}'.")

        except Exception as e:
            logger.error(f"Error logging Gold data: {e}")
            session.rollback()
