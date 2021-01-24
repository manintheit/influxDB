import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.sessions import session
import logging
logging.basicConfig(level=logging.DEBUG)

# InfluxDB Default output is json. If you want to change to output to csv, you need to add header.
# Note: On csv format, it is not possible show time format rfc3339
# https://stackoverflow.com/questions/43516396/how-can-you-get-csv-instead-of-json-from-the-http-api-of-influxdb
# jq -r "(.results[0].series[0].columns), (.results[0].series[0].values[]) | @csv"
headers = {'Accept': 'application/csv'}


def make_get_request(url, **kwargs):
    retry_strategy = Retry(
        total=5,
        status_forcelist=[429, 500, 502, 503, 504, 404],
        method_whitelist=["HEAD", "GET"],
        backoff_factor=0.8,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    if 'username' and 'password' in kwargs:
        session.auth = (kwargs.get('username'), kwargs.get('password'))
    data = kwargs.get('query')
    headers = kwargs.get('headers')
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    # for key, value in kwargs.items():
    #print("{0} = {1}".format(key, value))
    response = session.get(url, params=data, headers=headers)
    print(response.text)


if __name__ == '__main__':
    make_get_request("http://10.213.160.187:8086/query",
                     username="user", password="pass", query="q=show databases", headers=headers)
