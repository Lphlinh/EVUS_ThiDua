"""BGH score review/edit page for M03.2.

This page only handles BGH workflow: choose month, choose teacher form,
then delegate the actual score form rendering to score_form_component.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from app.components.score_form_component import FORM_ACTION_SAVE, FORM_MODE_BGH, render_score_form
from app.services.criteria_service import get_all_criteria
from app.services.account_service import normalize_missing_password_hashes
from app.services.config_service import (
    get_teacher_scoring_deadline_day,
    set_teacher_scoring_deadline_day,
)
from app.services.google_sheets_service import read_sheet_records
from app.services.teacher_service import get_all_teachers
from app.services.thi_dua_service import (
    build_monthly_excel_export,
    finalize_month,
    summarize_month,
    repair_th_ids_for_month,
    get_chi_tiet_phieu,
    get_current_scoring_month,
    save_bgh_scores,
)

SHEET_TH = "TH_ThiDua"

STATUS_TEXT = {
    1: "Chưa tạo",
    2: "Đang chấm",
    3: "Đã nộp",
    4: "BGH đã chỉnh sửa",
    5: "Đã chốt",
}

TH_ALIASES = {
    "ID": ("ID", "id"),
    "NamHoc": ("NamHoc", "Năm học", "nam_hoc", "namhoc"),
    "Thang": ("Thang", "Tháng", "thang"),
    "MaGV": ("MaGV", "Mã GV", "ma_gv", "magv"),
    "TrangThai": ("TrangThai", "Trạng thái phiếu", "Trạng thái", "trang_thai", "trangthai"),
    "TongDiem": ("TongDiem", "Tổng điểm", "tong_diem", "tongdiem"),
    "NgayNop": ("NgayNop", "Ngày nộp", "ngay_nop", "ngaynop"),
    "LanNop": ("LanNop", "Lần nộp", "lan_nop", "lannop"),
    "LanMoKhoa": ("LanMoKhoa", "Lần mở khóa", "lan_mo_khoa", "lanmokhoa"),
    "KhoaGV": ("KhoaGV", "Khóa GV", "khoa_gv", "khoagv"),
    "KhoaBGH": ("KhoaBGH", "Khóa BGH", "khoa_bgh", "khoabgh"),
    "NgayCapNhat": ("NgayCapNhat", "Thời gian cập nhật", "Ngày cập nhật", "ngay_cap_nhat"),
}

CT_ALIASES = {
    "ID": ("ID", "id"),
    "IDPhieu": ("IDPhieu", "ID Phiếu", "id_phieu", "idphieu"),
    "MaTC": ("MaTC", "Mã TC", "ma_tc", "MaTieuChi", "Mã tiêu chí", "ma_tieu_chi"),
    "DiemGV": ("DiemGV", "Điểm GV", "Điểm giáo viên", "Điểm GV chấm", "Tự chấm", "diem_gv", "diemgv"),
    "DiemBGH": ("DiemBGH", "Điểm BGH", "Điểm BGH chỉnh", "diem_bgh", "diembgh"),
}


def render_bgh_score_page() -> None:
    """Render BGH monthly score review/edit workflow."""
    user = _get_logged_in_user()
    if not user:
        st.warning("Cần đăng nhập trước khi xem màn hình Ban Giám hiệu.")
        return

    if not _is_bgh_user(user):
        st.error("Tài khoản hiện tại không có quyền truy cập màn hình Ban Giám hiệu.")
        return

    _render_bgh_compact_css()

    default_month = get_current_scoring_month()
    st.markdown(
        '<div class="ev-bgh-page-title">Ban Giám hiệu - Chỉnh điểm thi đua</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Vai trò: BGH | Kỳ đánh giá: {default_month}")

    top_left, top_right = st.columns([2.1, 1.2], gap="small")
    with top_left:
        with st.container(border=True):
            st.markdown('<div class="ev-bgh-card-title">Thông tin chấm điểm thi đua</div>', unsafe_allow_html=True)
            thang = st.text_input("Tháng chấm", value=default_month, help="Định dạng MM/YYYY, ví dụ 06/2026.")
    with top_right:
        with st.container(border=True):
            _render_system_admin_panel(compact=True)

    normalized_month = _normalize_month_key(thang)

    try:
        repair_result = repair_th_ids_for_month(normalized_month)
        if repair_result.get("repaired_count", 0):
            st.warning(
                f"Đã phát hiện và sửa {repair_result.get('repaired_count')} khóa ID phiếu không hợp lệ trong TH_ThiDua."
            )
    except ValueError as exc:
        st.error(str(exc))
        return

    phieu_list = _get_phieu_list_by_month(normalized_month)
    teacher_map = _get_teacher_map()

    finalize_status = st.session_state.pop("m03_finalize_status", "")
    if finalize_status:
        st.success(finalize_status)

    summary_status = st.session_state.pop("m03_summary_status", "")
    if summary_status:
        st.success(summary_status)

    options = {
        _format_select_label(phieu, teacher_map): str(phieu.get("ID", "")).strip()
        for phieu in phieu_list
        if str(phieu.get("ID", "")).strip()
    }

    action_cols = st.columns(4, gap="small")
    with action_cols[0]:
        selected_id = _render_select_phieu_card(options)
    with action_cols[1]:
        _render_finalize_month_card(normalized_month, phieu_list, teacher_map)
    with action_cols[2]:
        _render_summarize_month_card(normalized_month, phieu_list)
    with action_cols[3]:
        _render_export_month_excel_card(normalized_month)

    if not phieu_list:
        st.info(f"Chưa có phiếu thi đua cho tháng {normalized_month or thang}.")
        return

    selected_phieu_id = st.session_state.get("m03_bgh_selected_phieu_id") or selected_id
    if selected_phieu_id:
        selected_phieu = next((item for item in phieu_list if str(item.get("ID", "")).strip() == selected_phieu_id), None)
        if not selected_phieu:
            st.warning("Phiếu đã chọn không còn trong danh sách tháng hiện tại.")
            return
        _render_selected_phieu(selected_phieu, teacher_map)


def _render_bgh_compact_css() -> None:
    """Attach compact CSS for the BGH control area only."""
    st.markdown(
        """
        <style>
        .ev-bgh-page-title {
            font-size: 1.85rem;
            font-weight: 800;
            line-height: 1.12;
            margin: 0.2rem 0 0.1rem 0;
        }
        .ev-bgh-card-title {
            font-weight: 750;
            font-size: 0.95rem;
            margin-bottom: 0.35rem;
        }
        .ev-bgh-card-caption {
            opacity: 0.72;
            font-size: 0.78rem;
            line-height: 1.2;
            margin-bottom: 0.45rem;
        }
        .ev-bgh-card-metric {
            font-size: 1.25rem;
            font-weight: 750;
            line-height: 1.1;
            margin: 0.15rem 0 0.35rem 0;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            padding-top: 0.45rem !important;
            padding-bottom: 0.45rem !important;
        }
        div[data-testid="stMetric"] {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        div[data-testid="stMetric"] label {
            font-size: 0.72rem !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.15rem !important;
        }

        .ev-bgh-detail-title {
            font-size: 1.25rem;
            font-weight: 800;
            margin: 0.55rem 0 0.35rem 0;
        }
        .ev-bgh-info-label {
            color: rgba(49, 51, 63, 0.68);
            font-size: 0.72rem;
            line-height: 1.15;
            margin-bottom: 0.05rem;
            white-space: nowrap;
        }
        .ev-bgh-info-value {
            font-size: 0.82rem;
            font-weight: 650;
            line-height: 1.15;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            margin-bottom: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_select_phieu_card(options: dict[str, str]) -> str:
    """Render compact selected-form action card and return selected form ID."""
    with st.container(border=True):
        st.markdown('<div class="ev-bgh-card-title">Chọn phiếu xử lý</div>', unsafe_allow_html=True)
        if not options:
            st.info("Không đọc được ID phiếu trong TH_ThiDua.")
            return ""
        selected_label = st.selectbox("Phiếu xem/chỉnh", list(options.keys()), label_visibility="collapsed")
        selected_id = options[selected_label]
        if st.button("Xem / Chỉnh phiếu", type="primary", use_container_width=True):
            st.session_state["m03_bgh_selected_phieu_id"] = selected_id
            st.rerun()
        return selected_id


def _render_finalize_month_card(thang: str, phieu_list: list[dict], teacher_map: dict[str, dict]) -> None:
    """Render compact finalization card."""
    normalized_month = _normalize_month_key(thang)
    eligible = [phieu for phieu in phieu_list if _safe_int(phieu.get("TrangThai"), default=0) in {3, 4}]
    finalized = [phieu for phieu in phieu_list if _safe_int(phieu.get("TrangThai"), default=0) == 5]
    unsubmitted = [phieu for phieu in phieu_list if _safe_int(phieu.get("TrangThai"), default=0) not in {3, 4, 5}]
    phieu_teacher_codes = {
        str(phieu.get("MaGV", "")).strip()
        for phieu in phieu_list
        if str(phieu.get("MaGV", "")).strip()
    }
    no_form_teachers = [
        teacher for ma_gv, teacher in teacher_map.items()
        if ma_gv not in phieu_teacher_codes and not _is_bgh_user(teacher)
    ]

    with st.container(border=True):
        st.markdown('<div class="ev-bgh-card-title">Chốt tháng</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            st.metric("Có thể", len(eligible))
        with cols[1]:
            st.metric("Đã chốt", len(finalized))
        with cols[2]:
            st.metric("Chưa nộp", len(unsubmitted) + len(no_form_teachers))
        if unsubmitted or no_form_teachers:
            with st.expander("Danh sách chưa nộp/chưa có", expanded=False):
                for phieu in unsubmitted:
                    ma_gv = str(phieu.get("MaGV", "")).strip()
                    teacher = teacher_map.get(ma_gv, {})
                    name = teacher.get("ho_ten") or ma_gv or "Không rõ"
                    st.write(f"- {ma_gv} - {name}: {_status_text(phieu.get('TrangThai'))}")
                for teacher in no_form_teachers:
                    ma_gv = str(teacher.get("ma_gv", "")).strip()
                    name = teacher.get("ho_ten") or ma_gv or "Không rõ"
                    st.write(f"- {ma_gv} - {name}: Chưa có phiếu")
        if not eligible:
            st.button("Chốt tháng", disabled=True, use_container_width=True)
            return
        confirm_key = f"m03_confirm_finalize_{normalized_month}"
        if st.button("Chốt tháng", type="primary", use_container_width=True):
            st.session_state[confirm_key] = True
            st.rerun()

    if not st.session_state.get(confirm_key):
        return

    st.error(
        f"Xác nhận chốt tháng {normalized_month}. Sau khi chốt, giáo viên và BGH chỉ được xem, không được chỉnh sửa các phiếu đã chốt."
    )
    confirm_col, cancel_col, _ = st.columns([1.1, 1.1, 4])
    with confirm_col:
        if st.button("Xác nhận chốt tháng", type="primary", use_container_width=True):
            try:
                actor = _resolve_actor_code(_get_logged_in_user() or {})
                result = finalize_month(normalized_month, actor)
                st.session_state["m03_finalize_status"] = (
                    f"Đã chốt tháng {result.get('thang')}. "
                    f"Số phiếu chốt: {result.get('finalized_count', 0)}. "
                    f"Số phiếu chưa nộp/bỏ qua: {result.get('unsubmitted_count', 0)}."
                )
                st.session_state[confirm_key] = False
                st.session_state.pop("m03_bgh_selected_phieu_id", None)
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
    with cancel_col:
        if st.button("Hủy chốt tháng", use_container_width=True):
            st.session_state[confirm_key] = False
            st.rerun()


def _render_summarize_month_card(thang: str, phieu_list: list[dict]) -> None:
    """Render compact summary card."""
    normalized_month = _normalize_month_key(thang)
    finalized = [phieu for phieu in phieu_list if _safe_int(phieu.get("TrangThai"), default=0) == 5]
    with st.container(border=True):
        st.markdown('<div class="ev-bgh-card-title">Tổng hợp tháng</div>', unsafe_allow_html=True)
        st.metric("Phiếu đã chốt", len(finalized))
        if not finalized:
            st.button("Tổng hợp tháng", disabled=True, use_container_width=True)
            return
        if st.button("Tổng hợp tháng", type="primary", use_container_width=True):
            try:
                actor = _resolve_actor_code(_get_logged_in_user() or {})
                result = summarize_month(normalized_month, actor)
                st.session_state["m03_summary_status"] = (
                    f"Đã tổng hợp tháng {result.get('thang')}. "
                    f"Số dòng: {result.get('summary_count', 0)}. "
                    f"Thêm mới: {result.get('created_count', 0)}. "
                    f"Cập nhật: {result.get('updated_count', 0)}."
                )
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))


def _render_export_month_excel_card(thang: str) -> None:
    """Render compact Excel export card."""
    normalized_month = _normalize_month_key(thang)
    with st.container(border=True):
        st.markdown('<div class="ev-bgh-card-title">Xuất Excel tháng</div>', unsafe_allow_html=True)
        try:
            filename, file_bytes, row_count = build_monthly_excel_export(normalized_month)
        except ValueError as exc:
            st.info(str(exc))
            st.button("Tải Excel", disabled=True, use_container_width=True)
            return
        st.metric("Số dòng", row_count)
        st.download_button(
            "Tải Excel tổng hợp",
            data=file_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True,
        )


def _render_finalize_month_panel(thang: str, phieu_list: list[dict], teacher_map: dict[str, dict]) -> None:
    """Render BGH month-finalization panel with unsubmitted warning."""
    normalized_month = _normalize_month_key(thang)
    eligible = [
        phieu for phieu in phieu_list
        if _safe_int(phieu.get("TrangThai"), default=0) in {3, 4}
    ]
    finalized = [
        phieu for phieu in phieu_list
        if _safe_int(phieu.get("TrangThai"), default=0) == 5
    ]
    unsubmitted = [
        phieu for phieu in phieu_list
        if _safe_int(phieu.get("TrangThai"), default=0) not in {3, 4, 5}
    ]

    phieu_teacher_codes = {
        str(phieu.get("MaGV", "")).strip()
        for phieu in phieu_list
        if str(phieu.get("MaGV", "")).strip()
    }
    no_form_teachers = [
        teacher for ma_gv, teacher in teacher_map.items()
        if ma_gv not in phieu_teacher_codes and not _is_bgh_user(teacher)
    ]

    st.divider()
    st.subheader("Chốt tháng")
    st.caption(
        "Chỉ chốt các phiếu đã nộp hoặc đã được BGH chỉnh sửa. "
        "Phiếu chưa nộp hoặc giáo viên chưa có phiếu sẽ không bị ép chốt."
    )

    col_ready, col_finalized, col_pending = st.columns(3)
    with col_ready:
        st.metric("Có thể chốt", len(eligible))
    with col_finalized:
        st.metric("Đã chốt", len(finalized))
    with col_pending:
        st.metric("Chưa nộp/chưa có phiếu", len(unsubmitted) + len(no_form_teachers))

    if unsubmitted or no_form_teachers:
        st.warning("Còn giáo viên chưa nộp phiếu hoặc chưa có phiếu trong tháng này.")
        with st.expander("Xem danh sách chưa nộp/chưa có phiếu", expanded=False):
            for phieu in unsubmitted:
                ma_gv = str(phieu.get("MaGV", "")).strip()
                teacher = teacher_map.get(ma_gv, {})
                name = teacher.get("ho_ten") or ma_gv or "Không rõ"
                st.write(f"- {ma_gv} - {name}: {_status_text(phieu.get('TrangThai'))}")
            for teacher in no_form_teachers:
                ma_gv = str(teacher.get("ma_gv", "")).strip()
                name = teacher.get("ho_ten") or ma_gv or "Không rõ"
                st.write(f"- {ma_gv} - {name}: Chưa có phiếu")

    if not eligible:
        st.info("Không có phiếu trạng thái Đã nộp hoặc BGH đã chỉnh sửa để chốt trong tháng này.")
        return

    confirm_key = f"m03_confirm_finalize_{normalized_month}"
    if st.button("Chốt tháng", type="primary", use_container_width=False):
        st.session_state[confirm_key] = True
        st.rerun()

    if not st.session_state.get(confirm_key):
        return

    st.error(
        f"Xác nhận chốt tháng {normalized_month}. Sau khi chốt, giáo viên và BGH chỉ được xem, không được chỉnh sửa các phiếu đã chốt."
    )
    confirm_col, cancel_col, _ = st.columns([1.1, 1.1, 4])
    with confirm_col:
        if st.button("Xác nhận chốt tháng", type="primary", use_container_width=True):
            try:
                actor = _resolve_actor_code(_get_logged_in_user() or {})
                result = finalize_month(normalized_month, actor)
                st.session_state["m03_finalize_status"] = (
                    f"Đã chốt tháng {result.get('thang')}. "
                    f"Số phiếu chốt: {result.get('finalized_count', 0)}. "
                    f"Số phiếu chưa nộp/bỏ qua: {result.get('unsubmitted_count', 0)}."
                )
                st.session_state[confirm_key] = False
                st.session_state.pop("m03_bgh_selected_phieu_id", None)
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
    with cancel_col:
        if st.button("Hủy chốt tháng", use_container_width=True):
            st.session_state[confirm_key] = False
            st.rerun()


def _render_summarize_month_panel(thang: str, phieu_list: list[dict]) -> None:
    """Render monthly summary action after finalization."""
    normalized_month = _normalize_month_key(thang)
    finalized = [
        phieu for phieu in phieu_list
        if _safe_int(phieu.get("TrangThai"), default=0) == 5
    ]

    st.divider()
    st.subheader("Tổng hợp tháng")
    st.caption("Chỉ tổng hợp các phiếu đã chốt. Chạy lại sẽ cập nhật dòng đã có, không tạo trùng.")

    if not finalized:
        st.info("Chưa có phiếu đã chốt để tổng hợp trong tháng này.")
        return

    st.metric("Số phiếu đã chốt có thể tổng hợp", len(finalized))
    if st.button("Tổng hợp tháng", type="primary", use_container_width=False):
        try:
            actor = _resolve_actor_code(_get_logged_in_user() or {})
            result = summarize_month(normalized_month, actor)
            st.session_state["m03_summary_status"] = (
                f"Đã tổng hợp tháng {result.get('thang')}. "
                f"Số dòng: {result.get('summary_count', 0)}. "
                f"Thêm mới: {result.get('created_count', 0)}. "
                f"Cập nhật: {result.get('updated_count', 0)}."
            )
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))



