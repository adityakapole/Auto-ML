from operator import index
import streamlit as st
import plotly.express as px
from pycaret.regression import setup as setup_reg, compare_models as compare_models_reg
from pycaret.classification import (
    setup as setup_clf,
    compare_models as compare_models_clf,
)
from pycaret.regression import pull as pull_reg, save_model as save_model_reg
from pycaret.classification import pull as pull_clf, save_model as save_model_clf
import sweetviz as sv
import pandas as pd
import os

st.set_page_config(page_title="AutoML:Minion", page_icon="⚙️")

if os.path.exists("./dataset.csv"):
    df = pd.read_csv("dataset.csv", index_col=None)


with st.sidebar:
    st.image("asset/main_img.jpeg")
    st.title("AutoML:Minion")
    choice = st.radio("Navigation", ["Upload", "Profiling", "Modelling", "Download"])
    st.info(
        "From CSV input to comprehensive data analysis and the best-trained model in one streamlined process."
    )


if choice == "Upload":
    st.title("Upload Your Dataset")
    file = st.file_uploader("Upload Your Dataset")
    if file:
        df = pd.read_csv(file, index_col=None)
        df.to_csv("dataset.csv", index=None)
        st.dataframe(df)

if choice == "Profiling":
    st.title("Exploratory Data Analysis")
    # if st.button("Download EDA Report"):
    with open("SWEETVIZ_REPORT.html", "rb") as f:
        report = sv.analyze(df)
        report.show_html()
        st.download_button("Download EDA Report", f, file_name="SWEETVIZ_REPORT.html")


if choice == "Modelling":
    st.title("Model Training")
    model_type = st.radio(
        "Choose the Model Type",
        ["Regression", "Classification"],
        key="model_type_selection",
    )
    chosen_target = st.selectbox("Choose the Target Column", df.columns)

    if st.button("Run Modelling"):
        if model_type == "Regression":
            setup_reg(df, target=chosen_target)
            setup_df = pull_reg()
            st.dataframe(setup_df)
            best_model = compare_models_reg()
            compare_df = pull_reg()
            st.dataframe(compare_df)
            save_model_reg(best_model, "best_model")
        else:
            setup_clf(df, target=chosen_target)
            setup_df = pull_clf()
            st.dataframe(setup_df)
            best_model = compare_models_clf()
            compare_df = pull_clf()
            st.dataframe(compare_df)
            save_model_clf(best_model, "best_model")


if choice == "Download":
    with open("best_model.pkl", "rb") as f:
        st.download_button("Download Model", f, file_name="best_model.pkl")
    with open("Run.ipynb", "rb") as f:
        st.download_button("Load Model File", f, file_name="Run.ipynb")
