"""Teacher monthly scoring page for M02."""

from __future__ import annotations

import streamlit as st

from app.components.score_form_component import (
    FORM_ACTION_SAVE,
    FORM_ACTION_SUBMIT,
    render_score_form,
)
from app.services.criteria_service import get_all_criteria
from app.services.thi_dua_service import (
    create_phieu_for_teacher,
    get_chi_tiet_phieu,
    get_current_scoring_month,
    get_phieu,
    is_teacher_allowed_to_create,
    is_teacher_allowed_to_edit,
    save_teacher_scores,
    submit_phieu,
    validate_before_submit,
)

SUBMIT_CONFIRM_TEXT = """Sau khi xác nhận, phiếu thi đua được xem như đã được Thầy/Cô ký xác nhận và gửi về Ban Giám hiệu. Thầy/Cô sẽ không thể chỉnh sửa nội dung phiếu sau bước này.

Thầy/Cô có chắc chắn muốn xác nhận và nộp phiếu không?"""

EXPIRED_TEXT = """Đã hết thời gian tự chấm phiếu thi đua của tháng này (từ ngày 01 đến ngày 05 hằng tháng). Nếu có lý do đặc biệt, Thầy/Cô vui lòng liên hệ Ban Giám hiệu để được xem xét mở quyền chấm bổ sung."""


def render_teacher_score_page() -> None:
    """Render teacher scoring workflow."""
    teacher = _get_logged_in_teacher()
    if not teacher:
        st.warning("Thầy/Cô cần đăng nhập trước khi chấm phiếu thi đua.")
        return

    ma_gv = str(teacher.get("ma_gv") or teacher.get("MaGV") or "").strip()
    if not ma_gv:
        st.error("Không xác định được mã giáo viên trong phiên đăng nhập.")
        return

    thang = get_current_scoring_month()
    st.title(f"Phiếu thi đua tháng {thang}")

    cache_key = _score_cache_key(ma_gv, thang)
    cache = st.session_state.setdefault(cache_key, {})

    phieu = cache.get("phieu")
    if not phieu:
        phieu = get_phieu(ma_gv, thang)
        if not phieu:
            if not is_teacher_allowed_to_create():
                st.warning(EXPIRED_TEXT)
                return
            phieu = create_phieu_for_teacher(ma_gv, thang)
            st.success("Đã tạo phiếu thi đua tháng cho giáo viên.")
        cache["phieu"] = phieu

    id_phieu = str(phieu.get("ID", "")).strip()
    if "details" not in cache:
        cache["details"] = get_chi_tiet_phieu(id_phieu)
    if "criteria" not in cache:
        cache["criteria"] = get_all_criteria()

    details = cache["details"]
    criteria = cache["criteria"]
    readonly = not is_teacher_allowed_to_edit(phieu)

    _render_header_info(phieu, readonly)
    save_status = st.session_state.pop("m02_save_status", "")
    if save_status:
        st.success(save_status)
    changed_rows, current_total, action, input_errors = render_score_form(criteria, details, readonly=readonly)

    if readonly:
        st.info("Phiếu đã khóa. Thầy/Cô chỉ được xem lại, không được chỉnh sửa.")
        return

    if action == FORM_ACTION_SAVE:
        if input_errors:
            st.error("Chưa thể lưu vì còn điểm tự chấm vượt thang điểm đánh giá.")
            return
        if not changed_rows:
            st.warning("Không có dòng chi tiết để lưu. Vui lòng kiểm tra dữ liệu CT_ThiDua của phiếu.")
            return
        total = save_teacher_scores(id_phieu, changed_rows, ma_gv)
        st.session_state.pop(cache_key, None)
        st.session_state["m02_save_status"] = f"Đã lưu phiếu vào Google Sheets. Tổng điểm hiện hành: {total}"
        st.rerun()

    if action == FORM_ACTION_SUBMIT:
        if input_errors:
            st.error("Chưa thể nộp vì còn điểm tự chấm vượt thang điểm đánh giá.")
            return
        st.session_state["m02_confirm_submit"] = True
        st.session_state["m02_pending_changed_rows"] = changed_rows

    if st.session_state.get("m02_confirm_submit"):
        confirm_text_html = SUBMIT_CONFIRM_TEXT.replace(chr(10), "<br>")
        st.markdown(
            f'''
            <div style="max-width: 980px; margin: 0.75rem auto; padding: 1rem 1.25rem; border: 1px solid #f59e0b; background: #fff7ed; color: #92400e; border-radius: 0.5rem; line-height: 1.55;">
                <b>Xác nhận nộp phiếu</b><br>
                {confirm_text_html}
            </div>
            ''',
            unsafe_allow_html=True,
        )
        left_pad, confirm_col, cancel_col, right_pad = st.columns([0.8, 1.1, 1.1, 0.8])

        with confirm_col:
            if st.button("Đồng ý nộp", type="primary", use_container_width=True):
                try:
                    pending_rows = st.session_state.get("m02_pending_changed_rows", changed_rows)
                    latest_details = _merge_unsaved_changes(details, pending_rows)
                    errors = validate_before_submit(latest_details)
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        submit_phieu(id_phieu, ma_gv, pending_rows)
                        st.session_state["m02_confirm_submit"] = False
                        st.session_state.pop("m02_pending_changed_rows", None)
                        st.session_state.pop(cache_key, None)
                        st.success("Đã xác nhận và nộp phiếu thi đua.")
                        st.rerun()
                except ValueError as exc:
                    st.error(str(exc))

        with cancel_col:
            if st.button("Hủy", use_container_width=True):
                st.session_state["m02_confirm_submit"] = False
                st.session_state.pop("m02_pending_changed_rows", None)
                st.rerun()