def _render_export_month_excel_panel(thang: str) -> None:
    """Render monthly Excel export action from TongHop_ThiDua."""
    normalized_month = _normalize_month_key(thang)
    st.divider()
    st.subheader("Xuất Excel tháng")
    st.caption("Xuất bảng tổng hợp thi đua toàn trường từ TongHop_ThiDua. Cần tổng hợp tháng trước khi xuất.")

    try:
        filename, file_bytes, row_count = build_monthly_excel_export(normalized_month)
    except ValueError as exc:
        st.info(str(exc))
        return

    st.metric("Số dòng sẽ xuất", row_count)
    st.download_button(
        "Tải Excel tổng hợp tháng",
        data=file_bytes,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=False,
    )


def _render_system_admin_panel(compact: bool = False) -> None:
    """Render BGH-only system administration tools near the top-right area."""
    if not compact:
        st.divider()
        st.markdown(
            '<div style="color:#ff4b4b; font-weight:800; font-size:1.5rem; margin-bottom:0.35rem;">Quản trị hệ thống</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Các thao tác dưới đây chỉ phục vụ vận hành hệ thống. "
            "Không dùng để chấm điểm hay xử lý phiếu thi đua."
        )
    else:
        st.markdown(
            '<div style="color:#ff4b4b; font-weight:800; font-size:1.05rem; margin-bottom:0.15rem;">Quản trị hệ thống</div>',
            unsafe_allow_html=True,
        )
        st.caption("Cấu hình vận hành và tài khoản.")

    with st.expander("Cấu hình thời hạn tự chấm", expanded=False):
        _render_scoring_deadline_panel()

    with st.expander("Tài khoản và mật khẩu", expanded=False):
        _render_account_password_panel()


