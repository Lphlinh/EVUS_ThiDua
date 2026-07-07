"""Teacher monthly scoring page for M02."""

from __future__ import annotations

import streamlit as st

from app.components.score_form_component import (
    FORM_ACTION_CANCEL_SUBMIT,
    FORM_ACTION_CONFIRM_SUBMIT,
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

    cache_key = _score_cache_key(ma_gv, thang)
    cache = st.session_state.setdefault(cache_key, {})

    # Không cache TH_ThiDua Header. Trạng thái/KhoaGV phải luôn đọc mới
    # để sau khi Lưu/Nộp/Chốt không dùng quyền chỉnh sửa cũ.
    phieu = get_phieu(ma_gv, thang)
    if not phieu:
        if not is_teacher_allowed_to_create():
            st.warning(EXPIRED_TEXT)
            return
        phieu = create_phieu_for_teacher(ma_gv, thang)
        st.success("Đã tạo phiếu thi đua tháng cho giáo viên.")

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

    submit_warning_key = _submit_warning_key(id_phieu)

    if action == FORM_ACTION_SAVE:
        if input_errors:
            st.error("Chưa thể lưu vì còn điểm tự chấm vượt thang điểm đánh giá.")
            return
        if not changed_rows:
            st.warning("Không có dòng chi tiết để lưu. Vui lòng kiểm tra dữ liệu CT_ThiDua của phiếu.")
            return
        total = save_teacher_scores(id_phieu, changed_rows, ma_gv)
        st.session_state.pop(cache_key, None)
        st.session_state["m02_confirm_submit"] = False
        st.session_state.pop("m02_pending_changed_rows", None)
        st.session_state.pop("m02_submit_warning_messages", None)
        st.session_state.pop(submit_warning_key, None)
        st.session_state["m02_save_status"] = f"Đã lưu phiếu vào Google Sheets. Tổng điểm hiện hành: {total}"
        st.rerun()

    if action == FORM_ACTION_SUBMIT:
        if input_errors:
            st.error("Chưa thể nộp vì còn điểm tự chấm vượt thang điểm đánh giá.")
            return
        st.session_state["m02_confirm_submit"] = True
        st.session_state["m02_pending_changed_rows"] = changed_rows
        st.session_state.pop("m02_submit_warning_messages", None)
        st.session_state.pop(submit_warning_key, None)
        st.rerun()

    if action == FORM_ACTION_CONFIRM_SUBMIT:
        try:
            # Dùng một nguồn kiểm tra duy nhất: validate_before_submit().
            # Không sinh danh sách cảnh báo riêng ở giao diện để tránh lệch dữ liệu.
            pending_rows = changed_rows or st.session_state.get("m02_pending_changed_rows", [])
            if pending_rows:
                st.session_state["m02_pending_changed_rows"] = pending_rows

            latest_details = _merge_unsaved_changes(details, pending_rows)
            validation_errors = validate_before_submit(latest_details, criteria)
            previous_messages = st.session_state.get("m02_submit_warning_messages") or []
            already_acknowledged = bool(st.session_state.get(submit_warning_key))

            if validation_errors:
                # Nếu danh sách lỗi thay đổi hoặc GV chưa xác nhận sau cảnh báo,
                # cập nhật đúng danh sách từ validate_before_submit() và dừng tại đây.
                if validation_errors != previous_messages or not already_acknowledged:
                    st.session_state["m02_submit_warning_messages"] = validation_errors
                    st.session_state[submit_warning_key] = True
                    st.rerun()

            submit_phieu(id_phieu, ma_gv, pending_rows)
            st.session_state["m02_confirm_submit"] = False
            st.session_state.pop("m02_pending_changed_rows", None)
            st.session_state.pop("m02_submit_warning_messages", None)
            st.session_state.pop(submit_warning_key, None)
            st.session_state.pop(cache_key, None)
            st.success("Đã xác nhận và nộp phiếu thi đua.")
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))

    if action == FORM_ACTION_CANCEL_SUBMIT:
        st.session_state["m02_confirm_submit"] = False
        st.session_state.pop("m02_pending_changed_rows", None)
        st.session_state.pop("m02_submit_warning_messages", None)
        st.session_state.pop(submit_warning_key, None)
        st.rerun()




def _score_cache_key(ma_gv: str, thang: str) -> str:
    return f"m02_score_cache_{ma_gv}_{thang}"


def _submit_warning_key(id_phieu: str) -> str:
    return f"m02_submit_warning_acknowledged_{str(id_phieu).strip()}"


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
    """Render compact score-sheet summary.

    This replaces large Streamlit metric cards to keep the scoring table close
    to the application header. It only changes presentation, not workflow.
    """
    thang = str(phieu.get("Thang", "")).strip()
    title = f"Phiếu thi đua tháng {thang}" if thang else "Phiếu thi đua tháng"
    status = _status_text(phieu.get("TrangThai"))
    submit_date = str(phieu.get("NgayNop", "") or "Chưa nộp").strip()
    total_score = str(phieu.get("TongDiem", "") or "0").strip()
    mode_text = "Chỉ xem" if readonly else "Được chỉnh sửa"
    id_phieu = str(phieu.get("ID", "")).strip()
    lan_nop = str(phieu.get("LanNop", 0)).strip()
    lan_mo_khoa = str(phieu.get("LanMoKhoa", 0)).strip()

    st.markdown(
        f'''
        <style>
        .ev-teacher-summary {{
            border: 1px solid rgba(128, 128, 128, 0.24);
            border-radius: 0.55rem;
            padding: 0.5rem 0.7rem;
            margin: 0.2rem 0 0.45rem 0;
            background: #ffffff;
            color: #2f3340;
        }}
        .ev-teacher-summary-title {{
            font-size: 1.05rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 0.25rem;
        }}
        .ev-teacher-summary-line {{
            font-size: 0.82rem;
            line-height: 1.45;
            color: rgba(47, 51, 64, 0.82);
        }}
        .ev-teacher-summary-line b {{
            color: #2f3340;
            font-weight: 700;
        }}
        </style>
        <div class="ev-teacher-summary">
            <div class="ev-teacher-summary-title">{_html_escape(title)}</div>
            <div class="ev-teacher-summary-line">
                <b>Trạng thái:</b> {_html_escape(status)}
                &nbsp;|&nbsp; <b>Ngày nộp:</b> {_html_escape(submit_date)}
                &nbsp;|&nbsp; <b>Tổng điểm lưu:</b> {_html_escape(total_score)}
                &nbsp;|&nbsp; <b>Chế độ:</b> {_html_escape(mode_text)}
            </div>
            <div class="ev-teacher-summary-line">
                <b>ID:</b> {_html_escape(id_phieu)}
                &nbsp;|&nbsp; <b>Lần nộp:</b> {_html_escape(lan_nop)}
                &nbsp;|&nbsp; <b>Lần mở khóa:</b> {_html_escape(lan_mo_khoa)}
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def _html_escape(value: object) -> str:
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
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
