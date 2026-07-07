"""Streamlit scoring form component generated from DM_TieuChi."""

from __future__ import annotations

from typing import Any

import streamlit as st
import streamlit.components.v1 as components


FORM_CSS = """
<style>
.ev-m02-note {
    font-size: 0.9rem;
    color: rgba(80, 80, 80, 0.78);
    margin: 0.25rem 0 0.75rem 0;
}
.ev-score-totalbar {
    display: grid;
    grid-template-columns: 5% 53% 12% 10% 20%;
    align-items: center;
    margin: 0.25rem 0 0.5rem 0;
}
.ev-score-totalbox {
    grid-column: 4 / 5;
    border: 1px solid #222;
    background: #fff2cc;
    color: #111;
    font-weight: 700;
    text-align: center;
    padding: 0.55rem 0.35rem;
}
.ev-score-totalbox small {
    display: block;
    font-weight: 600;
    font-size: 0.75rem;
}
.ev-score-header {
    position: -webkit-sticky;
    position: sticky;
    top: 0;
    z-index: 1000;
    display: grid;
    grid-template-columns: 5% 53% 12% 10% 20%;
    background: #d8e4bc;
    border-top: 1px solid #222;
    border-left: 1px solid #222;
    font-weight: 700;
    color: #111;
}
.ev-score-header > div,
.ev-cell {
    border-right: 1px solid #222;
    border-bottom: 1px solid #222;
    padding: 0.48rem 0.45rem;
    min-height: 2.35rem;
    line-height: 1.35;
    white-space: normal;
    overflow-wrap: anywhere;
    word-break: normal;
    color: #111;
}
.ev-score-header > div {
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}
.ev-score-header small {
    font-size: 0.72rem;
    font-weight: 500;
    line-height: 1.2;
}
.ev-live-total-wrap {
    display: flex;
    justify-content: flex-end;
    margin: 0.8rem 0 0.6rem 0;
}
.ev-live-total-box {
    min-width: 10rem;
    border: 1px solid #222;
    background: #fff2cc;
    text-align: center;
    padding: 0.55rem 0.8rem;
    font-weight: 700;
    color: #111;
}
.ev-live-total-box strong {
    display: block;
    font-size: 1.45rem;
    line-height: 1.2;
}
.ev-cell-center { text-align: center; }
.ev-group-cell { background: #ffff00; font-weight: 700; }
.ev-section-cell { background: #d8e4bc; font-weight: 700; }
.ev-item-odd { background: #ffffff; }
.ev-item-even { background: #eaf2dd; }
.ev-placeholder { color: #9a3412; font-style: italic; }
.ev-bgh-note {
    font-size: 0.82rem;
    color: rgba(80, 80, 80, 0.78);
    margin: 0.1rem 0 0.45rem 0;
}
.ev-score-warning {
    color: #b91c1c;
    font-weight: 600;
    margin: 0.25rem 0 0.5rem 0;
}
div[data-testid="stNumberInput"] input {
    min-height: 2.05rem;
    text-align: center;
}
/* Không ép overflow toàn trang; bảng GV dùng vùng cuộn Streamlit thuần. */
div[data-testid="stTextInput"] input {
    min-height: 2.05rem;
}

.ev-action-header-table {
    display: grid;
    grid-template-columns: 5% 53% 12% 10% 20%;
    background: #d8e4bc;
    border-top: 1px solid #222;
    border-left: 1px solid #222;
    margin-top: 0.75rem;
    font-weight: 700;
    color: #111;
}
.ev-action-header-table > div {
    border-right: 1px solid #222;
    border-bottom: 1px solid #222;
    padding: 0.75rem 0.45rem;
    min-height: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    flex-direction: column;
    line-height: 1.25;
}
.ev-action-header-table small {
    font-size: 0.72rem;
    font-weight: 500;
    line-height: 1.2;
}
.ev-action-block-note {
    font-size: 0.78rem;
    color: rgba(80, 80, 80, 0.72);
    margin-top: 0.35rem;
}
.ev-action-confirm-note {
    margin: 0.35rem 0 0.25rem 0;
    padding: 0.42rem 0.55rem;
    border: 1px solid #f59e0b;
    background: #fff7ed;
    color: #92400e;
    border-radius: 0.35rem;
    font-size: 0.82rem;
    line-height: 1.35;
}
.ev-action-warning-box {
    margin: 0.35rem 0 0.35rem 0;
    padding: 0.45rem 0.6rem;
    border: 1px solid #fca5a5;
    background: #fef2f2;
    color: #991b1b;
    border-radius: 0.35rem;
    font-size: 0.8rem;
    line-height: 1.35;
}
.ev-action-warning-item {
    margin-top: 0.16rem;
}

.ev-score-scroll-box {
    max-height: 56vh;
    overflow-y: auto;
    overflow-x: hidden;
    border: 1px solid rgba(128, 128, 128, 0.32);
    border-radius: 0.45rem;
    padding: 0.45rem 0.55rem;
    margin-top: 0.45rem;
    background: #ffffff;
}
.ev-score-scroll-box::-webkit-scrollbar {
    width: 0.65rem;
}
.ev-score-scroll-box::-webkit-scrollbar-thumb {
    background: rgba(120, 120, 120, 0.55);
    border-radius: 999px;
}
.ev-score-scroll-anchor {
    height: 0;
    margin: 0;
    padding: 0;
    overflow: hidden;
}

@media (max-width: 900px) {
    .ev-score-header, .ev-score-totalbar { grid-template-columns: 7% 45% 14% 14% 20%; font-size: 0.82rem; }
    .ev-cell { font-size: 0.82rem; }
}
</style>
"""


