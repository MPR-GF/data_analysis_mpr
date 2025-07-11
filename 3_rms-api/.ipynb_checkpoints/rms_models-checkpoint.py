from pydantic import BaseModel
from typing import List

class Api_Config(BaseModel):
    personal_access_token: str
    api_base_url : str = "https://api.rms.teltonika-networks.com"
    green_fusion_company_id : int = 134619
    verbose: bool = False

class Status_Api_Config(BaseModel):
    personal_access_token: str
    api_base_url : str = "https://api.rms.teltonika-networks.com/status/channel"
    verbose: bool = False

class Api_Response(BaseModel):
    status_code : int
    response_body : dict

class Device_Registration_Info(BaseModel):
    company_id : int = 134619
    device_series : str = "rut"
    serial : str
    mac : str
    imei : str
    name : str
    # firmware_file_id : int = None
    # config_file_id : int = None
    auto_credit_enable : bool = False
    password_confirmation : str
    tag_id : List[int] = []

class Device_Registration_Root_Model(BaseModel):
    data : List[Device_Registration_Info]

class Device_Monitoring_Info(BaseModel):
    device_id : int
    monitoring_enabled : int = 1

class Device_Monitoring_Root_Model(BaseModel):
    data : List[Device_Monitoring_Info]
