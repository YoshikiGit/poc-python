import os
import csv
import json
from io import StringIO
import requests
from google.cloud import storage

# Configuration from environment variables
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
OUTPUT_FILE_NAME = os.environ.get("OUTPUT_FILE_NAME", "tokyo_weather_forecast.csv")
TOKYO_LATITUDE = 35.6895
TOKYO_LONGITUDE = 139.6917

def get_tokyo_weather_forecast(event, context):
    """
    Cloud Function to retrieve the weather forecast for Tokyo for the next 7 days
    and upload it as a CSV file to Google Cloud Storage.
    """
    if not GCS_BUCKET_NAME:
        print("Error: GCS_BUCKET_NAME environment variable is not set.")
        return "Error: GCS_BUCKET_NAME not set.", 500

    print(f"Fetching weather forecast for Tokyo ({TOKYO_LATITUDE}, {TOKYO_LONGITUDE})")

    # Open-Meteo API URL
    # We request daily data for temperature_2m_max, temperature_2m_min, precipitation_sum, windspeed_10m_max
    api_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={TOKYO_LATITUDE}&longitude={TOKYO_LONGITUDE}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max"
        f"&timezone=Asia/Tokyo"
    )

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        weather_data = response.json()
        print("Successfully fetched weather data.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return f"Error fetching weather data: {e}", 500

    if "daily" not in weather_data or not all(
        k in weather_data["daily"]
        for k in ["time", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "windspeed_10m_max"]
    ):
        print(f"Unexpected API response format: {weather_data}")
        return "Error: Unexpected API response format.", 500

    # Prepare CSV data
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    header = [
        "date",
        "temperature_max_celsius",
        "temperature_min_celsius",
        "precipitation_sum_mm",
        "windspeed_max_kmh",
    ]
    writer.writerow(header)

    # Write data rows
    daily_data = weather_data["daily"]
    for i in range(len(daily_data["time"])):
        row = [
            daily_data["time"][i],
            daily_data["temperature_2m_max"][i],
            daily_data["temperature_2m_min"][i],
            daily_data["precipitation_sum"][i],
            daily_data["windspeed_10m_max"][i],
        ]
        writer.writerow(row)

    csv_data = output.getvalue()
    output.close()
    print(f"CSV data prepared:\n{csv_data[:200]}...") # Log first 200 chars of CSV

    # Upload to Google Cloud Storage
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(OUTPUT_FILE_NAME)

        blob.upload_from_string(csv_data, content_type="text/csv")
        print(f"Successfully uploaded '{OUTPUT_FILE_NAME}' to bucket '{GCS_BUCKET_NAME}'.")
    except Exception as e:
        print(f"Error uploading to GCS: {e}")
        return f"Error uploading to GCS: {e}", 500

    return f"Successfully processed weather data and uploaded to GCS bucket '{GCS_BUCKET_NAME}' as '{OUTPUT_FILE_NAME}'.", 200

if __name__ == "__main__":
    # This section is for local testing and won't run in Cloud Functions
    # Set environment variables for local testing:
    os.environ["GCS_BUCKET_NAME"] = "your-gcs-bucket-name" # Replace with your bucket name
    os.environ["OUTPUT_FILE_NAME"] = "tokyo_weather_local_test.csv"

    print("Running local test...")
    message, status_code = get_tokyo_weather_forecast(None, None)
    print(f"Local test finished with status {status_code}: {message}")
    if status_code == 200:
        print(f"\nCheck your GCS bucket '{os.environ['GCS_BUCKET_NAME']}' for the file '{os.environ['OUTPUT_FILE_NAME']}'.")
        print("Ensure you have authenticated gcloud locally (e.g., `gcloud auth application-default login`).")

    # To test, you might need to install libraries:
    # pip install requests google-cloud-storage
    # And set up authentication for GCS.
    # Example: gcloud auth application-default login
    # Then run: python pattern/tokyo_weather_forecast.py