FORM_ACTION_NONE = "none"
FORM_ACTION_SAVE = "save"
FORM_ACTION_SUBMIT = "submit"
FORM_ACTION_CONFIRM_SUBMIT = "confirm_submit"
FORM_ACTION_CANCEL_SUBMIT = "cancel_submit"
FORM_MODE_TEACHER = "teacher"
FORM_MODE_BGH = "bgh"
MAX_TOTAL_SCORE = 100.0



def render_score_form(
    criteria: list[dict],
    details: list[dict],
    readonly: bool = False,
    mode: str = FORM_MODE_TEACHER,
) -> tuple[list[dict], float, str, list[str]]:
    """Render the official score form for Teacher or BGH.

    Teacher mode preserves the M02 behavior: teachers edit DiemGV/GhiChuGV.
    BGH mode reuses the same component style while BGH edits DiemBGH/GhiChuBGH.
    """
    normalized_mode = str(mode or FORM_MODE_TEACHER).strip().lower()
    if normalized_mode == FORM_MODE_BGH:
        return _render_bgh_score_form(criteria, details, readonly=readonly)
    return _render_teacher_score_form(criteria, details, readonly=readonly)

def _render_teacher_score_form(
    criteria: list[dict],
    details: list[dict],
    readonly: bool = False,
) -> tuple[list[dict], float, str, list[str]]:
    """Render Excel-like scoring form for teacher.

    Khối thao tác và tiêu đề bảng được tách khỏi nội dung phiếu điểm.
    Phần này chỉ thay đổi giao diện, không thay đổi nghiệp vụ lưu/nộp.
    """
    st.markdown(FORM_CSS, unsafe_allow_html=True)
    normalized_criteria = [_normalize_criterion(row) for row in criteria]
    normalized_details = [_normalize_detail(row) for row in details]
    detail_by_ma_tc = {str(row.get("MaTC", "")).strip(): row for row in normalized_details if str(row.get("MaTC", "")).strip()}

    prepared_rows = _prepare_rows(normalized_criteria, detail_by_ma_tc)
    parent_totals = _build_parent_totals(prepared_rows)

    changed_rows: list[dict] = []
    errors: list[str] = []
    action = FORM_ACTION_NONE

    # KHỐI 1: thao tác + tiêu đề cột. Không render nội dung điểm ở đây.
    with st.container(border=True):
        is_confirming_submit = bool(st.session_state.get("m02_confirm_submit"))
        if is_confirming_submit:
            save_col, submit_col, confirm_col, cancel_col, _ = st.columns([1.0, 1.15, 0.95, 0.65, 1.0])
        else:
            save_col, submit_col, _ = st.columns([1.1, 1.3, 1.2])
            confirm_col = cancel_col = None

        save_is_active = st.session_state.get("m02_last_action") == FORM_ACTION_SAVE
        save_button_type = "primary" if save_is_active else "secondary"
        submit_button_type = "secondary" if save_is_active else "primary"

        with save_col:
            save_clicked = st.button("Lưu", type=save_button_type, use_container_width=True, disabled=readonly, key="m02_save_button_top")
        with submit_col:
            submit_clicked = st.button("Xác nhận nộp phiếu", type=submit_button_type, use_container_width=True, disabled=readonly, key="m02_submit_button_top")

        confirm_clicked = False
        cancel_clicked = False
        if is_confirming_submit and confirm_col is not None and cancel_col is not None:
            with confirm_col:
                confirm_clicked = st.button("Đồng ý nộp", type="primary", use_container_width=True, disabled=readonly, key="m02_confirm_submit_button_top")
            with cancel_col:
                cancel_clicked = st.button("Hủy", use_container_width=True, disabled=readonly, key="m02_cancel_submit_button_top")
            st.markdown(
                '<div class="ev-action-confirm-note"><b>Xác nhận nộp phiếu:</b> Sau khi nộp, phiếu sẽ khóa phần chỉnh sửa của giáo viên.</div>',
                unsafe_allow_html=True,
            )

        warning_messages = st.session_state.get("m02_submit_warning_messages") or []
        if warning_messages:
            st.markdown('<div class="ev-action-warning-box"><b>Tiêu chí cần kiểm tra/ghi chú:</b>', unsafe_allow_html=True)
            for message in warning_messages:
                st.markdown(f'<div class="ev-action-warning-item">- {_html_escape(message)}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if save_clicked:
            st.session_state["m02_last_action"] = FORM_ACTION_SAVE
            action = FORM_ACTION_SAVE
        elif submit_clicked:
            st.session_state["m02_last_action"] = FORM_ACTION_SUBMIT
            action = FORM_ACTION_SUBMIT
        elif confirm_clicked:
            action = FORM_ACTION_CONFIRM_SUBMIT
        elif cancel_clicked:
            action = FORM_ACTION_CANCEL_SUBMIT

        _render_teacher_fixed_header()

    # KHỐI 2: nội dung phiếu điểm trong vùng cuộn Streamlit thuần.
    # Không dùng JavaScript/DOM để tránh treo trắng khi Lưu hoặc Nộp.
    total = 0.0
    group_index = 0
    item_index = 0

    with st.container(height=520, border=True):
        for row in prepared_rows:
            loai = row["loai"]
            if loai == "GROUP":
                group_index += 1
                item_index = 0
                totals = parent_totals.get(row["ma_tc"], {})
                _render_static_row(
                    f"{_to_roman(group_index)}.",
                    row["ten_tc"],
                    _format_score(_to_float(totals.get("max", 0))),
                    "group",
                    _format_score(_to_float(totals.get("teacher", 0))),
                )
                continue

            if loai == "SECTION":
                totals = parent_totals.get(row["ma_tc"], {})
                _render_static_row(
                    row["display_code"],
                    row["ten_tc"],
                    _format_score(_to_float(totals.get("max", 0))),
                    "section",
                    _format_score(_to_float(totals.get("teacher", 0))),
                )
                continue

            if loai != "ITEM":
                continue

            item_index += 1
            display_tt = row["display_code"] or (f"{group_index}.{item_index}" if group_index else str(item_index))
            row_kind = "item-even" if item_index % 2 == 0 else "item-odd"
            diem_gv, ghi_chu_gv = _render_item_row(
                display_tt=display_tt,
                ten_tc=row["ten_tc"],
                diem_mac_dinh=row["diem_mac_dinh"],
                current_diem_gv=row["current_diem_gv"],
                current_ghi_chu_gv=row["current_ghi_chu_gv"],
                key_base=row["key_base"],
                readonly=readonly,
                row_kind=row_kind,
            )

            if diem_gv > row["diem_mac_dinh"]:
                errors.append(
                    f"Tiêu chí {display_tt}: điểm tự chấm {diem_gv:g} lớn hơn thang điểm {row['diem_mac_dinh']:g}."
                )

            total += _resolve_official_score_for_display(row, float(diem_gv))

            if not readonly:
                changed_rows.append(
                    {
                        "ID": row["detail"].get("ID", ""),
                        "IDPhieu": row["detail"].get("IDPhieu", ""),
                        "MaTC": row["ma_tc"],
                        "DiemMacDinh": row["diem_mac_dinh"],
                        "DiemGV": float(diem_gv),
                        "GhiChuGV": str(ghi_chu_gv).strip(),
                    }
                )

            if row["diem_bgh"]:
                st.markdown(
                    f'<div class="ev-bgh-note">BGH điều chỉnh: <b>{_html_escape(row["diem_bgh"])}</b>. '
                    f'Ghi chú BGH: {_html_escape(row["ghi_chu_bgh"] or "Không có")}</div>',
                    unsafe_allow_html=True,
                )


    if errors:
        for error in errors:
            st.markdown(f'<div class="ev-score-warning">{_html_escape(error)}</div>', unsafe_allow_html=True)

    total = _cap_total(total)
    _render_live_total(total)

    return changed_rows, total, action, errors


def _render_bgh_score_form(
    criteria: list[dict],
    details: list[dict],
    readonly: bool = False,
) -> tuple[list[dict], float, str, list[str]]:
    """Render the BGH scoring form using the same stable component pattern as M02."""
    st.markdown(FORM_CSS, unsafe_allow_html=True)
    normalized_criteria = [_normalize_criterion(row) for row in criteria]
    normalized_details = [_normalize_detail(row) for row in details]
    detail_by_ma_tc = {str(row.get("MaTC", "")).strip(): row for row in normalized_details if str(row.get("MaTC", "")).strip()}

    prepared_rows = _prepare_rows(normalized_criteria, detail_by_ma_tc)
    parent_totals = _build_parent_totals(prepared_rows)
    _render_bgh_sticky_header()

    changed_rows: list[dict] = []
    errors: list[str] = []
    action = FORM_ACTION_NONE

    with st.form("m03_bgh_score_form", clear_on_submit=False):
        total = 0.0
        group_index = 0
        item_index = 0

        # Bảng 2: chỉ chứa các dòng tiêu chí và có vùng cuộn riêng.
        # Header 7 cột đã được render ở trên bằng _render_bgh_sticky_header().
        # Không thay đổi logic nhập/lưu điểm BGH.
        with st.container(height=430, border=True):
            for row in prepared_rows:
                loai = row["loai"]
                if loai == "GROUP":
                    group_index += 1
                    item_index = 0
                    totals = parent_totals.get(row["ma_tc"], {})
                    _render_bgh_static_row(
                        f"{_to_roman(group_index)}.",
                        row["ten_tc"],
                        _format_score(_to_float(totals.get("max", 0))),
                        _format_score(_to_float(totals.get("teacher", 0))),
                        _format_score(_to_float(totals.get("teacher", 0))),
                        "group",
                    )
                    continue

                if loai == "SECTION":
                    totals = parent_totals.get(row["ma_tc"], {})
                    _render_bgh_static_row(
                        row["display_code"],
                        row["ten_tc"],
                        _format_score(_to_float(totals.get("max", 0))),
                        _format_score(_to_float(totals.get("teacher", 0))),
                        _format_score(_to_float(totals.get("teacher", 0))),
                        "section",
                    )
                    continue

                if loai != "ITEM":
                    continue

                item_index += 1
                display_tt = row["display_code"] or (f"{group_index}.{item_index}" if group_index else str(item_index))
                row_kind = "item-even" if item_index % 2 == 0 else "item-odd"
                diem_bgh, ghi_chu_bgh = _render_bgh_item_row(
                    display_tt=display_tt,
                    ten_tc=row["ten_tc"],
                    diem_mac_dinh=row["diem_mac_dinh"],
                    current_diem_gv=row["current_diem_gv"],
                    current_ghi_chu_gv=row["current_ghi_chu_gv"],
                    current_diem_bgh=row["diem_bgh"],
                    current_ghi_chu_bgh=row["ghi_chu_bgh"],
                    key_base=row["key_base"],
                    readonly=readonly,
                    row_kind=row_kind,
                )

                if diem_bgh > row["diem_mac_dinh"]:
                    errors.append(
                        f"Tiêu chí {display_tt}: điểm BGH {diem_bgh:g} lớn hơn thang điểm {row['diem_mac_dinh']:g}."
                    )

                total += float(diem_bgh)

                if not readonly:
                    changed_rows.append(
                        {
                            "ID": row["detail"].get("ID", ""),
                            "IDPhieu": row["detail"].get("IDPhieu", ""),
                            "MaTC": row["ma_tc"],
                            "DiemGV": float(row["current_diem_gv"]),
                            "DiemBGH": float(diem_bgh),
                            "GhiChuBGH": str(ghi_chu_bgh).strip(),
                        }
                    )

        if errors:
            for error in errors:
                st.markdown(f'<div class="ev-score-warning">{_html_escape(error)}</div>', unsafe_allow_html=True)

        total = _cap_total(total)

        # BGH chỉ dùng một tổng điểm chính thức ở đầu phiếu.
        # Không hiển thị thêm tổng điểm tạm ở cuối form để tránh hiểu nhầm.
        st.markdown('<div id="evus-bgh-actions-anchor"></div>', unsafe_allow_html=True)
        save_col, _ = st.columns([1.2, 3.8])
        with save_col:
            save_clicked = st.form_submit_button("Lưu điểm BGH", type="primary", use_container_width=True, disabled=readonly)

        if save_clicked:
            action = FORM_ACTION_SAVE

    return changed_rows, total, action, errors


def _render_bgh_sticky_header() -> None:
    st.markdown(
        """
        <div class="ev-score-header" style="grid-template-columns: 5% 43% 10% 10% 11% 10% 11%;">
            <div>TT</div>
            <div>Tiêu chí xét thi đua</div>
            <div>Thang điểm</div>
            <div>Điểm GV</div>
            <div>Ghi chú GV</div>
            <div>Điểm BGH</div>
            <div>Ghi chú BGH</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_bgh_static_row(tt: str, content: str, default_score: str, teacher_score: str, bgh_score: str, row_kind: str) -> None:
    css = "ev-group-cell" if row_kind == "group" else "ev-section-cell"
    c1, c2, c3, c4, c5, c6, c7 = st.columns([5, 43, 10, 10, 11, 10, 11], gap="small")
    safe_content = _safe_content(content)
    with c1:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_html_escape(tt)}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="ev-cell {css}">{safe_content}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_html_escape(default_score)}</div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_html_escape(teacher_score)}</div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="ev-cell {css}">&nbsp;</div>', unsafe_allow_html=True)
    with c6:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_html_escape(bgh_score)}</div>', unsafe_allow_html=True)
    with c7:
        st.markdown(f'<div class="ev-cell {css}">&nbsp;</div>', unsafe_allow_html=True)


def _render_bgh_item_row(
    display_tt: str,
    ten_tc: str,
    diem_mac_dinh: float,
    current_diem_gv: float,
    current_ghi_chu_gv: str,
    current_diem_bgh: str,
    current_ghi_chu_bgh: str,
    key_base: str,
    readonly: bool,
    row_kind: str,
) -> tuple[float, str]:
    css = "ev-item-even" if row_kind == "item-even" else "ev-item-odd"
    c1, c2, c3, c4, c5, c6, c7 = st.columns([5, 43, 10, 10, 11, 10, 11], gap="small")
    initial_bgh = _to_float(current_diem_bgh) if str(current_diem_bgh).strip() else float(current_diem_gv)
    max_value = max(float(diem_mac_dinh), initial_bgh, 0.0)
    with c1:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_html_escape(display_tt)}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="ev-cell {css}">{_safe_content(ten_tc)}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_format_score(diem_mac_dinh)}</div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_format_score(current_diem_gv)}</div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="ev-cell {css}">{_html_escape(current_ghi_chu_gv or "")}</div>', unsafe_allow_html=True)
    with c6:
        diem_bgh = st.number_input(
            "Điểm BGH",
            min_value=0.0,
            max_value=max_value,
            value=float(initial_bgh),
            step=0.5,
            key=f"diem_bgh_{key_base}",
            disabled=readonly,
            label_visibility="collapsed",
        )
    with c7:
        ghi_chu_bgh = st.text_input(
            "Ghi chú BGH",
            value=current_ghi_chu_bgh,
            key=f"ghi_chu_bgh_{key_base}",
            disabled=readonly,
            label_visibility="collapsed",
        )
    return float(diem_bgh), str(ghi_chu_bgh)

def _scroll_to_bgh_actions() -> None:
    """Cuộn nhẹ đến nút lưu BGH khi khu vực thao tác nằm dưới cuối bảng."""
    components.html(
        """
        <script>
        (function() {
          const root = window.parent.document;
          const anchor = root.getElementById('evus-bgh-actions-anchor');
          if (!anchor) return;
          setTimeout(function() {
            anchor.scrollIntoView({block: 'center', behavior: 'smooth'});
          }, 80);
        })();
        </script>
        """,
        height=0,
    )


def _cap_total(total: float) -> float:
    return min(float(total or 0), MAX_TOTAL_SCORE)


def _render_live_total(total: float, label: str = "Tổng điểm hiện hành") -> None:
    html = f"""
        <div class="ev-live-total-wrap">
            <div class="ev-live-total-box">
                <div>{_html_escape(label)}</div>
                <strong id="m02-current-total">{_format_score(total)}</strong>
            </div>
        </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def _attach_live_total_and_sticky_header() -> None:
    """Attach limited browser helpers.

    Không dùng MutationObserver vì có thể làm Chrome báo trang không phản hồi
    khi Streamlit dựng lại nhiều widget trong form.
    """
    components.html(
        """
        <script>
        (function() {
          const root = window.parent.document;

          const parseNumber = (value) => {
            const normalized = String(value || '').replace(',', '.').trim();
            const parsed = Number.parseFloat(normalized);
            return Number.isFinite(parsed) ? parsed : 0;
          };

          const formatScore = (value) => {
            const capped = Math.min(value, 100);
            const rounded = Math.round(capped * 100) / 100;
            if (Math.abs(rounded - Math.round(rounded)) < 0.000001) return String(Math.round(rounded));
            return String(rounded).replace('.', ',');
          };

          const scoreInputs = () => Array.from(root.querySelectorAll('input[type="number"]'))
            .filter((input) => !input.disabled && input.offsetParent !== null);

          const updateTotal = () => {
            const totalEl = root.getElementById('m02-current-total');
            if (!totalEl) return;
            let total = 0;
            scoreInputs().forEach((input) => { total += parseNumber(input.value); });
            totalEl.textContent = formatScore(total);
          };

          const attach = () => {
            root.querySelectorAll('input[type="number"], input[type="text"]').forEach((input) => {
              if (input.dataset.evusSafeAttached === '1') return;
              input.dataset.evusSafeAttached = '1';
              input.addEventListener('focus', function() { this.select(); });
              input.addEventListener('mouseup', function(event) { event.preventDefault(); });
              input.addEventListener('input', updateTotal);
              input.addEventListener('change', updateTotal);
              input.addEventListener('keyup', updateTotal);
              input.addEventListener('click', updateTotal);
            });
            updateTotal();
          };

          attach();
          let tries = 0;
          const timer = root.defaultView.setInterval(() => {
            tries += 1;
            attach();
            if (tries >= 20) root.defaultView.clearInterval(timer);
          }, 250);
        })();
        </script>
        """,
        height=0,
        width=0,
    )

def _attach_input_helpers() -> None:
    """Input helpers are attached once by _attach_live_total_and_sticky_header."""
    return


def _render_total_bar(total: float) -> None:
    st.markdown(
        f"""
        <div class="ev-score-totalbar">
            <div class="ev-score-totalbox"><small>Tổng điểm hiện hành</small>{_format_score(total)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def _render_teacher_fixed_header() -> None:
    """Render a separate 1-row, 5-column header for the teacher action block.

    This header is not reused from the score table body. It is intentionally
    rendered as a standalone HTML grid so the action block can stay independent
    from the scoring rows.
    """
    st.markdown(
        """
        <div class="ev-action-header-table">
            <div>TT</div>
            <div>Tiêu chí xét thi đua</div>
            <div>Thang điểm<br>đánh giá<br>(100)</div>
            <div>Tự<br>chấm</div>
            <div>Ghi chú<br><small>Dùng khi tự chấm khác điểm mặc định</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _render_sticky_header() -> None:
    st.markdown(
        """
        <div class="ev-score-header">
            <div>TT</div>
            <div>Tiêu chí xét thi đua</div>
            <div>Thang điểm<br>đánh giá<br>(100)</div>
            <div>Tự<br>chấm</div>
            <div>Ghi chú<br><small>Dùng khi tự chấm khác điểm mặc định</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_static_row(tt: str, content: str, default_score: str, row_kind: str, teacher_score: str = "") -> None:
    css = "ev-group-cell" if row_kind == "group" else "ev-section-cell"
    c1, c2, c3, c4, c5 = st.columns([5, 53, 12, 10, 20], gap="small")
    safe_content = _safe_content(content)
    with c1:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_html_escape(tt)}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="ev-cell {css}">{safe_content}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_html_escape(default_score)}</div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_html_escape(teacher_score)}</div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="ev-cell {css}">&nbsp;</div>', unsafe_allow_html=True)


def _render_item_row(
    display_tt: str,
    ten_tc: str,
    diem_mac_dinh: float,
    current_diem_gv: float,
    current_ghi_chu_gv: str,
    key_base: str,
    readonly: bool,
    row_kind: str,
) -> tuple[float, str]:
    css = "ev-item-even" if row_kind == "item-even" else "ev-item-odd"
    c1, c2, c3, c4, c5 = st.columns([5, 53, 12, 10, 20], gap="small")
    with c1:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_html_escape(display_tt)}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="ev-cell {css}">{_safe_content(ten_tc)}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="ev-cell ev-cell-center {css}">{_format_score(diem_mac_dinh)}</div>', unsafe_allow_html=True)
    with c4:
        diem_gv = st.number_input(
            "Tự chấm",
            min_value=0.0,
            max_value=float(diem_mac_dinh),
            value=float(current_diem_gv),
            step=0.5,
            key=f"diem_gv_{key_base}",
            disabled=readonly,
            label_visibility="collapsed",
        )
    with c5:
        ghi_chu_gv = st.text_input(
            "Ghi chú",
            value=current_ghi_chu_gv,
            key=f"ghi_chu_gv_{key_base}",
            disabled=readonly,
            label_visibility="collapsed",
        )
    return float(diem_gv), str(ghi_chu_gv)


def _prepare_rows(criteria: list[dict[str, Any]], detail_by_ma_tc: dict[str, dict]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for criterion in criteria:
        loai = criterion["loai"]
        ma_tc = criterion["ma_tc"]
        detail = detail_by_ma_tc.get(ma_tc, {}) if ma_tc else {}
        diem_mac_dinh = _resolve_default_score(criterion, detail)
        current_diem_gv = _resolve_teacher_score(detail, diem_mac_dinh)
        key_base = str(detail.get("ID") or f"new_{ma_tc}").replace("/", "_")
        rows.append(
            {
                "ma_tc": ma_tc,
                "ma_cha": criterion.get("ma_cha", ""),
                "loai": loai,
                "ten_tc": criterion["ten_tc"],
                "display_code": criterion.get("display_code", ""),
                "ghi_chu": criterion.get("ghi_chu", ""),
                "tinh_vao_tong": criterion.get("tinh_vao_tong", True),
                "diem_mac_dinh": diem_mac_dinh,
                "current_diem_gv": current_diem_gv,
                "current_ghi_chu_gv": str(detail.get("GhiChuGV", "")).strip(),
                "diem_bgh": str(detail.get("DiemBGH", "")).strip(),
                "ghi_chu_bgh": str(detail.get("GhiChuBGH", "")).strip(),
                "detail": detail,
                "key_base": key_base,
            }
        )
    return rows


def _build_parent_totals(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Calculate display totals for GROUP/SECTION rows from ITEM rows only."""
    row_by_code = {str(row.get("ma_tc", "")).strip(): row for row in rows if str(row.get("ma_tc", "")).strip()}
    totals: dict[str, dict[str, float]] = {}

    for row in rows:
        if row.get("loai") != "ITEM" or not row.get("tinh_vao_tong", True):
            continue

        max_score = _to_float(row.get("diem_mac_dinh"))
        teacher_score = _to_float(row.get("current_diem_gv"))
        parent_code = str(row.get("ma_cha", "")).strip()
        visited: set[str] = set()

        while parent_code and parent_code not in visited:
            visited.add(parent_code)
            parent = row_by_code.get(parent_code)
            if not parent:
                break
            if parent.get("loai") in {"GROUP", "SECTION"}:
                bucket = totals.setdefault(parent_code, {"max": 0.0, "teacher": 0.0})
                bucket["max"] += max_score
                bucket["teacher"] += teacher_score
            parent_code = str(parent.get("ma_cha", "")).strip()

    return totals



def _normalize_detail(record: dict[str, Any]) -> dict[str, Any]:
    """Return CT_ThiDua row with canonical field names.

    Google Sheets readers in earlier iterations may return either exact sheet
    headers or normalized/lowercase keys. Saving requires ID, IDPhieu and MaTC,
    so the form must not depend on one key style only.
    """
    return {
        "ID": _get_text(record, "ID", "id"),
        "IDPhieu": _get_text(record, "IDPhieu", "ID Phiếu", "id_phieu", "idphieu"),
        "MaTC": _get_text(record, "MaTC", "Mã TC", "ma_tc", "MaTieuChi", "ma_tieu_chi"),
        "DiemMacDinh": _get_text(record, "DiemMacDinh", "Điểm mặc định", "Điểm gợi ý", "diem_mac_dinh", "diemmacdinh"),
        "DiemGV": _get_text(record, "DiemGV", "Điểm GV", "Điểm giáo viên", "Điểm GV chấm", "Tự chấm", "diem_gv", "diemgv"),
        "DiemBGH": _get_text(record, "DiemBGH", "Điểm BGH", "Điểm BGH chỉnh", "diem_bgh", "diembgh"),
        "GhiChuGV": _get_text(record, "GhiChuGV", "Ghi chú GV", "ghi_chu_gv", "ghichugv"),
        "GhiChuBGH": _get_text(record, "GhiChuBGH", "Ghi chú BGH", "ghi_chu_bgh", "ghichubgh"),
        "NgayCapNhat": _get_text(record, "NgayCapNhat", "Ngày cập nhật", "ngay_cap_nhat"),
        "NguoiCapNhat": _get_text(record, "NguoiCapNhat", "Người cập nhật", "nguoi_cap_nhat"),
    }

def _resolve_official_score_for_display(row: dict[str, Any], teacher_score: float) -> float:
    """Resolve displayed official score.

    Some older rows may store DiemBGH as 0 instead of blank.
    By business rule, DiemBGH is only official when BGH actually adjusted it.
    If DiemBGH is 0 but there is no BGH note and teacher score is not 0,
    treat it as blank to avoid showing total 0 on submitted teacher forms.
    """
    raw_bgh = str(row.get("diem_bgh", "")).strip()
    if raw_bgh == "":
        return float(teacher_score)

    bgh_score = _to_float(raw_bgh)
    bgh_note = str(row.get("ghi_chu_bgh", "")).strip()
    if bgh_score == 0 and float(teacher_score) != 0 and not bgh_note:
        return float(teacher_score)
    return float(bgh_score)


def _calculate_total_from_state(rows: list[dict[str, Any]]) -> float:
    total = 0.0
    for row in rows:
        if row["loai"] != "ITEM":
            continue
        state_key = f"diem_gv_{row['key_base']}"
        value = st.session_state.get(state_key, row["current_diem_gv"])
        total += _resolve_official_score_for_display(row, _to_float(value))
    return total


def _is_changed(row: dict[str, Any], diem_gv: float, ghi_chu_gv: str) -> bool:
    detail = row["detail"]
    original_diem_gv = _to_float(detail.get("DiemGV", "")) if detail else row["diem_mac_dinh"]
    stored_default = _to_float(detail.get("DiemMacDinh", "")) if detail else row["diem_mac_dinh"]
    current_ghi_chu_gv = row["current_ghi_chu_gv"]
    return (
        float(diem_gv) != original_diem_gv
        or row["diem_mac_dinh"] != stored_default
        or str(ghi_chu_gv).strip() != current_ghi_chu_gv
    )


def _safe_content(content: str) -> str:
    return _html_escape(content) if content else '<span class="ev-placeholder">Chưa có nội dung tiêu chí</span>'


def _normalize_criterion(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "ma_tc": _get_text(record, "MaTC", "Mã TC", "ma_tc", "MaTieuChi", "Mã tiêu chí", "ma_tieu_chi"),
        "ma_cha": _get_text(record, "MaCha", "Mã cha", "ma_cha", "MaChaTieuChi", "ma_cha_tieu_chi"),
        "ten_tc": _get_text(
            record,
            "TenTieuChi",
            "ten_tieu_chi",
            "TenTC",
            "Tên tiêu chí",
            "TieuChi",
            "Tiêu chí",
            "NoiDung",
            "Nội dung",
            "noi_dung",
            "Tiêu chí xét thi đua",
        ),
        "loai": _get_text(record, "Loai", "loai", "Loại", "loai_tieu_chi", "LoaiTieuChi", "Loại tiêu chí").upper(),
        "display_code": _get_text(record, "MaHienThi", "ma_hien_thi", "Mã hiển thị"),
        "ghi_chu": _get_text(record, "GhiChu", "Ghi chú", "ghi_chu"),
        "tinh_vao_tong": _to_bool(_get_text(record, "TinhVaoTong", "Tính vào tổng", "tinh_vao_tong"), default=True),
        "diem": _to_float(
            _get_text(
                record,
                "DiemMacDinh",
                "Điểm mặc định",
                "Diem",
                "Điểm",
                "GiaTriLonNhat",
                "gia_tri_lon_nhat",
                "diem_mac_dinh",
                "DiemMax",
                "Điểm tối đa",
                "diem_max",
                "thang_diem",
                "Thang điểm",
                "Thang điểm đánh giá (100 )",
                "trong_so",
                "Trọng số",
            )
        ),
    }


def _resolve_default_score(criterion: dict[str, Any], detail: dict[str, Any]) -> float:
    stored_default = _to_float(detail.get("DiemMacDinh", "")) if detail else 0.0
    criterion_default = _to_float(criterion.get("diem", ""))
    if stored_default != 0:
        return stored_default
    return criterion_default


def _resolve_teacher_score(detail: dict[str, Any], diem_mac_dinh: float) -> float:
    if not detail:
        return diem_mac_dinh
    raw = str(detail.get("DiemGV", "")).strip()
    ghi_chu = str(detail.get("GhiChuGV", "")).strip()
    if raw == "":
        return diem_mac_dinh
    value = _to_float(raw)
    if value == 0 and diem_mac_dinh != 0 and not ghi_chu:
        return diem_mac_dinh
    return min(value, diem_mac_dinh)


def _get_text(record: dict[str, Any], *keys: str) -> str:
    normalized = {_normalize_key(key): value for key, value in record.items()}
    for key in keys:
        value = record.get(key)
        if value is not None and str(value).strip() != "":
            return str(value).strip()
        normalized_value = normalized.get(_normalize_key(key))
        if normalized_value is not None and str(normalized_value).strip() != "":
            return str(normalized_value).strip()
    return ""


def _normalize_key(value: str) -> str:
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


def _to_bool(value: Any, default: bool = False) -> bool:
    text = str(value).strip().lower()
    if text == "":
        return default
    if text in {"true", "1", "yes", "y", "x", "co", "có"}:
        return True
    if text in {"false", "0", "no", "n", "khong", "không"}:
        return False
    return default


def _to_float(value: Any) -> float:
    if value is None or str(value).strip() == "":
        return 0.0
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return 0.0


def _format_score(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def _to_roman(number: int) -> str:
    values = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    result = ""
    remaining = number
    for value, symbol in values:
        while remaining >= value:
            result += symbol
            remaining -= value
    return result


def _html_escape(value: Any) -> str:
    text = str(value)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")
