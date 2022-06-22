# snu-web-final-project-backend

- 웹프로그래밍 수업 기말 팀 프로젝트를 위한 백엔드 서버입니다.
- OpenAPI 만을 이용하면 실제 업로드가 불가능하기 때문에 백엔드를 추가적으로 구현하였습니다
- Fastapi 와 MySQL 을 이용하여 간단하게 구현하였습니다.
- Fastapi Server, MySQL 은 Docker 를 이용하여 EC2 위에 배포하였습니다.


## Api Documentation
- 기본적으로 http://3.34.253.236:8080/docs 에서 Swagger 문서를 볼 수 있습니다.
- 따라서 각 Input, Output 설명은 생략하고, 주의해야할 부분이나 모호한 부분을 README 에서 보강합니다.

### Get
- 직접 업로드한 동물들의 정보를 얻어올 수 있는 Api 입니다.
- Client 에서 num 을 input 으로 주어 한 번에 Fetch 해올 데이터 수를 결정합니다. (Client 자유도 부여)
- `created_at` 는 분실신고 시점을 보여주는 데에 사용됩니다.
- `image_url` 을 통해 이미지를 직접 받아올 수 있습니다.

### Upload
- Client 에서 서버에 동물 정보를 업로드하기 위한 Api 입니다. 이미지와 몇몇 정보들을 서버에 업로드하면, 서버는 해당 이미지를 S3 에 업로드하고, S3 에 저장된 Path 와 다른 정보들을 DB 에 저장하게 됩니다.

---
## 기타 (DB)
- DB 로는 MySQL 8.0 을 사용하며, 가볍게 Docker 를 이용해서 띄웁니다.
- 한글을 사용하기 때문에 추가적인 옵션을 추가해서 띄웁니다.
```
$ docker run --name mysql -e MYSQL_ROOT_PASSWORD=mysql -d -p 3306:3306 mysql:8.0 \
	--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```
- `snu` 라는 Database 명, `animals` 라는 Table 명을 각각 사용합니다.