def _score_cache_key(ma_gv: str, thang: str) -> str:
    return f"m02_score_cache_{ma_gv}_{thang}"


def _apply_changed_rows_to_cache(cache: dict, changed_rows: list[dict]) -> None:
    if not changed_rows:
        return
    detail_by_id = {str(row.get("ID", "")).strip(): dict(row) for row in cache.get("details", [])}
    for changed in changed_rows:
        row_id = str(changed.get("ID", "")).strip()
        if row_id in detail_by_id:
            detail_by_id[row_id].update(changed)
    cache["details"] = list(detail_by_id.values())


def _get_logged_in_teacher() -> dict | None:
    """Read teacher identity from common Streamlit session keys."""
    for key in ("teacher", "user", "current_user", "auth_user"):
        value = st.session_state.get(key)
        if isinstance(value, dict):
            return value
    return None


def _render_header_info(phieu: dict, readonly: bool) -> None:
    col_status, col_submit_date = st.columns(2)
    with col_status:
        st.metric("Trạng thái", _status_text(phieu.get("TrangThai")))
    with col_submit_date:
        st.metric("Ngày nộp", phieu.get("NgayNop", "") or "Chưa nộp")

    st.caption(
        f"ID phiếu: {phieu.get('ID', '')} | Lần nộp: {phieu.get('LanNop', 0)} | "
        f"Lần mở khóa: {phieu.get('LanMoKhoa', 0)} | Chế độ: {'Chỉ xem' if readonly else 'Được chỉnh sửa'}"
    )


def _status_text(value: object) -> str:
    mapping = {
        1: "Chưa tạo",
        2: "Đang chấm",
        3: "Đã nộp",
        4: "BGH đã chỉnh sửa",
        5: "Đã chốt",
    }
    try:
        return mapping.get(int(value or 0), str(value))
    except ValueError:
        return str(value)


def _merge_unsaved_changes(details: list[dict], changed_rows: list[dict]) -> list[dict]:
    detail_by_id = {str(row.get("ID", "")).strip(): dict(row) for row in details}
    for changed in changed_rows:
        row_id = str(changed.get("ID", "")).strip()
        if row_id in detail_by_id:
            detail_by_id[row_id].update(changed)
    return list(detail_by_id.values())
