# snu-web-final-project-backend

- 웹프로그래밍 수업 기말 팀 프로젝트를 위한 백엔드 서버입니다.
- OpenAPI 만을 이용하면 실제 업로드가 불가능하기 때문에 백엔드를 추가적으로 구현하였습니다
- Fastapi 와 MySQL 을 이용하여 간단하게 구현하였습니다.
- Fastapi Server, MySQL 은 Docker 를 이용하여 EC2 위에 배포하였습니다.


## Api Documentation
- 기본적으로 http://52.78.82.160:8080/docs 에서 Swagger 문서를 볼 수 있습니다

### Get
- 직접 업로드한 동물들의 정보를 얻어올 수 있는 Api 입니다.
- Client 에서 num 을 input 으로 주어 한 번에 Fetch 해올 데이터 수를 결정합니다. (Client 자유도 부여)
- `created_at` 는 분실신고 시점을 보여주는 데에 사용됩니다.
- `image_url` 을 통해 이미지를 직접 받아올 수 있습니다.
- `notice_number` 는 auto incrementing `id` 와 `major_province`, `minor_province` 를 조합하여 서버에서 내려줍니다.

### Upload
- Client 에서 서버에 동물 정보를 업로드하기 위한 Api 입니다.
- `last_datetime_of_notice` 는 Date 형식으로 넣어주면 됩니다. e.g. 2022-07-30
- `major_province` 와 `minor_province` 의 경우, 서울과 같은 시인 경우 모두 시를 넣어주면 됩니다. e.g. 서울인 경우, 양쪽 모두 서울 명시.
- 이외의 경우에는 도, 군이 각각 들어갑니다. e.g. `major_province: 경남`, `minor_province: 합천`
- 해당 정보들로 `notice_number` 가 결정되기 때문에 반드시 필요합니다. 

---
## 기타 (DB)
- DB 로는 MySQL 8.0 을 사용하며, 가볍게 Docker 를 이용해서 띄웁니다.
- 한글을 사용하기 때문에 추가적인 옵션을 추가해서 띄웁니다.
```
docker run --name mysql -e MYSQL_ROOT_PASSWORD=mysql -d -p 3306:3306 mysql:8.0 \
	--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```
- `snu` 라는 Database 명, `animals` 라는 Table 명을 각각 사용합니다.
