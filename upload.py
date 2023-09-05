import requests

def upload_file(room):
    # Replace these values with your server's details
    server_url = 'http://127.0.0.1:5000/upload'  # URL where you want to upload the file
    file_path = 'TEST.txt'         # Path to the file you want to upload

    try:
        # Open the file for reading
        with open(file_path, 'rb') as file:
            # Prepare the file to be uploaded
            files = {'file': (file_path, file)}
            headers = {'auth': "12345", 'room': room}
            # Make the POST request to the server
            response = requests.post(server_url, files=files, headers=headers)

            # Check the response from the server
            if response.status_code == 200:
                print("File uploaded successfully!")
            else:
                print("Upload failed with status code:", response.status_code)
                print(response.text)  # Print the response content for more details

    except FileNotFoundError:
        print("File not found:", file_path)

    except Exception as e:
        print("An error occurred:", str(e))

# This code will only run when the script is executed directly
if __name__ == "__main__":
    upload_file()
