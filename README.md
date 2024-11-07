# DocRetriever: A FastAPI-Based Document Ingestion and Querying System with RAG

This is a simple FastAPI application designed to receive and process text files uploaded by users. The API exposes an endpoint where users can upload .txt files and get the content returned as JSON.

## Features
-Upload text files (.txt) via a POST request

-Process and return the file content as a JSON response

-Basic error handling and logging for troubleshooting

## Prerequisites
-Python 3.8+: Ensure Python is installed on your system.
-FastAPI: This is the main web framework for the application.
-Uvicorn: An ASGI server that runs the FastAPI app.

![Screenshot 2024-11-07 at 10 44 54](https://github.com/user-attachments/assets/9978a210-ee2f-41dd-a47a-2b9e32cccc94)
![Screenshot 2024-11-07 at 10 54 40](https://github.com/user-attachments/assets/2cf877a4-04b0-4250-aa81-b2b5268e9b46)

## Installation
1. Clone the Repository:
```shell
git clone <repository-url>
cd <repository-directory>
```

2. Install Dependencies:
```shell
pip install fastapi uvicorn
```

3. Add Your Text File (for testing purposes): Place a .txt file in the project directory, or use the provided sample sample.txt file.

## Running the Application
Run the server with Uvicorn:
```shell
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```
The application should now be running at http://127.0.0.1:8080.

## Usage
### Uploading a File via cURL
To upload a file, you can use the following curl command:
```shell
curl -X POST "http://127.0.0.1:8080/upload/" -F "file=@/path/to/sample.txt"
```

### Swagger UI
You can also test the endpoint using the Swagger UI by going to http://127.0.0.1:8080/docs. This interface provides a web form to upload a file directly.

### Example Response
If the upload is successful, the API will return a JSON response with the file’s name and content:
```shell
{
    "filename": "sample.txt",
    "content": "Sample text content for testing the upload."
}

```

## License
This project is licensed under the MIT License.
