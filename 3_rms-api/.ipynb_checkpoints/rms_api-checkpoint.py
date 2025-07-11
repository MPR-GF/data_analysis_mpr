import json
import time
import requests
from rms_models import Api_Config, Api_Response, Device_Registration_Root_Model, Device_Monitoring_Root_Model

class RmsApi:
    """
    Contains variables and provides functionality
    to interact with Teltonika RMS API.
    """

    def __init__(self, config: Api_Config) -> None:
        """
        Initializes a TeltonikaRmsApi object with required
        variables from a .env file.
        """
        self.personal_access_token : str = config.personal_access_token
        self.api_base_url : str = config.api_base_url
        self.green_fusion_company_id : str = config.green_fusion_company_id
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

    def get_companies(self)->None:
        """

        """
        print("Fetching all companies info...")
        url = f"{self.api_base_url}/companies"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.personal_access_token}"
            }
        response = self.api_call(url, headers, method="GET")
        if response:
            print(response.status_code)
            print(json.dumps(response.response_body, indent=2))
            print(("Fetched all companies info successfully!"))
        else:
            raise ValueError("Fetching all companies info failed.")

    def get_device_id_by_name(self, name)->Api_Response:
        """

        """
        print(f"Fetching {name}'s device_id...")
        url = f"{self.api_base_url}/devices?q={name}&fields=id"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.personal_access_token}"
            }
        response = self.api_call(url, headers, method="GET")
        if response:
            print(response.status_code)
            print(json.dumps(response.response_body, indent=2))
            print((f"Fetched {name}'s device_id successfully!"))
            return response.response_body["data"][0]["id"]
        else:
            raise ValueError(f"Fetching {name}'s device_id failed.")


    def add_new_device(self, config: Device_Registration_Root_Model)->Api_Response:
        """

        """
        print(f"Registering device: {config.data[0].name} ...")
        url = f"{self.api_base_url}/devices"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.personal_access_token}"
            }
        payload = config.model_dump()
        response = self.api_call(url, headers, method="POST", payload=payload)
        if response:
            print(response.status_code)
            print(json.dumps(response.response_body, indent=2))
            print((f"Registered device {config.data[0].name} successfully!"))
            return response
        else:
            raise ValueError(f"Registering device {config.data[0].name} failed.")

    def enable_device_monitoring(self, config: Device_Monitoring_Root_Model)->Api_Response:
        """

        """
        print(f"Enabling monitoring for: {config.data[0].device_id} ...")
        url = f"{self.api_base_url}/devices/monitoring"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.personal_access_token}"
            }
        payload = config.model_dump()
        response = self.api_call(url, headers, method="PUT", payload=payload)
        if response:
            print(response.status_code)
            print(json.dumps(response.response_body, indent=2))
            print((f"Enabled monitoring for: {config.data[0].device_id} successfully!"))
            return response
        else:
            raise ValueError(f"Enabling monitoring for: {config.data[0].device_id} failed.")

    def get_offline_devices(self)->Api_Response:
        """

        """
        print(f"Fetching offline devices...")
        url = f"{self.api_base_url}/devices?status=offline"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.personal_access_token}"
            }
        response = self.api_call(url, headers, method="GET")
        if response:
            print(response.status_code)
            # print(json.dumps(response.response_body, indent=2))
            print((f"Fetched offline devices successfully!"))
            return Api_Response(
                status_code=response.status_code,
                response_body=response.response_body
            )
        else:
            raise ValueError(f"Fetching offline devices failed.")