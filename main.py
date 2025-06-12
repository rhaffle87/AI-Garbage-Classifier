import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Data Simpel")
st.write("Ini adalah dashbord data simpel yang dibuat dengan Streamlit (Python)")

uploaded_file = st.file_uploader("Pilih CSV File", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("Data Summary")                                
    st.write(df.describe())

    st.subheader('Filter Data')
    columns = df.columns.tolist()
    selected_column = st.selectbox("Pilih kolom Filter dengan", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Pilih nilai", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot Data")
    x_column = st.selectbox("Pilih kolom x-axis", columns)
    y_column = st.selectbox("Pilih kolom y-axis", columns)

    if st.button("Buat Plot"):
        st.line_chart(filtered_df.set_index(x_column)[y_column])
    else:
        st.write("Menunggu file untuk diupload...")