def _render_scoring_deadline_panel() -> None:
    """Render BGH system configuration for teacher self-scoring deadline."""
    st.markdown("**Cấu hình thời hạn tự chấm**")
    st.caption(
        "BGH chọn ngày cuối cùng giáo viên được tự tạo và tự chấm phiếu trong tháng. "
        "Nếu chưa cấu hình, hệ thống mặc định hết ngày 5."
    )

    deadline_status = st.session_state.pop("m03_deadline_config_status", "")
    if deadline_status:
        st.success(deadline_status)

    try:
        current_deadline = get_teacher_scoring_deadline_day()
    except ValueError as exc:
        st.error(str(exc))
        return

    col_day, col_button, _ = st.columns([1.2, 1.5, 4])
    with col_day:
        selected_day = st.number_input(
            "Ngày cuối tự chấm",
            min_value=1,
            max_value=31,
            value=int(current_deadline),
            step=1,
            help="Ví dụ 5 nghĩa là giáo viên được tự chấm từ ngày 1 đến hết ngày 5.",
        )
    with col_button:
        st.write("")
        if st.button("Lưu thời hạn tự chấm", type="primary", use_container_width=True):
            try:
                actor = _resolve_actor_code(_get_logged_in_user() or {})
                set_teacher_scoring_deadline_day(int(selected_day), actor)
                st.session_state["m03_deadline_config_status"] = (
                    f"Đã cập nhật thời hạn tự chấm đến hết ngày {int(selected_day)} mỗi tháng."
                )
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))


