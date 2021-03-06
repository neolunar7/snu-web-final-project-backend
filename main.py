from fastapi import FastAPI, UploadFile, HTTPException
import uvicorn
from schema import AnimalInfos, UploadResult
import pymysql
import os, uuid
from utils.db import get_conn
import boto3

app = FastAPI()

# ENVS
LOCAL_IMAGE_DIR = "/home/ubuntu/lost-animal-images"
BUCKET_NAME = 'infra-test-831uq8dafq'


@app.get("/api/animals/v2", status_code=200)
async def get_animals(num: int):
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                sql = 'SELECT * FROM `animals` ORDER BY id DESC LIMIT {}'.format(num)
                cursor.execute(sql)
                animals = cursor.fetchall()

                # If no data, return empty list
                if not animals:
                    return {
                            "animals": animals
                    }
                
                # If data
                result = []
                for animal in animals:
                    result.append(
                        {
                            "image_url": "{}".format(animal['image_url']),
                            "notice_number": "{}-{}-{}".format(animal['major_province'], animal['major_province'], str(animal['id']).zfill(5)),
                            "kind": "{}".format(animal['kind']),
                            "feature": "{}".format(animal['feature']),
                            "sex": "{}".format(animal['sex']),
                            "created_at": "{}".format(animal['created_at']),
                            "province": "{}".format(animal['major_province'])
                        }
                    )                
                return {
                    "animals": result
                }
    except Exception as e:
        print(e)


@app.post("/api/animals/v2", status_code=201)
async def upload_animal(file: UploadFile, kind: str, feature: str,
                        sex : str, major_province: str) -> None:
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Format should be jpeg")

    img = await file.read()
    hashed_filename = uuid.uuid4().hex
    hashed_filename_with_ext = "{}.jpeg".format(hashed_filename)
    local_image_path = os.path.join(LOCAL_IMAGE_DIR, hashed_filename_with_ext)

    with open(local_image_path, "wb") as f:
        f.write(img)

    client = boto3.client('s3',
                          region_name='ap-northeast-2')
    try:
        client.upload_file(
            local_image_path,
            BUCKET_NAME,
            hashed_filename_with_ext,
            ExtraArgs={'ContentType': 'image/jpeg'}
        )
    except Exception as e:
        print(e)

    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                insert_sql = '''
                INSERT INTO `animals` (
                    `major_province`,
                    `image_url`,
                    `kind`,
                    `feature`,
                    `sex`
                )
                VALUES (
                    %s, -- major_province
                    %s, -- image_url
                    %s, -- kind
                    %s, -- feature
                    %s -- sex
                )
                '''
                cursor.execute(insert_sql, (
                    major_province,
                    "https://{}.s3.ap-northeast-2.amazonaws.com/{}".format(BUCKET_NAME, hashed_filename_with_ext),
                    kind,
                    feature,
                    sex
                ))
            conn.commit()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
