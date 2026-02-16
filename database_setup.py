import os

import pymysql
from dotenv import load_dotenv


def get_mysql_config() -> dict:
	load_dotenv()

	def require_env(name: str) -> str:
		value = os.getenv(name)
		if not value:
			raise ValueError(f"Missing required env var: {name}")
		return value

	return {
		"host": require_env("MYSQL_HOST"),
		"port": int(require_env("MYSQL_PORT")),
		"user": require_env("MYSQL_USER"),
		"password": require_env("MYSQL_PASSWORD"),
		"database": require_env("MYSQL_DATABASE"),
		"charset": require_env("MYSQL_CHARSET") if os.getenv("MYSQL_CHARSET") else "utf8mb4",
		"autocommit": True,
	}


def get_mysql_config_without_db() -> dict:
	"""获取不指定数据库的配置（用于创建数据库）"""
	load_dotenv()

	def require_env(name: str) -> str:
		value = os.getenv(name)
		if not value:
			raise ValueError(f"Missing required env var: {name}")
		return value

	return {
		"host": require_env("MYSQL_HOST"),
		"port": int(require_env("MYSQL_PORT")),
		"user": require_env("MYSQL_USER"),
		"password": require_env("MYSQL_PASSWORD"),
		"charset": require_env("MYSQL_CHARSET") if os.getenv("MYSQL_CHARSET") else "utf8mb4",
		"autocommit": True,
	}


def create_database_if_not_exists():
	"""自动创建数据库（如果不存在）"""
	config = get_mysql_config_without_db()
	database_name = os.getenv("MYSQL_DATABASE")

	connection = pymysql.connect(**config)
	try:
		with connection.cursor() as cursor:
			cursor.execute(
				f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
			print(f"数据库 '{database_name}' 检查/创建完成")
	finally:
		connection.close()


TABLE_STATEMENTS = [
	# ========== 原有表 ==========
	"""
	CREATE TABLE IF NOT EXISTS pd_summary (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		contract_no VARCHAR(64) NOT NULL,
		report_date DATE,
		driver_phone VARCHAR(32),
		driver_name VARCHAR(64),
		vehicle_no VARCHAR(32),
		product_name VARCHAR(64),
		weigh_date DATE,
		weigh_ticket_no VARCHAR(64),
		net_weight DECIMAL(12, 3),
		unit_price DECIMAL(12, 2),
		amount DECIMAL(14, 2),
		planned_truck_count INT,
		shipper VARCHAR(64),
		payee VARCHAR(64),
		other_fees DECIMAL(14, 2),
		amount_payable DECIMAL(14, 2),
		payment_schedule_date DATE,
		remarks TEXT,
		remittance_unit_price DECIMAL(12, 2),
		remittance_amount DECIMAL(14, 2),
		received_payment_date DATE,
		arrival_payment_90 DECIMAL(14, 2),
		final_payment_date DATE,
		final_payment_10 DECIMAL(14, 2),
		payout_date DATE,
		payout_details TEXT,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",
	"""
	CREATE TABLE IF NOT EXISTS pd_users (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(64) NOT NULL,
		account VARCHAR(64) NOT NULL UNIQUE,
		password_hash VARCHAR(255) NOT NULL,
		role VARCHAR(32) NOT NULL,
		phone VARCHAR(32),
		email VARCHAR(128),
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
		CHECK (role IN (
			'管理员',
			'大区经理',
			'自营库管理',
			'财务',
			'会计'
		))
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",
	"""
	CREATE TABLE IF NOT EXISTS pd_customers (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		smelter_name VARCHAR(128) NOT NULL,
		address VARCHAR(255),
		contact_person VARCHAR(64),
		contact_phone VARCHAR(32),
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",
	"""
	CREATE TABLE IF NOT EXISTS pd_deliveries (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		shipper VARCHAR(64),
		payee VARCHAR(64),
		other_fees DECIMAL(14, 2),
		report_date DATE,
		driver_phone VARCHAR(32),
		driver_name VARCHAR(64),
		vehicle_no VARCHAR(32),
		product_name VARCHAR(64),
		contract_no VARCHAR(64),
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
		INDEX idx_deliveries_report_date (report_date),
		INDEX idx_deliveries_contract_no (contract_no)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",
	"""
	CREATE TABLE IF NOT EXISTS pd_weighbills (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		weigh_date DATE,
		weigh_ticket_no VARCHAR(64),
		net_weight DECIMAL(12, 3),
		vehicle_no VARCHAR(32),
		contract_no VARCHAR(64),
		unit_price DECIMAL(12, 2),
		total_amount DECIMAL(14, 2),
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
		INDEX idx_weighbills_weigh_date (weigh_date),
		INDEX idx_weighbills_vehicle_no (vehicle_no),
		INDEX idx_weighbills_contract_no (contract_no)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",
	"""
	CREATE TABLE IF NOT EXISTS pd_weighbill_settlements (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		payable_amount DECIMAL(14, 2),
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",
	"""
	CREATE TABLE IF NOT EXISTS pd_receipts (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		remittance_amount DECIMAL(14, 2),
		received_payment_date DATE,
		arrival_payment_90 DECIMAL(14, 2),
		final_payment_date DATE,
		final_payment_10 DECIMAL(14, 2),
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",
	"""
	CREATE TABLE IF NOT EXISTS pd_payout_details (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		payout_amount DECIMAL(14, 2),
		payout_details TEXT,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",

	# ========== 新增合同管理表 ==========
	"""
	CREATE TABLE IF NOT EXISTS pd_contracts (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		seq_no INT UNIQUE COMMENT '序号（自动生成，使用触发器或应用层生成）',
		contract_no VARCHAR(64) NOT NULL UNIQUE COMMENT '合同编号',
		contract_date DATE COMMENT '合同签订日期',
		end_date DATE COMMENT '合同截止日期',
		smelter_company VARCHAR(128) COMMENT '冶炼公司',
		total_quantity DECIMAL(12, 3) COMMENT '合同总数量（吨）',
		arrival_payment_ratio DECIMAL(5, 4) DEFAULT 0.9 COMMENT '到货款比例',
		final_payment_ratio DECIMAL(5, 4) DEFAULT 0.1 COMMENT '尾款比例',
		contract_image_path VARCHAR(255) COMMENT '合同图片路径',
		status VARCHAR(32) DEFAULT '生效中' COMMENT '状态：生效中/已到期/已终止',
		remarks TEXT COMMENT '备注',
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
		INDEX idx_seq_no (seq_no)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",
	"""
	CREATE TABLE IF NOT EXISTS pd_contract_products (
		id BIGINT AUTO_INCREMENT PRIMARY KEY,
		contract_id BIGINT NOT NULL COMMENT '合同ID',
		product_name VARCHAR(64) NOT NULL COMMENT '品种名称',
		unit_price DECIMAL(12, 2) COMMENT '单价（元）',
		sort_order INT DEFAULT 0 COMMENT '排序',
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		FOREIGN KEY (contract_id) REFERENCES pd_contracts(id) ON DELETE CASCADE,
		INDEX idx_contract_id (contract_id)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	""",
]


def create_tables() -> None:
	# 第1步：先创建数据库（如果不存在）
	create_database_if_not_exists()

	# 第2步：创建表
	config = get_mysql_config()
	connection = pymysql.connect(**config)
	try:
		with connection.cursor() as cursor:
			for statement in TABLE_STATEMENTS:
				cursor.execute(statement)
		print("所有数据表创建完成")
	finally:
		connection.close()


if __name__ == "__main__":
	create_tables()