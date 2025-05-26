import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

st.set_page_config(page_title="당뇨병 데이터 시각화", layout="wide")

st.title("🩺 당뇨병 데이터 시각화 앱 (Plotly 없이)")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("diabetes_data.csv")
    df["Gender_label"] = df["Gender"].map({0: "여성", 1: "남성"})
    return df

df = load_data()

# 사이드바 메뉴
option = st.sidebar.selectbox(
    "시각화 선택",
    ("당뇨병 진단 분포", "성별에 따른 분포", "증상별 평균 비교")
)

# 1. Altair: 당뇨병 진단 분포
if option == "당뇨병 진단 분포":
    st.subheader("당뇨병 진단 유무 분포 (Altair)")
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("class:N", title="당뇨병 여부 (0=비당뇨, 1=당뇨)"),
        y=alt.Y("count()", title="개수"),
        color="class:N"
    ).properties(width=600, height=400)
    st.altair_chart(chart)

# 2. Matplotlib: 성별에 따른 당뇨병 여부
elif option == "성별에 따른 분포":
    st.subheader("성별에 따른 당뇨병 분포 (Matplotlib)")
    cross = pd.crosstab(df["Gender_label"], df["class"])
    fig, ax = plt.subplots()
    cross.plot(kind="bar", ax=ax, colormap="viridis")
    plt.title("성별에 따른 당뇨병 진단 분포")
    plt.xlabel("성별")
    plt.ylabel("개수")
    st.pyplot(fig)

# 3. Altair: 증상별 평균 비교
elif option == "증상별 평균 비교":
    st.subheader("증상별 당뇨병 유무에 따른 평균값 비교 (Altair)")
    symptoms = df.columns[:-2]  # 마지막 2개 제외 (Gender_label, class)
    symptom_summary = df.groupby("class")[symptoms].mean().T
    symptom_summary.columns = ["비당뇨", "당뇨"]
    symptom_df = symptom_summary.reset_index().rename(columns={"index": "증상"})

    melted = symptom_df.melt(id_vars="증상", var_name="구분", value_name="비율")

    chart = alt.Chart(melted).mark_bar().encode(
        x=alt.X("증상:N", sort=None),
        y="비율:Q",
        color="구분:N",
        column=alt.Column("구분:N")
    ).properties(width=300)
    st.altair_chart(chart)

# 원본 데이터 보기
if st.checkbox("📄 원본 데이터 보기"):
    st.dataframe(df)
