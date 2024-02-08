import pandas as pd
from io import BytesIO
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from fastapi.responses import StreamingResponse

from apps.database import get_db
from apps.helpers.response import response
from apps.schemas.akumulasi_schema import *
from apps.models.nilai_akhir import NilaiAkhir as NilaiAkhirModel

def execute_query(db, kd_matkul):
    query = text(f"call akumulasi_nilai_dan_kehadiran('{kd_matkul}')")
    result = db.execute(query)
    data = result.fetchall()
    column_names = result.keys()
    return data, column_names

def create_nilai_akhir(request, nilai_akhir_data, db):
    try:
        db_nilai_akhir = NilaiAkhirModel(**nilai_akhir_data.model_dump())
        db.add(db_nilai_akhir)
        db.commit()
        db.refresh(db_nilai_akhir)
        return response(request, status_code=200, success=True, msg="success create data", data=db_nilai_akhir)
    except Exception as e:
        return response(request, status_code=500, success=False, msg=str(e), data=None)

def get_akumulasi(request, kd_matkul: str, db: Session = Depends(get_db)):
    try:
        data, column_names = execute_query(db, kd_matkul)
        list_of_dicts = [dict(zip(column_names, row)) for row in data]
        return response(request, status_code=200, success=True, msg="success get data", data=list_of_dicts)
    except Exception as e:
        return response(request, status_code=500, success=False, msg=str(e), data=None)

def get_download(request, kd_matkul: str, db: Session = Depends(get_db)):
    try:
        data, column_names = execute_query(db, kd_matkul)
        df = pd.DataFrame(data, columns=column_names)
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)

        response = StreamingResponse(iter([excel_buffer.getvalue()]), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
        praktikum_value = data[0][list(column_names).index('praktikum')]
        filename = f"Akumulasi {praktikum_value}.xlsx"
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"

        redirect_url = f"/v1/nilai_akhir/akumulasi/{kd_matkul}"
        response.headers["Refresh"] = f"1; url={redirect_url}"

        return response
    except Exception as e:
        return response(request, status_code=500, success=False, msg=str(e), data=None)

def get_nilai_akhir(request, usersid, kd_matkul, db):
    try:
        nilai_akhir = db.query(NilaiAkhirModel).filter(
            NilaiAkhirModel.usersid == usersid,
            NilaiAkhirModel.kd_matkul == kd_matkul
        ).first()
        if nilai_akhir is None:
            raise HTTPException(status_code=404, detail="Nilai Akhir not found")
        return response(request,status_code=200, success=True, msg="Data ditemukan", data=nilai_akhir)
    except Exception as e:
        return response(request, status_code=500, success=False, msg=str(e), data=None)

def get_all_nilai_akhir(request, db):
    try:
        nilai_akhir_list = db.query(NilaiAkhirModel).all()
        return response(request, status_code=200, success=True, msg="success get data", data=nilai_akhir_list)
    except Exception as e:
        return response(request, status_code=500, success=False, msg=str(e), data=None)

def update_nilai_akhir(request, nilai_akhir_data, usersid, kd_matkul, db):
    try:
        data = nilai_akhir_data.dict()
        data["usersid"] = usersid
        data["kd_matkul"] = kd_matkul
        db_nilai_akhir = db.query(NilaiAkhirModel).filter(
            NilaiAkhirModel.usersid == usersid,
            NilaiAkhirModel.kd_matkul == kd_matkul
        ).first()
        if db_nilai_akhir is None:
            raise HTTPException(status_code=404, detail="Nilai Akhir not found")
        for key, value in data.items():
            setattr(db_nilai_akhir, key, value)
        db.commit()
        db.refresh(db_nilai_akhir)
        return response(request,status_code=200, success=True, msg="Berhasil memperbarui data", data=db_nilai_akhir)
    except Exception as e:
        return response(request, status_code=500, success=False, msg=str(e), data=None)

def delete_nilai_akhir(request, usersid, kd_matkul, db):
    try:
        db_nilai_akhir = db.query(NilaiAkhirModel).filter(
            NilaiAkhirModel.usersid == usersid,
            NilaiAkhirModel.kd_matkul == kd_matkul
        ).first()
        if db_nilai_akhir is None:
            raise HTTPException(status_code=404, detail="Nilai Akhir not found")
        db.delete(db_nilai_akhir)
        db.commit()
        return response(request,status_code=200, success=True, msg="Informasi berhasil dihapus", data=None)
    except Exception as e:
        return response(request, status_code=500, success=False, msg=str(e), data=None)