def _render_account_password_panel() -> None:
    """Render safe BGH account password initialization tool."""
    st.markdown("**Khởi tạo mật khẩu**")
    st.caption(
        "Dùng sau khi bổ sung giáo viên trong DM_GiaoVien. "
        "Chỉ tạo MatKhauHash cho tài khoản đang hoạt động và chưa có mật khẩu; không ghi đè tài khoản đã có mật khẩu. "
        "Tài khoản đăng nhập chỉ dùng GV hoặc BGH. Giáo viên dùng mật khẩu là Mã GV; BGH dùng mật khẩu riêng."
    )

    account_status = st.session_state.pop("m03_account_password_status", "")
    if account_status:
        st.success(account_status)

    col_missing, _ = st.columns([1.6, 4])
    with col_missing:
        if st.button("Khởi tạo mật khẩu cho tài khoản mới", type="primary", use_container_width=True):
            try:
                actor = _resolve_actor_code(_get_logged_in_user() or {})
                result = normalize_missing_password_hashes(actor)
                st.session_state["m03_account_password_status"] = (
                    f"Đã khởi tạo hash mật khẩu cho {result.get('updated_count', 0)} tài khoản mới. "
                    f"Bỏ qua tài khoản đã có hash: {result.get('skipped_has_hash', 0)}."
                )
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))

