import os
import json
from rms_api import RmsApi
from rms_status_api import RmsStatusApi
from rms_models import Api_Config, Status_Api_Config, Device_Registration_Info, Device_Registration_Root_Model, Device_Monitoring_Info, Device_Monitoring_Root_Model

rms_api_personal_access_token = os.getenv("RMS_API_PERSONAL_ACCESS_TOKEN")

## RMS api
rms_api = RmsApi(Api_Config(
    personal_access_token=rms_api_personal_access_token,
    verbose=False
    ))


## Get offline devices
offline_device = rms_api.get_offline_devices()
print(json.dumps(offline_device.response_body["data"], indent=2))


## RMS status api
# rms_status_api = RmsStatusApi(Status_Api_Config(
#     personal_access_token=rms_api_personal_access_token,
#     verbose=True
#     ))


## Function tests
#rms_api.get_companies()
#rms_api.get_devices(name="rut-testdev2")


## Device registration test
# device_registration_info = Device_Registration_Info(
#     serial="6000373275", # ubus call mnfinfo get -> mnfinfo.serial
#     mac="20:97:27:05:9C:03", # ubus call mnfinfo get -> mnfinfo.mac
#     imei="864086067797047", # ubus call gms.modem0 get_id_info -> imei
#     name="rut-testdev2",
#     password_confirmation="t8RPe2z0"
# )

# rms_api.add_new_device(Device_Registration_Root_Model(data=[new_device_info]))

# device_id = rms_api.get_device_id_by_name(name=device_registration_info.name)

# device_monitoring_info = Device_Monitoring_Info(
#     device_id=device_id
# )
# rms_api.enable_device_monitoring(Device_Monitoring_Root_Model(data=[device_monitoring_info]))


## RMS status api test
#print(response.response_body["meta"]["channel"])
#rms_status_api.get_channel_status(channel=response.response_body["meta"]["channel"])
#rms_status_api.get_channel_status(channel="private-status.154819.L4CXRUAXGL0vWAj6VzNlzRZlDeuuQ8UfWoD36xVunCVsWd4zwrirBKzLy57fUh6g")
