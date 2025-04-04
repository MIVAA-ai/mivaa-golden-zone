# Configuration settings

PROJECT_CONFIG = {
  "IGNORE_BRONZE_WARNING": True,
  "IGNORE_SILVER_WARNING": True,
  "ACL": {},
  "LEGAL": {},
  "LEGAL": {},
  "SQL_TABLES": {
    "FIELD": {
      "BRONZE_TABLE": "field_bronze_data",
      "SILVER_TABLE": "field_silver_data"
    }
  },
  "MASTER_DATA_KINDS": {
    "CRS": "osdu:wks:reference-data--CoordinateReferenceSystem:1.1.0",
    "FIELD": "osdu:wks:master-data--Field:1.*.*"
  },
  "TO_CRS": "{\"authCode\":{\"auth\":\"EPSG\",\"code\":\"4326\"},\"name\":\"GCS_WGS_1984\",\"type\":\"LBC\",\"ver\":\"PE_10_3_1\",\"wkt\":\"GEOGCS[\\\"GCS_WGS_1984\\\",DATUM[\\\"D_WGS_1984\\\",SPHEROID[\\\"WGS_1984\\\",6378137.0,298.257223563]],PRIMEM[\\\"Greenwich\\\",0.0],UNIT[\\\"Degree\\\",0.0174532925199433],AUTHORITY[\\\"EPSG\\\",4326]]\"}"
}



