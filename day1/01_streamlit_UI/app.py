import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import os

# -------- ページ設定 --------
st.set_page_config(
    page_title="全国歯学部アンケート",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------- 定数 --------
UNIVERSITIES = [
    "北海道大学", "東北大学", "東京医科歯科大学", "新潟大学", "大阪大学", "岡山大学",
    "広島大学", "徳島大学", "九州大学", "長崎大学", "鹿児島大学",
    "大阪歯科大学", "東京歯科大学", "昭和大学", "日本大学", "明海大学",
    "神奈川歯科大学", "鶴見大学", "松本歯科大学", "愛知学院大学", "朝日大学",
    "北海道医療大学", "岩手医科大学", "奥羽大学", "日本歯科大学 生命歯学部",
    "日本歯科大学 新潟生命歯学部", "福岡歯科大学", "九州歯科大学", "長崎県立大学"
]
YEARS = ["1 年", "2 年", "3 年", "4 年", "5 年", "6 年", "研修医"]
CSV_FILE = "responses.csv"

# -------- サイドバー --------
with st.sidebar:
    st.header("アンケート概要")
    st.write("• 匿名回答\n• 所要約3分\n• 締切: 2025‑06‑15")
    st.divider()

    # 送信済みなら集計を表示
    if os.path.exists(CSV_FILE):
        df_all = pd.read_csv(CSV_FILE)
        st.subheader("📊 平均スコア")
        st.write({
            "講義内容": df_all.lec_q.mean().round(2),
            "臨床実習": df_all.cli_q.mean().round(2),
            "デジタル歯科": df_all.digi_q.mean().round(2),
            "英語教育": df_all.eng_q.mean().round(2),
        })
        st.bar_chart(df_all[["lec_q","cli_q","digi_q","eng_q"]])

# -------- アンケートフォーム --------
progress = st.progress(0)

with st.form("survey"):
    # ステップ1/4
    st.header("① 基本属性")
    university = st.selectbox("所属大学 *", UNIVERITIES)
    year       = st.selectbox("学年 *",     YEARS)
    gender     = st.radio("性別", ["男性","女性","回答しない"], index=2, horizontal=True)
    if not university or not year:
        st.error("大学と学年は必須です。")
    progress.progress(25)

    # ステップ2/4
    with st.expander("② 学習環境への満足度", expanded=True):
        lec_q  = st.slider("講義内容", 1, 5, 3)
        cli_q  = st.slider("臨床実習", 1, 5, 3)
        digi_q = st.slider("デジタル歯科教育", 1, 5, 3)
        eng_q  = st.slider("英語教育", 1, 5, 3)
    progress.progress(50)

    # ステップ3/4
    with st.expander("③ キャリア志向", expanded=False):
        future_paths    = st.multiselect(
            "興味のある進路", 
            ["大学院","臨床開業医","病院勤務","企業/研究","海外臨床","官公庁","その他"]
        )
        overseas_intent = st.slider("卒後5年以内に海外勤務意向 (%)", 0, 100, 0)
    progress.progress(75)

    # ステップ4/4
    with st.expander("④ 睡眠歯科への関心", expanded=False):
        sleep_knowledge = st.slider("睡眠歯科の理解度", 1, 5, 3)
        sleep_curriculum = st.radio(
            "カリキュラムに睡眠歯科を強化するべきか？",
            ["強く思う","やや思う","どちらとも","あまり思わない","全く思わない"],
            index=2
        )
        comments = st.text_area("自由記述（任意）")
    progress.progress(100)

    # 送信ボタン
    submit = st.form_submit_button("送信")
    if submit:
        # 重複チェック（大学・学年・性別の組み合わせ）
        if os.path.exists(CSV_FILE):
            df_prev = pd.read_csv(CSV_FILE)
            dup = df_prev[
                (df_prev.university==university)&
                (df_prev.year==year)&
                (df_prev.gender==gender)
            ]
            if not dup.empty:
                st.warning("※ 同じ属性で既に回答が記録されています。更新しますか？")
        # レスポンス保存
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
        # CSV 追記
        df_new = pd.DataFrame([row])
        header = not os.path.exists(CSV_FILE)
        df_new.to_csv(CSV_FILE, mode="a", index=False, header=header, encoding="utf-8")
        st.success("ご協力ありがとうございました！")
        st.balloons()
