from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def file_validation(file: UploadFile):
    content_type = file.content_type.lower()
    file_extension = file.filename.split('.')[-1].lower()

    if content_type != 'application/pdf' or file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail='File tugas harus PDF dengan ekstensi yang sesuai.',
        )

    try:
        file_content = file.file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail='Gagal membaca file.',
        ) 

    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f'Ukuran maksimal file adalah {MAX_FILE_SIZE_MB} MB.',
        )

    file.file.seek(0) 

    return file