def _render_selected_phieu(phieu: dict, teacher_map: dict[str, dict]) -> None:
    id_phieu = str(phieu.get("ID", "")).strip()
    ma_gv = str(phieu.get("MaGV", "")).strip()
    teacher = teacher_map.get(ma_gv, {})

    details = get_chi_tiet_phieu(id_phieu)
    criteria = get_all_criteria()
    official_total = _calculate_total_score(details)

    st.markdown('<div class="ev-bgh-detail-title">Chi tiết phiếu</div>', unsafe_allow_html=True)
    info_cols = st.columns([1.6, 1.0, 1.0, 2.4, 1.5, 0.8, 0.9], gap="small")
    values = [
        ("Giáo viên", teacher.get("ho_ten") or ma_gv or "Không rõ"),
        ("Trạng thái", _status_text(phieu.get("TrangThai"))),
        ("Tổng điểm", _format_number(official_total)),
        ("ID phiếu", id_phieu),
        ("Ngày nộp", phieu.get("NgayNop", "") or "Chưa nộp"),
        ("Lần nộp", phieu.get("LanNop", "") or 0),
        ("Lần mở khóa", phieu.get("LanMoKhoa", "") or 0),
    ]
    for col, (label, value) in zip(info_cols, values):
        with col:
            st.markdown(
                f'<div class="ev-bgh-info-label">{_html_escape(label)}</div>'
                f'<div class="ev-bgh-info-value">{_html_escape(value)}</div>',
                unsafe_allow_html=True,
            )

    if not details:
        st.warning("Không tìm thấy CT_ThiDua của phiếu này.")
        return

    readonly = _safe_int(phieu.get("TrangThai"), default=0) == 5 or _parse_bool(phieu.get("KhoaBGH"))
    save_status = st.session_state.pop("m03_bgh_save_status", "")
    if save_status:
        st.success(save_status)

    changed_rows, current_total, action, input_errors = render_score_form(
        criteria,
        details,
        readonly=readonly,
        mode=FORM_MODE_BGH,
    )

    if readonly:
        st.info("Phiếu đã chốt hoặc đã khóa BGH. Ban Giám hiệu chỉ được xem, không được chỉnh sửa.")
        return

    if action == FORM_ACTION_SAVE:
        if input_errors:
            st.error("Chưa thể lưu vì còn điểm BGH vượt thang điểm đánh giá.")
            return
        if not changed_rows:
            st.warning("Không có dòng chi tiết để lưu. Vui lòng kiểm tra CT_ThiDua của phiếu.")
            return
        try:
            actor = _resolve_actor_code(_get_logged_in_user() or {})
            total = save_bgh_scores(id_phieu, changed_rows, actor)
            st.session_state["m03_bgh_save_status"] = f"Đã lưu điểm BGH. Tổng điểm hiện hành: {_format_number(total)}"
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))


