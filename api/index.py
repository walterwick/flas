import time
import requests

def run_cron_job():
    url = "https://walterwick.de/api/cron"
    
    while True:
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            
            # Print the status code to check if the request was successful
            print(f"Request sent. Status Code: {response.status_code}")
        
        except Exception as e:
            # Print any error if the request fails
            print(f"Error occurred: {e}")
        
        # Wait for 60 minutes (3600 seconds) before running the job again
        time.sleep(3600)

if __name__ == "__main__":
    run_cron_job()
