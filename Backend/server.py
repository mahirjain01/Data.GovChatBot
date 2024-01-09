from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from data_downloader_module import DataDownloader
from chatbot import create_chatbot  
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize the DataDownloader with API key
database_url = os.getenv("DATAGOVINDIA_API_KEY")
data_downloader = DataDownloader(database_url)

class SearchRequest(BaseModel):
    query: str
    search_fields: list = None
    sort_by: str = None
    ascending: bool = True

@app.post("/search")
async def search_data(request: SearchRequest):
    try:
        search_results = data_downloader.search_data(
            request.query,
            search_fields=request.search_fields,
            sort_by=request.sort_by,
            ascending=request.ascending
        )
        return {"data": search_results.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

@app.get("/resource/{resource_id}")
async def get_resource_info(resource_id: str):
    try:
        resource_info = data_downloader.get_resource_info(resource_id)
        return {"data": resource_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting resource info: {str(e)}")

@app.get("/data/{resource_id}")
async def get_data(resource_id: str, limit: int = 10):
    try:
        resource_data = data_downloader.get_data(resource_id, limit=limit)
        return {"data": resource_data.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting data: {str(e)}")

@app.get("/download/{resource_id}")
async def download_data(resource_id: str, output_format: str = "csv"):
    try:
        output_filepath = f"{resource_id}_data.{output_format}"
        downloaded_data = data_downloader.download_data(resource_id, output_format=output_format, output_filepath=output_filepath)
        return {"message": f"Data downloaded successfully! Saved to {output_filepath}", "data": downloaded_data.to_dict(orient="records"), "output_filepath": output_filepath}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during download: {str(e)}")

@app.get("/chatbot/{resource_id}")
async def chatbot_endpoint(resource_id: str, user_question: str):
    try:
        # Await the asynchronous function download_data
        download_result = await download_data(resource_id)
        output_filepath = download_result["output_filepath"]

        # Use the output_filepath in the chatbot
        chatbot_response = create_chatbot(output_filepath, user_question)
        return {"chatbot_response": chatbot_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chatbot execution: {str(e)}")