def _html_escape(value: object) -> str:
    text = str(value or "")
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _resolve_actor_code(user: dict) -> str:
    return str(
        user.get("ma_gv")
        or user.get("Mã GV")
        or user.get("ten_dang_nhap")
        or user.get("Tên đăng nhập")
        or "BGH"
    ).strip()


def _get_phieu_list_by_month(thang: str) -> list[dict]:
    target_month = _normalize_month_key(thang)
    selected_by_id: dict[str, dict] = {}
    for record in read_sheet_records(SHEET_TH):
        phieu = _canonicalize_th_record(record)
        if _normalize_month_key(phieu.get("Thang")) != target_month:
            continue
        id_phieu = str(phieu.get("ID", "")).strip()
        expected_id = _build_expected_phieu_id(phieu, target_month)
        if expected_id and id_phieu != expected_id:
            id_phieu = expected_id
            phieu["ID"] = id_phieu
        if not id_phieu:
            continue
        current = selected_by_id.get(id_phieu)
        if current is None or _phieu_priority(phieu) >= _phieu_priority(current):
            selected_by_id[id_phieu] = phieu
    return sorted(selected_by_id.values(), key=lambda item: str(item.get("MaGV", "")))


def _phieu_priority(phieu: dict) -> tuple[int, str, str]:
    has_total = int(_safe_float(phieu.get("TongDiem")) != 0)
    return (has_total, str(phieu.get("NgayNop", "")).strip(), str(phieu.get("NgayCapNhat", "")).strip())


