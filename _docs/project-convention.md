# Project Convention

이 문서는 Crypto ETL 프로젝트의 네이밍 컨벤션과 구조 설계 원칙을 정의합니다.

## 네이밍 컨벤션 원칙

### 1. 도메인 중심 설계 (Domain-Driven Design)

모든 구성요소는 **도메인(암호화폐)**을 중심으로 명명됩니다.

```
crypto_etl          # 도메인: 암호화폐 ETL
├── project-crypto  # 서비스: 암호화폐 프로젝트
├── container-crypto # 컨테이너: 암호화폐 컨테이너
├── database_crypto # 데이터베이스: 암호화폐 데이터
└── schema_crypto   # 스키마: 암호화폐 스키마
```

### 2. 계층별 접두사 사용

각 계층별로 일관된 접두사를 사용하여 역할을 명확히 구분합니다.

| 계층         | 접두사              | 예시                | 설명              |
| ------------ | ------------------- | ------------------- | ----------------- |
| 프로젝트     | `project-`          | `project-crypto`    | 전체 프로젝트     |
| 서비스       | `project-`          | `project-crypto`    | Docker 서비스     |
| 컨테이너     | `container-`        | `container-crypto`  | Docker 컨테이너   |
| 데이터베이스 | `database_`         | `database_crypto`   | PostgreSQL DB     |
| 스키마       | `schema_`           | `schema_crypto`     | PostgreSQL 스키마 |
| 테이블       | `{type}_{exchange}` | `prices_binance`    | 데이터 테이블     |

### 3. 일관성 유지

모든 구성요소는 동일한 도메인 키워드(`crypto`)를 사용하여 일관성을 유지합니다.

## 구조 설계 원칙

### 1. 논리적 계층 구조

```
Docker Container (container-crypto)
└── PostgreSQL Server
    └── database_crypto (데이터베이스)
        ├── public (기본 스키마)
        ├── quant (정량분석 스키마)
        └── schema_crypto (암호화폐 스키마)
            └── prices_binance (Binance 가격 테이블)
```

### 2. 역할 분리

- **데이터베이스**: `database_crypto` - 암호화폐 데이터 저장소
- **스키마**: `schema_crypto` - 암호화폐 관련 테이블들
- **테이블**: `prices_binance` - Binance 가격 데이터

### 3. 확장성 고려

향후 새로운 거래소나 데이터 타입 추가 시 일관된 네이밍을 유지합니다.

```sql
-- 향후 추가 가능한 테이블들
schema_crypto.prices_binance     -- Binance 가격
schema_crypto.prices_upbit       -- Upbit 가격
schema_crypto.prices_coinbase    -- Coinbase 가격
schema_crypto.volumes_binance    -- Binance 거래량
schema_crypto.volumes_upbit      -- Upbit 거래량
schema_crypto.market_cap         -- 시가총액 데이터
```

## 환경변수 컨벤션

### 1. 필수 환경변수

```bash
# 데이터베이스 설정
DB_NAME=database_crypto    # 데이터베이스명
DB_USER=juneyoung         # 사용자명
DB_PASSWORD=secure_pass   # 비밀번호

# pgAdmin 설정
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin_pass
```

### 2. 네이밍 규칙

- 모든 환경변수는 대문자 사용
- 단어 구분은 언더스코어(`_`) 사용
- 의미있는 이름 사용 (약어 지양)

## 파일 구조 컨벤션

### 1. 디렉토리 구조

```
module-crypto_etl/
├── _docs/                    # 문서
│   ├── project-convention.md # 이 파일
│   └── manage-postgre.md     # PostgreSQL 관리
├── crypto_etl/              # 메인 패키지
│   └── database_manager/     # 데이터베이스 관리
├── data/                     # 데이터 저장소
├── docker-compose.yml        # Docker 설정
├── Dockerfile               # Docker 이미지
├── init.sql                 # DB 초기화
└── README.md                # 프로젝트 설명
```

### 2. 파일 네이밍

- **설정 파일**: `kebab-case` (예: `docker-compose.yml`)
- **스크립트 파일**: `snake_case` (예: `init.sql`)
- **문서 파일**: `kebab-case` (예: `project-convention.md`)

## 코드 컨벤션

### 1. Python 코드

```python
# 테이블명은 스키마 포함
table_name = 'schema_crypto.prices_binance'

# 함수명은 snake_case
def insert_binance_data(data: List[Dict], table_name: str = 'schema_crypto.prices_binance'):
    pass
```

### 2. SQL 쿼리

```sql
-- 스키마명 명시적 사용
SELECT * FROM schema_crypto.prices_binance;

-- 테이블명은 {데이터타입}_{거래소} 형식
CREATE TABLE schema_crypto.prices_binance (
    id UUID PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    price NUMERIC(20, 8)
);

-- 거래소별, 데이터 타입별 테이블 생성
CREATE TABLE schema_crypto.prices_upbit (...);
CREATE TABLE schema_crypto.volumes_binance (...);
CREATE TABLE schema_crypto.volumes_upbit (...);
```

## 장점

### 1. 명확성

- 이름만으로 역할과 목적을 파악 가능
- 새로운 개발자도 쉽게 이해

### 2. 일관성

- 모든 구성요소가 동일한 네이밍 규칙
- 혼동과 오류 최소화

### 3. 확장성

- 새로운 기능 추가 시 일관된 패턴 유지
- 리팩토링 비용 절약

### 4. 유지보수성

- 구조가 단순하고 논리적
- 문서화 비용 절약

## 적용 방법

### 1. 새 프로젝트 시작 시

1. 도메인 키워드 정의
2. 계층별 접두사 결정
3. 환경변수 구조 설계
4. 파일 구조 계획

### 2. 기존 프로젝트 개선 시

1. 현재 구조 분석
2. 일관성 없는 부분 식별
3. 점진적 리팩토링
4. 문서화 업데이트

## 참고사항

- 이 컨벤션은 프로젝트의 특성에 맞게 조정 가능
- 팀 내 합의를 통해 변경 사항 결정
- 변경 시 모든 관련 문서 업데이트 필요

---

**작성일**: 2025-01-02  
**작성자**: Crypto ETL Team  
**버전**: 1.0.0
