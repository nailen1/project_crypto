# PostgreSQL Docker 관리 및 pgAdmin 접속 가이드

## Docker 명령어

### 기본 관리

```bash
# 컨테이너 시작 (백그라운드)
docker compose up -d

# 컨테이너 중지
docker compose stop

# 컨테이너 중지 및 삭제 (데이터는 보존)
docker compose down

# 컨테이너 중지 및 삭제 (데이터도 삭제)
docker compose down -v

# 컨테이너 재시작
docker compose restart
```

### 상태 확인

```bash
# 실행 중인 컨테이너 확인
docker compose ps

# 로그 확인
docker compose logs postgres
docker compose logs pgadmin

# 실시간 로그 보기
docker compose logs -f postgres

# 모든 Docker 컨테이너 확인
docker ps

# 리소스 사용량 확인
docker stats
```

### PostgreSQL 직접 접속

```bash
# psql로 접속
docker exec -it quant-postgres psql -U juneyoung -d database_quant

# 데이터베이스 목록
docker exec -it quant-postgres psql -U juneyoung -d postgres -c "\l"

# 테이블 목록
docker exec -it quant-postgres psql -U juneyoung -d database_quant -c "\dt quant.*"
```

---

## pgAdmin 접속

### 1. 브라우저 접속

```bash
# 터미널에서 실행
open http://localhost:5050

# 또는 브라우저에서 직접 입력
# http://localhost:5050
```

### 2. 로그인

- **Email**: `juneyoungpaak@gmail.com`
- **Password**: `Snsksms1202!`

### 3. 서버 추가

#### 3-1. "Add New Server" 클릭

좌측 Object Explorer에서 **Servers** 우클릭 → **Register** → **Server**

또는 중앙의 **"Add New Server"** 버튼 클릭

#### 3-2. General 탭

- **Name**: `Local Quant DB` (원하는 이름)

#### 3-3. Connection 탭

- **Host name/address**: `quant-postgres`
- **Port**: `5432`
- **Maintenance database**: `database_quant`
- **Username**: `juneyoung`
- **Password**: `Snsksms1202!`
- **Save password**: 체크 (선택사항)

#### 3-4. Save 클릭

### 4. 데이터 조회

```
Servers
  └─ Local Quant DB
      └─ Databases
          └─ database_quant
              └─ Schemas
                  └─ quant
                      └─ Tables
                          └─ binance_prices
                              (우클릭) → View/Edit Data → First 100 Rows
```

### 5. SQL 쿼리 실행

- **Tools** → **Query Tool**
- 또는 `binance_prices` 테이블 선택 후 상단 툴바에서 Query Tool 아이콘 클릭

```sql
-- 예시 쿼리
SELECT * FROM quant.binance_prices LIMIT 10;

SELECT COUNT(*) FROM quant.binance_prices;

SELECT DISTINCT datetime FROM quant.binance_prices ORDER BY datetime DESC;
```

---

## 문제 해결

### pgAdmin 접속 안 될 때

```bash
# 컨테이너 상태 확인
docker compose ps

# pgadmin 컨테이너 재시작
docker compose restart pgadmin

# 로그 확인
docker compose logs pgadmin
```

### PostgreSQL 연결 안 될 때

```bash
# 컨테이너 상태 확인
docker compose ps

# PostgreSQL 재시작
docker compose restart postgres

# 로그 확인
docker compose logs postgres
```

### 완전히 초기화

```bash
# 모든 데이터 삭제 후 재시작
docker compose down -v
docker compose up -d
```

---

## 참고사항

- Docker Desktop이 실행 중이어야 합니다
- `docker compose down`은 데이터를 보존합니다 (볼륨 유지)
- `docker compose down -v`는 모든 데이터를 삭제합니다
- pgAdmin은 웹 기반이므로 브라우저만 있으면 됩니다
- Host를 `quant-postgres`로 설정하는 이유: Docker 네트워크 내부 컨테이너명
