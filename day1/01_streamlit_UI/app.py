import streamlit as st
import pandas as pd
from datetime import datetime
import uuid, os

st.set_page_config(page_title="全国歯学部アンケート", layout="wide")

UNIVERSITIES = [  # ← 修正: 正しい名称
    "北海道大学", "東北大学", "東京医科歯科大学", "新潟大学", "大阪大学", "岡山大学",
    # … 他 23 校
]
YEARS = ["1 年","2 年","3 年","4 年","5 年","6 年","研修医"]
CSV_FILE = "responses.csv"

with st.sidebar:
    st.header("アンケート概要")
    st.write("• 匿名  • 所要約3分  • 締切:2025‑06‑15")
    st.divider()
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        st.write("平均講義満足度:", df.lec_q.mean().round(2))

st.title("全国歯学部生アンケート2025")
st.caption("所要時間≈3分｜匿名で収集")

with st.form("survey_form", clear_on_submit=True):
    st.subheader("① 基本属性")
    university = st.selectbox("所属大学 *", UNIVERSITIES)
    year       = st.selectbox("学年 *",     YEARS)
    gender     = st.radio("性別", ["男性","女性","回答しない"], index=2, horizontal=True)

    st.subheader("② 学習環境")
    lec_q  = st.slider("講義内容", 1,5,3)
    cli_q  = st.slider("臨床実習", 1,5,3)
    digi_q = st.slider("デジタル歯科教育", 1,5,3)
    eng_q  = st.slider("英語教育",      1,5,3)

    st.subheader("③ キャリア志向")
    future_paths    = st.multiselect("興味のある進路", ["大学院","開業","病院","企業","海外臨床","官公庁","その他"])
    overseas_intent = st.slider("海外勤務意向 (%)", 0,100,0)

    st.subheader("④ 睡眠歯科への関心")
    sleep_knowledge = st.slider("理解度", 1,5,3)
    sleep_curriculum = st.radio(
        "もっと講義を増やすべきか？",
        ["強く思う","やや思う","どちらとも","あまり思わない","全く思わない"],
        index=2
    )
    comments = st.text_area("自由記述（任意）")

    # ← ここが Submit ボタン
    submitted = st.form_submit_button("送信")

    if submitted:
        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "uuid":       str(uuid.uuid4()),
            "university": university,
            "year":       year,
            "gender":     gender,
            "lec_q":      lec_q,
            "cli_q":      cli_q,
            "digi_q":     digi_q,
            "eng_q":      eng_q,
            "future_paths": ";".join(future_paths),
            "overseas_intent": overseas_intent,
            "sleep_knowledge": sleep_knowledge,
            "sleep_curriculum": sleep_curriculum,
            "comments": comments
        }
        df_new = pd.DataFrame([row])
        header = not os.path.exists(CSV_FILE)
        df_new.to_csv(CSV_FILE, mode="a", index=False, header=header, encoding="utf-8")

        st.success("ご協力ありがとうございました！")
        st.balloons()
