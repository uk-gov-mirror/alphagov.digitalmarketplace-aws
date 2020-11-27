#!/usr/bin/env python

import os
import sys
import json
import requests
from requests.exceptions import HTTPError

def _read_in_chunks(file_path):
    chunk_size = 30720 * 30720
    with open(file_path, 'rb') as file_object:
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data


def upload_dump_to_s3():
    s3_post_url_data = json.loads(os.environ['S3_POST_URL_DATA'])
    dump_file = "/app/{}".format(os.environ['DUMP_FILE_NAME'])

    url = s3_post_url_data['url']
    fields = s3_post_url_data['fields']
    files = {"file": _read_in_chunks(dump_file)}

    response = requests.post(url, data=fields, files=files)

    try:
        response.raise_for_status()
    except HTTPError as e:
        print("Error uploading {} to {}: {}".format(dump_file, url, e.args[0]))
        sys.exit(1)
    except Exception as e:
        print("Error uploading: {}".format(e))
        sys.exit(2)
    else:
        print('Successfully uploaded {} to {}'.format(dump_file, url))


if __name__ == "__main__":
    upload_dump_to_s3()
