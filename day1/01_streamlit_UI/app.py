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
    # 国立大学（11校）
    "北海道大学",
    "東北大学",
    "東京医科歯科大学",
    "新潟大学",
    "大阪大学",
    "岡山大学",
    "広島大学",
    "徳島大学",
    "九州大学",
    "長崎大学",
    "鹿児島大学",
    # 私立大学／その他（18校）
    "大阪歯科大学",
    "東京歯科大学",
    "昭和大学",
    "日本大学",
    "明海大学",
    "神奈川歯科大学",
    "鶴見大学",
    "松本歯科大学",
    "愛知学院大学",
    "朝日大学",
    "北海道医療大学",
    "岩手医科大学",
    "奥羽大学",
    "日本歯科大学 生命歯学部",
    "日本歯科大学 新潟生命歯学部",
    "福岡歯科大学",
    "九州歯科大学",
    "長崎県立大学"
]

YEARS = ["1 年", "2 年", "3 年", "4 年", "5 年", "6 年", "研修医"]

CSV_FILE = "responses.csv"

# -------- サイドバー --------
with st.sidebar:
    st.header("アンケート概要")
    st.write("• 匿名回答  • 所要約3分  • 締切: 2025-06-15")
    st.divider()

    # すでに回答があれば、簡易集計を表示
    if os.path.exists(CSV_FILE):
        df_all = pd.read_csv(CSV_FILE)
        st.subheader("📊 平均スコア")
        st.write({
            "講義内容": df_all.lec_q.mean().round(2),
            "臨床実習": df_all.cli_q.mean().round(2),
            "デジタル歯科": df_all.digi_q.mean().round(2),
            "英語教育": df_all.eng_q.mean().round(2),
        })
        st.bar_chart(df_all[["lec_q", "cli_q", "digi_q", "eng_q"]])

# -------- メインタイトル --------
st.title("全国歯学部生アンケート 2025")
st.caption("所要時間 ≈ 3 分 ｜ 回答は匿名で収集されます")

# -------- アンケートフォーム --------
with st.form("survey_form", clear_on_submit=True):
    # ① 基本属性
    st.subheader("① 基本属性")
    university = st.selectbox("所属大学 *", UNIVERSITIES)
    year       = st.selectbox("学年 *",     YEARS)
    gender     = st.radio("性別", ["男性", "女性", "回答しない"], index=2, horizontal=True)

    # ② 学習環境の詳細評価
    st.subheader("② 学習環境の詳細評価")
    st.caption("※ 1 = 非常に不満, 5 = 非常に満足")

    # --- 講義・座学 ---
    with st.expander("講義・座学"):
        lec_clarity   = st.slider("講義の分かりやすさ",                 1, 5, 3, format="%d")
        lec_materials = st.slider("資料・スライドの充実度",             1, 5, 3, format="%d")
        lec_active    = st.slider("双方向的授業（質疑・ディスカッション）の頻度", 1, 5, 3, format="%d")
        lec_comment   = st.text_area("講義に関するご意見（任意）", key="lec_c")

    # --- 臨床実習・実技 ---
    with st.expander("臨床実習・実技"):
        cli_supervision = st.slider("指導医のサポート体制",     1, 5, 3, format="%d")
        cli_cases       = st.slider("症例数・多様性",           1, 5, 3, format="%d")
        cli_feedback    = st.slider("実習後フィードバックの質", 1, 5, 3, format="%d")
        cli_comment     = st.text_area("実習に関するご意見（任意）", key="cli_c")

    # --- デジタル歯科・ICT ---
    with st.expander("デジタル歯科・ICT"):
        digi_equipment = st.slider("CAD/CAM等機器の利用機会",         1, 5, 3, format="%d")
        digi_curric    = st.slider("AI・デジタル技術の講義充実度",     1, 5, 3, format="%d")
        digi_comment   = st.text_area("デジタル教育の改善点（任意）", key="digi_c")

    # --- 語学・国際化 ---
    with st.expander("語学・国際化"):
        eng_general   = st.slider("一般英語授業の質",       1, 5, 3, format="%d")
        eng_clinical  = st.slider("歯科専門英語教育の充実度", 1, 5, 3, format="%d")
        intl_exchange = st.slider("海外研修・交換留学の機会", 1, 5, 3, format="%d")
        eng_comment   = st.text_area("語学教育への要望（任意）", key="eng_c")

    # --- 重要度ヒアリング ---
    importance = st.radio(
        "今後、大学が **最も力を入れるべき** 分野は？",
        ["講義・座学", "臨床実習", "デジタル歯科", "語学・国際化", "研究機会"],
        horizontal=True
    )

    # ③ キャリア志向
    st.subheader("③ キャリア志向")
    future_paths    = st.multiselect(
        "興味のある進路（複数選択可）",
        ["大学院", "臨床開業医", "病院勤務", "企業／研究職", "海外臨床", "公衆衛生／官公庁", "その他"]
    )
    overseas_intent = st.slider("卒後5年以内に海外で働く意向 (%)", 0, 100, 0)

    # ④ 睡眠歯科への関心
    st.subheader("④ 睡眠歯科への関心")
    sleep_knowledge  = st.slider("睡眠歯科の理解度",                         1, 5, 3)
    sleep_curriculum = st.radio(
        "カリキュラムに睡眠歯科の講義をもっと取り入れるべきだと思いますか？",
        ["強く思う", "やや思う", "どちらとも言えない", "あまり思わない", "全く思わない"],
        index=2
    )
    comments = st.text_area("自由記述（任意）", placeholder="ご意見・ご要望など")

    # 送信ボタン
    submitted = st.form_submit_button("送信")
    if submitted:
        # 保存処理…
        st.success("ご協力ありがとうございました！")
        st.balloons()
        header = not os.path.exists(CSV_FILE)
        df_new.to_csv(CSV_FILE, mode="a", index=False, header=header, encoding="utf-8")
        st.success("ご協力ありがとうございました！")
        st.balloons()
