"""
异常上报服务 - 异常审核模块
"""
import logging
from typing import Any, Dict, List, Optional

from core.database import get_conn

logger = logging.getLogger(__name__)

STATUS_CHOICES = ("待处理", "已处理")


def _apply_exception_report_aliases(data: Dict[str, Any]) -> None:
    """把前端常用字段名合并到入库字段（就地修改）。"""
    vn = str(data.get("vehicle_no") or "").strip()
    if not vn:
        pn = str(data.get("plate_no") or "").strip()
        if pn:
            data["vehicle_no"] = pn
    desc = data.get("description")
    if desc is None or (isinstance(desc, str) and not desc.strip()):
        ad = data.get("abnormal_desc")
        if ad is not None:
            s = str(ad).strip()
            data["description"] = s or None


class ExceptionReportService:
    """异常上报管理服务"""

    def _resolve_exception_type(
        self,
        exception_type_id: Any,
        abnormal_type: Optional[str],
    ) -> tuple[Optional[int], Optional[str], Optional[str]]:
        """返回 (exception_type_id, exception_type_name, error_message)。"""
        tid: Optional[int] = None
        if exception_type_id is not None and str(exception_type_id).strip() != "":
            try:
                tid = int(exception_type_id)
            except (TypeError, ValueError):
                return None, None, "异常类型 ID 格式不正确"

        name_hint = (abnormal_type or "").strip() or None
        if tid is not None:
            try:
                with get_conn() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "SELECT type_name FROM pd_exception_types WHERE id = %s",
                            (tid,),
                        )
                        row = cur.fetchone()
                        if row:
                            return tid, row["type_name"], None
                        return None, None, f"异常类型 ID {tid} 不存在"
            except Exception as e:
                logger.error(f"查询异常类型失败: {e}")
                return None, None, str(e)

        if name_hint:
            try:
                with get_conn() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "SELECT id, type_name FROM pd_exception_types WHERE type_name = %s",
                            (name_hint,),
                        )
                        row = cur.fetchone()
                        if row:
                            return int(row["id"]), row["type_name"], None
                        return None, name_hint, None
            except Exception as e:
                logger.error(f"按名称查询异常类型失败: {e}")
                return None, None, str(e)

        return None, None, None

    def list_reports(
        self,
        status: Optional[str] = None,
        driver_name: Optional[str] = None,
        vehicle_no: Optional[str] = None,
        exception_type_id: Optional[int] = None,
        reporter: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """分页查询异常上报列表"""
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    conditions = []
                    params: List[Any] = []

                    if status:
                        conditions.append("r.status = %s")
                        params.append(status)
                    if driver_name:
                        conditions.append("r.driver_name LIKE %s")
                        params.append(f"%{driver_name}%")
                    if vehicle_no:
                        conditions.append("r.vehicle_no LIKE %s")
                        params.append(f"%{vehicle_no}%")
                    if exception_type_id:
                        conditions.append("r.exception_type_id = %s")
                        params.append(exception_type_id)
                    if reporter:
                        conditions.append("r.reporter LIKE %s")
                        params.append(f"%{reporter}%")

                    where_clause = " AND ".join(conditions) if conditions else "1=1"
                    count_sql = f"SELECT COUNT(*) as total FROM pd_exception_reports r WHERE {where_clause}"
                    cur.execute(count_sql, params)
                    total = cur.fetchone()["total"]

                    offset = (page - 1) * page_size
                    list_sql = f"""
                        SELECT r.id, r.status, r.driver_name, r.vehicle_no, r.phone,
                               r.exception_type_id, r.exception_type_name, r.description,
                               r.reporter, r.reported_at, r.created_at, r.updated_at
                        FROM pd_exception_reports r
                        WHERE {where_clause}
                        ORDER BY r.reported_at DESC, r.id DESC
                        LIMIT %s OFFSET %s
                    """
                    cur.execute(list_sql, params + [page_size, offset])
                    rows = cur.fetchall()

                    items = []
                    for r in rows:
                        items.append({
                            "id": r["id"],
                            "status": r["status"],
                            "driver_name": r["driver_name"],
                            "vehicle_no": r["vehicle_no"],
                            "phone": r["phone"],
                            "exception_type_id": r["exception_type_id"],
                            "exception_type_name": r["exception_type_name"],
                            "description": r["description"],
                            "reporter": r["reporter"],
                            "reported_at": str(r["reported_at"]) if r.get("reported_at") else None,
                            "created_at": str(r["created_at"]) if r.get("created_at") else None,
                            "updated_at": str(r["updated_at"]) if r.get("updated_at") else None,
                        })

                    return {
                        "success": True,
                        "data": {
                            "items": items,
                            "total": total,
                            "page": page,
                            "page_size": page_size,
                        },
                    }
        except Exception as e:
            logger.error(f"查询异常上报列表失败: {e}")
            return {"success": False, "error": str(e)}

    def get_report(self, report_id: int) -> Optional[Dict[str, Any]]:
        """获取单条异常上报详情"""
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, status, driver_name, vehicle_no, phone,
                               exception_type_id, exception_type_name, description,
                               reporter, reported_at, created_at, updated_at
                        FROM pd_exception_reports
                        WHERE id = %s
                        """,
                        (report_id,),
                    )
                    r = cur.fetchone()
                    if not r:
                        return None
                    return {
                        "id": r["id"],
                        "status": r["status"],
                        "driver_name": r["driver_name"],
                        "vehicle_no": r["vehicle_no"],
                        "phone": r["phone"],
                        "exception_type_id": r["exception_type_id"],
                        "exception_type_name": r["exception_type_name"],
                        "description": r["description"],
                        "reporter": r["reporter"],
                        "reported_at": str(r["reported_at"]) if r.get("reported_at") else None,
                        "created_at": str(r["created_at"]) if r.get("created_at") else None,
                        "updated_at": str(r["updated_at"]) if r.get("updated_at") else None,
                    }
        except Exception as e:
            logger.error(f"获取异常上报详情失败: {e}")
            return None

    def create_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """新增异常上报"""
        data = dict(data)
        _apply_exception_report_aliases(data)

        status = (data.get("status") or "待处理").strip()
        if status not in STATUS_CHOICES:
            return {"success": False, "error": f"异常状态必须是 {'/'.join(STATUS_CHOICES)} 之一"}

        driver_name = (data.get("driver_name") or "").strip() or None
        vehicle_no = (data.get("vehicle_no") or "").strip() or None
        phone = (data.get("phone") or "").strip() or None
        description = (data.get("description") or "").strip() or None
        reporter = (data.get("reporter") or "").strip() or None
        reported_at = data.get("reported_at")  # 可选，不传则用当前时间

        et_id_raw = data.get("exception_type_id")
        abnormal_type = (data.get("abnormal_type") or "").strip() or None
        if et_id_raw is None and abnormal_type is None:
            exception_type_id: Optional[int] = None
            exception_type_name = None
        else:
            exception_type_id, exception_type_name, err = self._resolve_exception_type(
                et_id_raw, abnormal_type
            )
            if err:
                return {"success": False, "error": err}

        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    if reported_at:
                        if isinstance(reported_at, str):
                            reported_at_val = reported_at
                        else:
                            reported_at_val = str(reported_at)
                        cur.execute(
                            """
                            INSERT INTO pd_exception_reports
                            (status, driver_name, vehicle_no, phone, exception_type_id, exception_type_name,
                             description, reporter, reported_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                status,
                                driver_name,
                                vehicle_no,
                                phone,
                                exception_type_id,
                                exception_type_name,
                                description,
                                reporter,
                                reported_at_val,
                            ),
                        )
                    else:
                        cur.execute(
                            """
                            INSERT INTO pd_exception_reports
                            (status, driver_name, vehicle_no, phone, exception_type_id, exception_type_name,
                             description, reporter)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                status,
                                driver_name,
                                vehicle_no,
                                phone,
                                exception_type_id,
                                exception_type_name,
                                description,
                                reporter,
                            ),
                        )
                    report_id = cur.lastrowid
                    return {
                        "success": True,
                        "message": "异常上报成功",
                        "data": {"id": report_id},
                    }
        except Exception as e:
            logger.error(f"新增异常上报失败: {e}")
            return {"success": False, "error": str(e)}

    def update_report(self, report_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """修改异常上报"""
        data = dict(data)
        _apply_exception_report_aliases(data)

        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM pd_exception_reports WHERE id = %s", (report_id,))
                    if not cur.fetchone():
                        return {"success": False, "error": f"异常上报 ID {report_id} 不存在"}

                    allowed_fields = [
                        "status",
                        "driver_name",
                        "vehicle_no",
                        "phone",
                        "exception_type_id",
                        "description",
                        "reporter",
                        "reported_at",
                    ]
                    update_parts = []
                    params: List[Any] = []

                    if "status" in data and data["status"] is not None:
                        status = str(data["status"]).strip()
                        if status not in STATUS_CHOICES:
                            return {"success": False, "error": f"异常状态必须是 {'/'.join(STATUS_CHOICES)} 之一"}
                        update_parts.append("status = %s")
                        params.append(status)

                    if "driver_name" in data:
                        update_parts.append("driver_name = %s")
                        params.append((data["driver_name"] or "").strip() or None)
                    if "vehicle_no" in data or "plate_no" in data:
                        update_parts.append("vehicle_no = %s")
                        params.append((data.get("vehicle_no") or "").strip() or None)
                    if "phone" in data:
                        update_parts.append("phone = %s")
                        params.append((data["phone"] or "").strip() or None)
                    if "exception_type_id" in data or "abnormal_type" in data:
                        et_id_raw = data.get("exception_type_id")
                        abnormal_type = (data.get("abnormal_type") or "").strip() or None
                        if et_id_raw is None and not abnormal_type:
                            exception_type_id = None
                            exception_type_name = None
                        else:
                            exception_type_id, exception_type_name, err = self._resolve_exception_type(
                                et_id_raw, abnormal_type
                            )
                            if err:
                                return {"success": False, "error": err}
                        update_parts.append("exception_type_id = %s")
                        params.append(exception_type_id)
                        update_parts.append("exception_type_name = %s")
                        params.append(exception_type_name)
                    if "description" in data or "abnormal_desc" in data:
                        update_parts.append("description = %s")
                        params.append((data.get("description") or "").strip() or None)
                    if "reporter" in data:
                        update_parts.append("reporter = %s")
                        params.append((data["reporter"] or "").strip() or None)
                    if "reported_at" in data:
                        update_parts.append("reported_at = %s")
                        params.append(data["reported_at"])

                    if not update_parts:
                        return {"success": False, "error": "没有要更新的字段"}

                    params.append(report_id)
                    cur.execute(
                        f"UPDATE pd_exception_reports SET {', '.join(update_parts)} WHERE id = %s",
                        tuple(params),
                    )
                    return {
                        "success": True,
                        "message": "异常上报修改成功",
                        "data": {"id": report_id},
                    }
        except Exception as e:
            logger.error(f"修改异常上报失败: {e}")
            return {"success": False, "error": str(e)}

    def delete_report(self, report_id: int) -> Dict[str, Any]:
        """删除异常上报"""
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM pd_exception_reports WHERE id = %s", (report_id,))
                    if not cur.fetchone():
                        return {"success": False, "error": f"异常上报 ID {report_id} 不存在"}

                    cur.execute("DELETE FROM pd_exception_reports WHERE id = %s", (report_id,))
                    return {
                        "success": True,
                        "message": "异常上报删除成功",
                        "data": {"id": report_id},
                    }
        except Exception as e:
            logger.error(f"删除异常上报失败: {e}")
            return {"success": False, "error": str(e)}


_exception_report_service = None


def get_exception_report_service() -> ExceptionReportService:
    global _exception_report_service
    if _exception_report_service is None:
        _exception_report_service = ExceptionReportService()
    return _exception_report_service
