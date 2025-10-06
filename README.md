# NASA_NEO_MINI_PROJECT

This project retrieves, processes, and stores Near-Earth Object (NEO) data using NASA's public API, and demonstrates how to store the results in a local MySQL database for further analysis.

## Overview

The Jupyter Notebook (`nasa_neo_project.ipynb`) automates the following tasks:
- Fetches Near Earth Object data for a given date range using the NASA API.
- Parses and organises asteroid data, including physical properties and close approach details.
- Stores the processed data in a local MySQL database, with separate tables for asteroid properties and close approach data.
- Demonstrates simple querying of the database to view stored results.

## Workflow

1. **Install Dependencies**  
   Required Python packages:  
   - `requests` (for API calls)  
   - `pandas` and `numpy` (for data manipulation)  
   - `pymysql` (for MySQL connectivity)

2. **Fetch Data from NASA API**  
   - Uses an API key to request NEO data for a set date range.
   - Collects details such as name, magnitude, estimated diameter, hazardous status, and close approach parameters.

3. **Data Parsing**  
   - Extracts relevant fields and structures them into Python dictionaries and Pandas DataFrames.

4. **Database Storage**  
   - Connects to a local MySQL server.
   - Creates a database and tables (`ASTEROID` and `CLOSE_APPROACH_DATA`).
   - Inserts parsed data into these tables.

5. **Verification**  
   - Executes SQL queries to verify that data has been inserted correctly.

## Requirements

- Python 3.12+
- MySQL server (local instance)
- Python packages:  
  `requests`, `pandas`, `numpy`, `pymysql`

Install packages using:
```bash
pip install requests pandas numpy pymysql
```

## Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/ar4199/NASA_NEO_MINI_PROJECT.git
   cd NASA_NEO_MINI_PROJECT
   ```

2. **Set up MySQL**
   - Ensure MySQL server is running locally.
   - Update MySQL credentials in the notebook as needed.

3. **Run the Notebook**
   - Open `nasa_neo_project.ipynb` in Jupyter.
   - Execute each cell sequentially.

## Outputs

- **Database Tables:**
  - `ASTEROID`: Contains asteroid ID, name, magnitude, diameter range, and hazardous status.
  - `CLOSE_APPROACH_DATA`: Contains NEO reference ID, close approach date, velocity, miss distance, and orbiting body.

- **Example SQL Query Results:**  
  The notebook demonstrates retrieving and displaying sample data from each table.

## Notes

- The NASA API key used in the notebook is for demonstration. You may request your own API key from [NASA's API portal](https://api.nasa.gov/).
- Data is fetched for the week starting `2024-01-01` (can be modified in the notebook).
- Ensure your MySQL user has privileges to create databases and tables.

## License

MIT License

## Acknowledgements

- [NASA NeoWs API](https://api.nasa.gov/)
