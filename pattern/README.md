# Tokyo Weather Forecast Cloud Function

This directory contains a Google Cloud Function that fetches a 7-day weather forecast for Tokyo from the Open-Meteo API and uploads it as a CSV file to a specified Google Cloud Storage bucket.

## Files

- `tokyo_weather_forecast.py`: The Python script containing the Cloud Function logic.
- `requirements.txt`: Lists the Python dependencies required for the function.

## Deployment

Follow these steps to deploy the Cloud Function:

1.  **Ensure Google Cloud SDK is installed and configured.**
    If not, follow the instructions [here](https://cloud.google.com/sdk/docs/install).

2.  **Set up your Google Cloud project.**
    Make sure you have a project created and billing enabled. Note your `PROJECT_ID`.

3.  **Enable necessary APIs.**
    You'll need to enable the Cloud Functions API and Cloud Storage API for your project.
    ```bash
    gcloud services enable cloudfunctions.googleapis.com storage-component.googleapis.com --project YOUR_PROJECT_ID
    ```

4.  **Create a Google Cloud Storage bucket.**
    This bucket will store the output CSV file. Note your `BUCKET_NAME`.
    ```bash
    gsutil mb gs://YOUR_BUCKET_NAME
    ```

5.  **Deploy the Cloud Function.**
    Navigate to the `pattern` directory in your terminal. Then run the following `gcloud` command:

    ```bash
    gcloud functions deploy get_tokyo_weather_forecast \
        --project YOUR_PROJECT_ID \
        --region YOUR_PREFERRED_REGION # e.g., us-central1, asia-northeast1
        --runtime python39 # Or python38, python310, python311, python312 as per your preference
        --trigger-http # Or use --trigger-topic YOUR_PUBSUB_TOPIC for Pub/Sub trigger, or --trigger-bucket YOUR_TRIGGER_BUCKET for GCS trigger
        --entry-point get_tokyo_weather_forecast \
        --source . \
        --set-env-vars GCS_BUCKET_NAME="YOUR_BUCKET_NAME",OUTPUT_FILE_NAME="tokyo_forecast.csv" \
        --allow-unauthenticated # If you want to invoke it via HTTP without authentication
    ```
    Replace `YOUR_PROJECT_ID`, `YOUR_PREFERRED_REGION`, and `YOUR_BUCKET_NAME` with your actual values. You can also customize `OUTPUT_FILE_NAME`.

    *   `--runtime`: Choose a supported Python runtime.
    *   `--trigger-http`: This example uses an HTTP trigger. You can change this to a Pub/Sub trigger (`--trigger-topic YOUR_TOPIC`) or a Cloud Scheduler job for periodic execution.
    *   `--entry-point`: The name of the function in your Python script.
    *   `--source .`: Specifies that the source code is in the current directory.
    *   `--set-env-vars`: Sets environment variables required by the function.
    *   `--allow-unauthenticated`: Remove this if you want to secure your HTTP-triggered function with IAM.

6.  **Set IAM Permissions (if not already covered by default service account permissions).**
    The Cloud Function will execute using a service account. By default, this service account is `YOUR_PROJECT_ID@appspot.gserviceaccount.com`.
    This service account needs permission to write to the GCS bucket you created. Grant the "Storage Object Creator" or "Storage Object Admin" role to this service account on the specific bucket.

    You can do this via the Google Cloud Console (IAM & Admin > IAM, or Storage > Browser > Your Bucket > Permissions) or using `gsutil`:
    ```bash
    gsutil iam ch serviceAccount:YOUR_PROJECT_ID@appspot.gserviceaccount.com:objectCreator gs://YOUR_BUCKET_NAME
    # Or for finer-grained control on the default compute service account:
    # gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    #   --member="serviceAccount:YOUR_PROJECT_ID@appspot.gserviceaccount.com" \
    #   --role="roles/storage.objectCreator"
    # If you are using a dedicated service account for your function, replace the service account email accordingly.
    ```

## Environment Variables

The Cloud Function uses the following environment variables:

-   `GCS_BUCKET_NAME`: (Required) The name of the Google Cloud Storage bucket where the CSV file will be uploaded.
-   `OUTPUT_FILE_NAME`: (Optional) The name of the output CSV file. Defaults to `tokyo_weather_forecast.csv`.

## Local Testing

The `tokyo_weather_forecast.py` script includes a `if __name__ == "__main__":` block for basic local testing.
To use it:
1.  Install dependencies: `pip install -r requirements.txt`
2.  Set environment variables locally:
    ```bash
    export GCS_BUCKET_NAME="your-actual-gcs-bucket-name"
    export OUTPUT_FILE_NAME="tokyo_weather_local_test.csv"
    ```
3.  Ensure you are authenticated with Google Cloud for application-default credentials:
    ```bash
    gcloud auth application-default login
    ```
4.  Run the script:
    ```bash
    python tokyo_weather_forecast.py
    ```
This will attempt to fetch the weather data and upload it to your specified GCS bucket.

## Invocation

-   **HTTP Trigger:** If deployed with an HTTP trigger, you can find the URL in the output of the `gcloud functions deploy` command or in the Cloud Console. You can invoke it using `curl` or any HTTP client.
-   **Pub/Sub or Scheduler:** If configured with a different trigger, it will run based on that trigger's events (e.g., a message to a Pub/Sub topic, or a schedule defined in Cloud Scheduler). For scheduled execution, create a Cloud Scheduler job that targets your HTTP-triggered function or publishes a message to its Pub/Sub topic.
```
