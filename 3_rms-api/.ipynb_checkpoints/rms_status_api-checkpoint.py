import json
import time
import requests
from rms_models import Status_Api_Config, Api_Response

class RmsStatusApi:
    """
    Contains variables and provides functionality
    to interact with Teltonika RMS API.
    """

    def __init__(self, config: Status_Api_Config) -> None:
        """
        Initializes a TeltonikaRmsApi object with required
        variables from a .env file.
        """
        self.personal_access_token : str = config.personal_access_token
        self.api_base_url : str = config.api_base_url
        self.verbose : bool = config.verbose


    def api_call(
            self,
            url : str,
            headers : dict[str, str] | None = None,
            method : str ="GET",
            payload : dict[str, str] | None = None,
            max_retries : int = 3,
            backoff_factor : int = 2,
            timeout : int = 5
            )->Api_Response:
        """
        Implements actual API calls using request package including timeout and retries.
        Allowed methods are GET, POST, PUT and DELETE.
        """

        for attempt in range(max_retries):
            try:
                if method.upper() == "GET":
                    response = requests.get(
                        url,
                        headers=headers,
                        params=payload,
                        timeout=timeout,
                        verify=True
                        )
                elif method.upper() == "POST":
                    response = requests.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=timeout,
                        verify=True
                        )
                elif method.upper() == "PUT":
                    response = requests.put(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=timeout,
                        verify=True
                        )
                elif method.upper() == "DELETE":
                    response = requests.delete(
                        url,
                        headers=headers,
                        timeout=timeout,
                        verify=True
                        )
                else:
                    raise ValueError("Unsupported HTTP method. Use 'GET', 'POST', 'PUT' or 'DELETE'.")

                if response.status_code == 200 or response.status_code == 201 or response.status_code == 202 or response.status_code == 204:
                    response_body = response.json()
                    #print(response.status_code)
                    #print(json.dumps(response_body, indent=2))
                    return Api_Response(
                        status_code=response.status_code,
                        response_body=response_body
                    )
                else:
                    response_body = response.json()
                    print(
f"""Attempt {attempt + 1} - API call failed with:
status code: {response.status_code}
response: {json.dumps(response_body, indent=2)}
"""
                    )

            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1}: Request error: {str(e)}")

            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        raise Exception("All retry attempts failed.")

    def get_channel_status(self, channel)->None:
        """

        """
        print(f"Fetching events log for channel: {channel}...")
        url = f"{self.api_base_url}/{channel}"
        print(url)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.personal_access_token}"
            }
        response = self.api_call(url, headers, method="GET", max_retries=1)
        if response:
            print(response.status_code)
            print(json.dumps(response.response_body, indent=2))
            print((f"Fetched events log for channel: {channel} successfully!"))
        else:
            raise ValueError(f"Fetching events log for channel: {channel} failed.")
