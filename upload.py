import os
import requests


def upload_file(room, path):
    # Replace these values with your server's details
    server_url = 'http://127.0.0.1:5000/upload'  # URL where you want to upload the files

    try:
        # List all files in the specified folder
        files = os.listdir(path)

        for file_name in files:
            file_path = os.path.join(path, file_name)

            # Check if the item in the folder is a file (not a directory)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    # Prepare the file to be uploaded
                    files = {'file': (file_name, file)}
                    headers = {'auth': "12345", 'room': room}
                    # Make the POST request to the server
                    response = requests.post(server_url, files=files, headers=headers)

                    # Check the response from the server
                    if response.status_code == 200:
                        print(f"File '{file_name}' uploaded successfully!")
                    else:
                        print(f"Upload of '{file_name}' failed with status code:", response.status_code)
                        print(response.text)  # Print the response content for more details

    except FileNotFoundError:
        print("Folder not found:", path)

    except Exception as e:
        print("An error occurred:", str(e))

# This code will only run when the script is executed directly
if __name__ == "__main__":
    upload_file()
