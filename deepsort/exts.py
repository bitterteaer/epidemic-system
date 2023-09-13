import requests

base_url = "http://121.40.62.192:5503/api"
# base_url = "http://127.0.0.1:5000/api"


def group_requests_post(data):
    response = requests.post(base_url + "/capture/group_set_data",
                             data=data,
                             files=None,
                             verify=False,
                             stream=True)

    return response.status_code


def capture_requests_post(data):
    response = requests.post(base_url + "/capture/set_data",
                             data=data,
                             files=None,
                             verify=False,
                             stream=True)

    return response.status_code


def passers_by_requests_post(data):
    response = requests.post(base_url + "/passers_by/set_data",
                             data=data,
                             files=None,
                             verify=False,
                             stream=True)

    return response.status_code


def video_post(files):
    response = requests.post(base_url + "/capture/save_picture_cut",
                             # data={"ip": res, "type_": "video_upload"},
                             files=files,
                             verify=False,
                             stream=True)
    return response.status_code
