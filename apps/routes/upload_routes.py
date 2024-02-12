from fastapi import APIRouter, File, HTTPException, UploadFile
from apps.middleware.validation import file_validation

router = APIRouter()

@router.post("/upload", response_model=dict)
async def upload_tugas(file: UploadFile = File(..., description="File tugas PDF")):
    try:
        file_validation(file)
        return {"message": "File uploaded successfully"}
    except HTTPException as e:
        raise e
