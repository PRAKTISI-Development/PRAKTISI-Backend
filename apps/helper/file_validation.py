from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

def validate_pdf(file: UploadFile):
    allowed_extensions = {'pdf'}
    max_file_size = 5 * 1024 * 1024 

    if file.content_type.lower() != 'application/pdf':
        raise HTTPException(
            status_code=400,
            detail='File tugas harus PDF.',
        )

    if file.filename.split('.')[-1].lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail='Ekstensi tidak sesuai. file harus berupa PDF.',
        )

    if len(file.file.read()) > max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f'Ukuran maksimal file adalah {max_file_size / (1024 * 1024)} MB.',
        )

    file.file.seek(0)

    return file

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    validated_file = validate_pdf(file)

    return JSONResponse(content={"message": "File berhasil diunggah!"}, status_code=200)