def _get_teacher_map() -> dict[str, dict]:
    teachers = get_all_teachers()
    return {str(teacher.get("ma_gv", "")).strip(): teacher for teacher in teachers if str(teacher.get("ma_gv", "")).strip()}


def _build_list_row(phieu: dict, teacher_map: dict[str, dict]) -> dict[str, Any]:
    ma_gv = str(phieu.get("MaGV", "")).strip()
    teacher = teacher_map.get(ma_gv, {})
    return {
        "Mã GV": ma_gv,
        "Họ và tên": teacher.get("ho_ten", ""),
        "Tổ chuyên môn": teacher.get("to_chuyen_mon", ""),
        "Trạng thái": _status_text(phieu.get("TrangThai")),
        "Tổng điểm": phieu.get("TongDiem", ""),
        "Ngày nộp": phieu.get("NgayNop", ""),
        "Lần nộp": phieu.get("LanNop", ""),
        "ID phiếu": phieu.get("ID", ""),
    }


def _format_select_label(phieu: dict, teacher_map: dict[str, dict]) -> str:
    ma_gv = str(phieu.get("MaGV", "")).strip()
    teacher_name = teacher_map.get(ma_gv, {}).get("ho_ten", "")
    total = phieu.get("TongDiem", "") or "0"
    status = _status_text(phieu.get("TrangThai"))
    if teacher_name:
        return f"{ma_gv} - {teacher_name} | {status} | {total} điểm"
    return f"{ma_gv} | {status} | {total} điểm"


def _get_logged_in_user() -> dict | None:
    for key in ("teacher", "user", "current_user", "auth_user"):
        value = st.session_state.get(key)
        if isinstance(value, dict):
            return value
    return None


def _is_bgh_user(user: dict) -> bool:
    role = _normalize_key(user.get("vai_tro") or user.get("Vai trò") or user.get("role") or "")
    return role in {"bgh", "ban_giam_hieu", "admin", "quan_tri", "quan_tri_vien"}


def _canonicalize_th_record(record: dict) -> dict:
    canonical = {name: _get_text(record, *aliases) for name, aliases in TH_ALIASES.items()}

    status = _safe_int(canonical.get("TrangThai"), default=0)
    locked = _parse_bool(canonical.get("KhoaGV"))
    ngay_nop = str(canonical.get("NgayNop", "")).strip()
    if status not in {3, 5} and (locked or ngay_nop):
        canonical["TrangThai"] = "3"

    return canonical


