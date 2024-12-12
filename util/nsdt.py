import requests
from urllib3 import encode_multipart_formdata
import os.path
import time

BASE_URL = "https://tumo.nsdt.cloud"
STREAM_ID = "fbdb0ea035"


def upload_file_to_nsdt(file_path, file_type, api_key, comment):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Zjjs-Client": "9114a8df37f546f6b9de2180938c8800"
    }
    full_url = f"{BASE_URL}/api/file/{file_type}/{STREAM_ID}/main"

    filename = os.path.basename(file_path)
    try:
        with open(file_path, 'rb') as f:
            file = {'file': (filename, f.read()), 'comment': comment}
            encode_data = encode_multipart_formdata(file)
            filedata = encode_data[0]
            headers['Content-Type'] = encode_data[1]
            res = requests.post(full_url, headers=headers, data=filedata, stream=True)
            if res.status_code == 201:
                blob_id = res.json()['uploadResults'][0]['blobId']
                return {"done": 1, "blob_id": blob_id}
            else:
                return {"done": 0, "status": res.status_code }
    except Exception as e:
        return {"done": 0}


def download_file(api_key, file_type, ids, stream_id, out_path):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Zjjs-Client": "9114a8df37f546f6b9de2180938c8800"
    }
    full_url = f"{BASE_URL}/export?stream_id={stream_id}&ids={ids}&file_type={file_type}"
    try:
        response = requests.get(full_url, headers=headers, stream=True, timeout=3000)

        if response.status_code == 200:
            with open(out_path, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive new chunks
                        out_file.write(chunk)
            print(f"File downloaded successfully to {out_path}")
            return out_path
        else:
            print(f"Failed to download file. Status code: {response.status_code}, Response: {response.text}")
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def poll_file_upload_status(api_key, file_id):
    full_url = f"{BASE_URL}/graphql"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Zjjs-Client": "9114a8df37f546f6b9de2180938c8800"
    }
    query = """
    query File($fileId: String!, $streamId: String!) {
        stream(id: $streamId) {
            id
            fileUpload(id: $fileId) {
                id
                convertedCommitId
                userId
                convertedStatus
                convertedMessage
                fileName
                fileSize
                fileType
                uploadComplete
                uploadDate
                convertedLastUpdate
            }
        }
    }
    """

    variables = {
        "fileId": file_id,
        "streamId": STREAM_ID
    }

    while True:
        try:
            response = requests.post(full_url, json={"query": query, "variables": variables}, headers=headers)

            if response.status_code == 200:
                data = response.json()
                file_upload = data.get("data", {}).get("stream", {}).get("fileUpload", {})

                if file_upload.get("convertedStatus") == 2:
                    print("File processing completed.")
                    return {"done": 1, "commit_id": file_upload.get("convertedCommitId")}

                if file_upload.get("convert") == 3:
                    print("parse 3d file fail")
                    return {"done": 0}

                print("Processing not complete. Retrying in 3 seconds...")
                time.sleep(3)
            else:
                print(f"Failed to poll status. Status code: {response.status_code}, Response: {response.text}")
                return {"done": 0}
        except requests.exceptions.RequestException as e:
            print(f"A network error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def query_object(api_key, commit_id):
    full_url = f"{BASE_URL}/graphql"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Zjjs-Client": "9114a8df37f546f6b9de2180938c8800"
    }
    query = """
    query objectId($streamId: String!, $commitId: String!) {
        stream(id: $streamId) {
            commit(id: $commitId) {
                id
                referencedObject
                message
           }
        }
    }
    """

    variables = {
        "commitId": commit_id,
        "streamId": STREAM_ID
    }
    try:

        response = requests.post(full_url, json={"query": query, "variables": variables}, headers=headers)

        if response.status_code == 200:
            data = response.json()
            commit = data.get("data", {}).get("stream", {}).get("commit", {})
            return commit.get("referencedObject")
        else:
            return
    except Exception as e:
        print(str(e))
        return


def convert_to_target_file(api_key, target_type, blob_id, output_file_path):
    commit_res = poll_file_upload_status(api_key=api_key, file_id=blob_id)
    if commit_res['done'] == 0:
        return

    commit_id = commit_res['commit_id']

    object_id = query_object(api_key, commit_id)
    if object_id is None:
        return

    return download_file(api_key,target_type, object_id,STREAM_ID, output_file_path)



def test():
    file_path = 'tripo_pbr_model_b26fd51f-70d8-4ee9-9423-1ff1b34cb7cf.glb'
    target_type = "gltf"
    api_key = "put your api_key"

    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    extension = extension[1:] if extension else ""

    comment = f"""{{"convertType": "{target_type}", "from": "comfyUI-3D-Convert"}}"""
    directory = os.path.dirname(os.path.abspath(file_path))
    file_name = os.path.basename(file_path)
    new_file_path = os.path.join(directory, f'{file_name}.{target_type}')
    resp = upload_file_to_nsdt(file_path, extension, api_key, comment)

    if resp['done'] == 1:
        blob_id = resp['blob_id']
        print(f'file upload success: {blob_id}')
        target_path = convert_to_target_file(api_key, target_type, blob_id, new_file_path)
        if target_path is not None:
            return target_path

test()