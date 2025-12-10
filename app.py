import streamlit as st
import pandas as pd
from streamlit_calendar import calendar

st.set_page_config(page_title="캘린더", page_icon="🎾")

st.title("🎾 캘린더")

# CSV 불러오기
예약 = pd.read_csv("data/예약.csv")
참석 = pd.read_csv("data/참석.csv")

merge = pd.merge(예약, 참석.groupby(by="날짜").count(), on=["날짜"], how="left")

# 예약 이벤트 생성
예약_events = []
for _, row in merge.iterrows():
    color = "#3D9DF3" if (row["정원"] == row["참석자"]) else "#FFDD6CAF"
    예약_events.append({
        "title": f" 예약: {row['예약자']}({row['정원']})",
        "start": row['날짜'],
        "end": row['날짜'],
        "color": color,  # 파란색
    })

# 참석 이벤트 생성
참석_events = []
for _, row in 참석.iterrows():
    if pd.notna(row['참석자']):
        참석_events.append({
            "title": f"{row['참석자']}",
            "start": row['날짜'],
            "end": row['날짜'],
            "color": "#3DD56D",  # 초록색
        })

# 전체 이벤트 합치기
events = 예약_events + 참석_events

# Calendar 옵션
calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "selectable": "true",
    "initialView": "dayGridMonth",
    "initialDate": "2025-12-01",
}

# 캘린더 출력
state = calendar(
    events=events,
    options=calendar_options,
    custom_css="""
    .fc-event-title {
        font-weight: 600;
    }
    .fc-toolbar-title {
        font-size: 1.5rem;
    }
    """,
    key="daygrid",
)

# st.write("📊 현재 상태:", state)