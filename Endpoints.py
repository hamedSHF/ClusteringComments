from ClusteringModel import Cluster
from typing import Annotated
from fastapi import FastAPI,File, UploadFile,Response,Request,HTTPException,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,JSONResponse
import os


app = FastAPI()
templates = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})


@app.post("/uploadFile",response_class=JSONResponse)
async def uploadFile(file: Annotated[UploadFile,Form()],columnName : Annotated[str,Form()]):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400,detail="Uploaded file must be Excel file")
    if not columnName:
        raise HTTPException(status_code=400,detail="ColumnName must be provided for clustering")
    current_dir = os.path.dirname(__file__)
    file_path= os.path.join(current_dir,file.filename)
    with open(file_path,"wb") as f:
        f.write(file.file.read())
    clusterModel = Cluster()
    try:
        clusterModel.predict(pathOfExcelFile=file_path,columnName=columnName)
        content = clusterModel.extractClustersContent()
    except:
        raise HTTPException(status_code=400,detail="Error occured during clustering")
    return Response(content=content,media_type="application/json")
        