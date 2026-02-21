# PD FastAPI Starter
## 快速开始

### 1) 安装 uv 并创建虚拟环境

```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境
uv venv
```

### 2) 安装依赖

```bash
uv sync
# 如使用 EmailStr 字段，请确保安装 email-validator
uv pip install email-validator
```

### 3) 配置环境变量

推荐使用 .env 文件，以下为最小示例：

```
APP_NAME=PD API
JWT_SECRET=change-me
JWT_ALGORITHM=HS256

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=PD_db
MYSQL_CHARSET=utf8mb4

# 供应用数据库连接使用
DATABASE_URL=mysql+pymysql://root:123456@127.0.0.1:3306/PD_db?charset=utf8mb4
```

### 4) 初始化/同步数据库表结构

```bash
# 一次性创建基础表（或补齐缺失索引/列）
python database_setup.py
```

### 5) 运行应用

```bash
# 快速运行（开发环境）
uv run main.py

# 热重载
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 6) 访问地址

以下示例基于 .env 中 PORT=8007：

- 公网文档地址: http://8.136.35.215:8007/docs
- 内网文档地址: http://172.30.147.217:8007/docs

## API 概览

通用：
- GET /healthz
- GET /init-db

认证：
- POST /api/v1/auth/login

合同管理：
- POST /api/v1/contracts/ocr
- POST /api/v1/contracts/manual
- GET /api/v1/contracts
- GET /api/v1/contracts/{contract_id}
- PUT /api/v1/contracts/{contract_id}
- DELETE /api/v1/contracts/{contract_id}
- POST /api/v1/contracts/export

客户管理：
- POST /api/v1/customers
- GET /api/v1/customers
- GET /api/v1/customers/{customer_id}
- PUT /api/v1/customers/{customer_id}
- DELETE /api/v1/customers/{customer_id}

销售台账/报货订单：
- POST /api/v1/deliveries
- GET /api/v1/deliveries
- GET /api/v1/deliveries/{delivery_id}
- PUT /api/v1/deliveries/{delivery_id}
- DELETE /api/v1/deliveries/{delivery_id}
- POST /api/v1/deliveries/{delivery_id}/upload-order

磅单管理：
- POST /api/v1/weighbills/ocr
- POST /api/v1/weighbills
- GET /api/v1/weighbills
- GET /api/v1/weighbills/{bill_id}
- PUT /api/v1/weighbills/{bill_id}
- DELETE /api/v1/weighbills/{bill_id}
- POST /api/v1/weighbills/{bill_id}/confirm
- GET /api/v1/weighbills/match/delivery
- GET /api/v1/weighbills/contract/price

磅单结余/支付回单相关路由已注册到主路由。

## 安全性说明（当前状态）

- /api/v1/auth/login 目前仅签发 JWT，没有校验账号密码。
- 业务接口未统一接入鉴权与权限控制，存在未授权访问风险。
- JWT_SECRET 有默认值，若未配置会导致弱密钥问题。
- /init-db 公开可访问，生产环境不建议开放。
- 代码中存在另一套用户认证路由，但当前未挂载到主应用。
