import streamlit as st
import pandas as pd
import plotly.express as px

# 제목
st.title("🩺 당뇨병 데이터 시각화 웹앱")

# 데이터 불러오기
@st.cache_data
def load_data():
    file_path = "diabetes_data.csv"  # 같은 폴더에 있어야 함
    df = pd.read_csv(file_path)
    df['Gender_label'] = df['Gender'].map({0: '여성', 1: '남성'})
    return df

df = load_data()

# 사용자 선택: 시각화 종류
option = st.sidebar.selectbox(
    "📊 보고 싶은 그래프를 선택하세요",
    (
        "당뇨병 진단 분포",
        "성별에 따른 당뇨병 분포",
        "증상별 당뇨병 유무 비교"
    )
)

# 1. 당뇨병 진단 유무 분포
if option == "당뇨병 진단 분포":
    fig = px.histogram(df, x="class", color="class",
                       title="당뇨병 진단 유무 분포",
                       labels={"class": "당뇨병 여부"},
                       category_orders={"class": [0, 1]})
    st.plotly_chart(fig)

# 2. 성별에 따른 당뇨병 분포
elif option == "성별에 따른 당뇨병 분포":
    fig = px.histogram(df, x="Gender_label", color="class", barmode="group",
                       title="성별에 따른 당뇨병 유무 분포",
                       labels={"Gender_label": "성별", "class": "당뇨병 여부"})
    st.plotly_chart(fig)

# 3. 증상별 당뇨병 환자 비율 시각화
elif option == "증상별 당뇨병 유무 비교":
    symptoms = df.columns[:-2]  # Gender_label, class 제외
    symptom_summary = df.groupby("class")[symptoms].mean().T
    symptom_summary.columns = ["비당뇨", "당뇨"]
    symptom_summary = symptom_summary.reset_index().rename(columns={"index": "증상"})

    fig = px.bar(symptom_summary, x="증상", y=["비당뇨", "당뇨"],
                 barmode="group", title="증상별 당뇨병 유무에 따른 발생 비율")
    st.plotly_chart(fig)

# 데이터 보기 옵션
if st.checkbox("🔍 원본 데이터 보기"):
    st.dataframe(df)
