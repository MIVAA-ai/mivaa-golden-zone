# MIVAA Golden Zone

The **MIVAA Golden Zone** repository is the third phase in the MIVAA data processing pipeline, following the [MIVAA Bronze Zone](https://github.com/MIVAA-ai/mivaa-bronze-zone) and [MIVAA Silver Zone](https://github.com/MIVAA-ai/mivaa-silver-zone) repositories. This phase focuses on advanced data analytics and modeling to extract valuable insights from processed data.

## Project Structure

The repository is organized into the following directories and files:

- **`bronze/`**: Contains scripts and resources related to the initial data ingestion and validation phase.
- **`silver/`**: Houses components for data transformation and enrichment processes.
- **`gold/`**: Dedicated to advanced data analytics and modeling to extract valuable insights.
- **`config/`**: Configuration files for various environments and settings.
- **`crawler/`**: Tools and scripts for data collection from external sources.
- **`file_processor/`**: Utilities for processing and managing files.
- **`models/`**: Machine learning models and related resources.
- **`osdu/`**: Integration components for the Open Subsurface Data Universe (OSDU) platform.
- **`utils/`**: Helper functions and utilities used across the project.
- **`app.py`**: The main application script to initiate the data processing pipeline.
- **`requirements.txt`**: Lists the Python dependencies required for the project.

## Getting Started

To set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MIVAA-ai/mivaa-golden-zone.git
   cd mivaa-golden-zone
   ```

2. **Install Dependencies**:
   It's recommended to use a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and define necessary environment variables as specified in the `config/` directory.

4. **Run the Application**:
   ```bash
   python app.py
   ```

## Contributing

We welcome contributions to enhance the MIVAA Golden Zone project. Please follow the guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the [MIT License](LICENSE).

---

*Note: For detailed information on the preceding phases of the MIVAA data processing series, refer to the [MIVAA Bronze Zone](https://github.com/MIVAA-ai/mivaa-bronze-zone) and [MIVAA Silver Zone](https://github.com/MIVAA-ai/mivaa-silver-zone) repositories.*