def _canonicalize_ct_record(record: dict) -> dict:
    return {canonical: _get_text(record, *aliases) for canonical, aliases in CT_ALIASES.items()}


def _status_text(value: object) -> str:
    status = _safe_int(value, default=0)
    return STATUS_TEXT.get(status, str(value or ""))


def _calculate_total_score(details: list[dict]) -> float:
    total = 0.0
    seen: set[str] = set()
    for raw_detail in details:
        detail = _canonicalize_ct_record(raw_detail)
        row_id = str(detail.get("ID") or f"{detail.get('IDPhieu', '')}_{detail.get('MaTC', '')}").strip()
        if row_id and row_id in seen:
            continue
        if row_id:
            seen.add(row_id)
        total += _official_score(detail)
    return total


def _official_score(detail: dict) -> float:
    diem_bgh = str(detail.get("DiemBGH", "")).strip()
    if diem_bgh:
        return _safe_float(diem_bgh)
    return _safe_float(detail.get("DiemGV"))


def _get_text(record: dict, *keys: str) -> str:
    normalized = {_normalize_key(key): value for key, value in record.items()}
    for key in keys:
        value = record.get(key)
        if value is not None and str(value).strip() != "":
            return str(value).strip()
        normalized_value = normalized.get(_normalize_key(key))
        if normalized_value is not None and str(normalized_value).strip() != "":
            return str(normalized_value).strip()
    return ""



def _build_expected_phieu_id(phieu: dict, normalized_month: str) -> str:
    nam_hoc = str(phieu.get("NamHoc", "")).strip()
    ma_gv = str(phieu.get("MaGV", "")).strip()
    if not nam_hoc or not normalized_month or not ma_gv:
        return ""
    safe_thang = str(normalized_month).replace("/", "")
    return f"{nam_hoc}_{safe_thang}_{ma_gv}"


def _normalize_month_key(value: object) -> str:
    text = str(value or "").strip().replace("'", "")
    if not text:
        return ""

    parts = text.split("/")
    if len(parts) == 2:
        month, year = parts[0].strip(), parts[1].strip()
        try:
            return f"{int(float(month)):02d}/{int(float(year)):04d}"
        except ValueError:
            return text

    compact = "".join(ch for ch in text if ch.isdigit())
    if len(compact) == 6:
        return f"{compact[:2]}/{compact[2:]}"
    return text


def _normalize_key(value: object) -> str:
    text = str(value).strip().lower()
    replacements = {
        "ã": "a", "à": "a", "á": "a", "ả": "a", "ạ": "a", "ă": "a", "ằ": "a", "ắ": "a", "ẳ": "a", "ặ": "a", "â": "a", "ầ": "a", "ấ": "a", "ẩ": "a", "ậ": "a",
        "đ": "d", "è": "e", "é": "e", "ẻ": "e", "ẹ": "e", "ê": "e", "ề": "e", "ế": "e", "ể": "e", "ệ": "e",
        "ì": "i", "í": "i", "ỉ": "i", "ị": "i", "ò": "o", "ó": "o", "ỏ": "o", "ọ": "o", "ô": "o", "ồ": "o", "ố": "o", "ổ": "o", "ộ": "o", "ơ": "o", "ờ": "o", "ớ": "o", "ở": "o", "ợ": "o",
        "ù": "u", "ú": "u", "ủ": "u", "ụ": "u", "ư": "u", "ừ": "u", "ứ": "u", "ử": "u", "ự": "u", "ỳ": "y", "ý": "y", "ỷ": "y", "ỵ": "y",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return "_".join(text.replace("(", " ").replace(")", " ").replace("/", " ").split())


def _safe_int(value: object, default: int = 0) -> int:
    text = str(value or "").strip()
    if not text:
        return default
    try:
        return int(float(text.replace(",", ".")))
    except ValueError:
        return default


def _safe_float(value: object) -> float:
    text = str(value or "").strip()
    if not text:
        return 0.0
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return 0.0


def _format_number(value: object) -> str:
    number = _safe_float(value)
    if number.is_integer():
        return str(int(number))
    return f"{number:.2f}".rstrip("0").rstrip(".")


def _parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y", "x", "co", "có"}
