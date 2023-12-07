import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
# from mayavi import mlab
from pandas import DataFrame 
from PIL import Image
import os
import shutil
#-------------------------Input----------------------------------------------------#
add_selectbox = st.sidebar.selectbox(
    "Select material",
    ("Au", "Nb", "TiN", "Ta", "TiC", "Ti",  "VC",  "VN")
)
number = st.sidebar.number_input('Please enter the inner diameter of the cylinder into the box below.',value  = 200, step = 10)
st.sidebar.markdown("""
In the materials specifications:
\n\n - **d** is the inner diameter of the cylinder
\n\n - **D** is the outer diameter of the cylinder
\n\n - **h₁** is the height of TiN nanorings
\n\n - **L** is the center-to-center distance between two adjacent cylinders. In our calculations, we fix it to be 430nm""")

uploaded_file = st.sidebar.file_uploader("", type=["txt", "csv", "xlsx"])
#-----------------------------Lap ham cac thuat toan ML--------------------------------#
def Au_model(d):
    global abs_wl
    extra_model = joblib.load("1_Au_ExtraTressRegression.joblib")
    a = [[1, d+30, d]]*1003
    a = np.array(a).reshape(1,3*1003)
    abs_wl = extra_model.predict(a)
    abs_wl = abs_wl.reshape(1003, 2)
    
def Nb_model(d):
    global abs_wl
    extra_model = joblib.load("2_Nb_ExtraTressRegression.joblib")
    a = [[2, d+30, d]]*1003
    a = np.array(a).reshape(1,3*1003)
    abs_wl = extra_model.predict(a)
    abs_wl = abs_wl.reshape(1003, 2)
   
def TiN_model(d):
    global abs_wl
    extra_model = joblib.load("3_TiN_ExtraTressRegression.joblib")
    a = [[3, d+30, d]]*1003
    a = np.array(a).reshape(1,3*1003)
    abs_wl = extra_model.predict(a)
    abs_wl = abs_wl.reshape(1003, 2)
   
def Ta_model(d):
    global abs_wl
    extra_model = joblib.load("4_Ta_ExtraTressRegression.joblib")
    a = [[4, d+30, d]]*1003
    a = np.array(a).reshape(1,3*1003)
    abs_wl = extra_model.predict(a)
    abs_wl = abs_wl.reshape(1003, 2)
  
def TiC_model(d):
    global abs_wl
    extra_model = joblib.load("5_TiC_ExtraTressRegression.joblib")
    a = [[5, d+30, d]]*1003
    a = np.array(a).reshape(1,3*1003)
    abs_wl = extra_model.predict(a)
    abs_wl = abs_wl.reshape(1003, 2)
    
def Ti_model(d):
    global abs_wl
    extra_model = joblib.load("6_Ti_ExtraTressRegression.joblib")
    a = [[6, d+30, d]]*1003
    a = np.array(a).reshape(1,3*1003)
    abs_wl = extra_model.predict(a)
    abs_wl = abs_wl.reshape(1003, 2)
    
def VC_model(d):
    global abs_wl
    extra_model = joblib.load("7_VC_ExtraTressRegression.joblib")
    a = [[7, d+30, d]]*1003
    a = np.array(a).reshape(1,3*1003)
    abs_wl = extra_model.predict(a)
    abs_wl = abs_wl.reshape(1003, 2)
   
def VN_model(d):
    global abs_wl
    extra_model = joblib.load("8_VN_ExtraTressRegression.joblib")
    a = [[8, d+30, d]]*1003
    a = np.array(a).reshape(1,3*1003)
    abs_wl = extra_model.predict(a)
    abs_wl = abs_wl.reshape(1003, 2)

def efficiency(abs_wl):
    global H
    H = 0
    for i in range(0, 1002, 1):
        H += ((abs_wl[i+1, 1]+abs_wl[i, 1])/2) *(abs_wl[i+1, 0] - abs_wl[i, 0] )
    H = H/2700
    return H
#----------------Goi ham va ve do thi--------------------------------------------#
st.markdown(" We calculate the spectral absorption of TiN-nanoring-based metamaterials by machine learning algorithms and data sets collected from CST simulations. The structure of the metamaterials is following:")
# st.image("3D/fig1.jpeg",width= 300, use_column_width=True)
st.image("3D/fig1.jpeg",width= 500)
if st.button("Spectral Absorption Prediction"):
    H = []
    if (add_selectbox == "Au"):
        for i in range(200, 400, 5):
            Au_model(i)
            H = H + [efficiency(abs_wl)]
        Au_model(number)
    
    if (add_selectbox == "Nb"):
        for i in range(200, 400, 5):
            Nb_model(i)
            H = H + [efficiency(abs_wl)]
        Nb_model(number)
    
    if (add_selectbox == "TiN"):
        for i in range(200, 400, 5):
            TiN_model(i)
            H = H + [efficiency(abs_wl)]
        TiN_model(number)
        
    if (add_selectbox == "Ta"):
        for i in range(200, 400, 5):
            Ta_model(i)
            H = H + [efficiency(abs_wl)]
        Ta_model(number)
    
    if (add_selectbox == "TiC"):
        for i in range(200, 400, 5):
            TiC_model(i)
            H = H + [efficiency(abs_wl)]
        TiC_model(number)
    
    if (add_selectbox == "Ti"):
        for i in range(200, 400, 5):
            Ti_model(i)
            H = H + [efficiency(abs_wl)]
        Ti_model(number)
    
    if (add_selectbox == "VC"):
        for i in range(200, 400, 5):
            VC_model(i)
            H = H + [efficiency(abs_wl)]
        VC_model(number)
    if (add_selectbox == "VN"):
        for i in range(200, 400, 5):
            VN_model(i)
            H = H + [efficiency(abs_wl)]
        VN_model(number)
    
    H0 =max(H)
    index_max = H.index(max(H))
    D = range(200, 400, 5)
    D0 = D[index_max]
    col1, col2 = st.columns([3.6, 1])
    with col1:
        if uploaded_file is None:
            # st.subheader("The absorption spectrum")
            plt.figure(dpi = 300)
            fig, ax = plt.subplots()
            ax.plot(abs_wl[ :, 0], abs_wl[ :, 1])
            ax.set_xlabel("wavelength(nm)")
            ax.set_ylabel("Efficiency")
            ax.set_xlim([200, 3000])
            ax.set_ylim([0, 1])
            st.pyplot(fig)
    #----------------------------Read data uploaded file -----------------------------------#
        if uploaded_file is not None:
            if uploaded_file.type == "text/csv":  # Đối với file csv
                data_upload = pd.read_csv(uploaded_file, delimiter=',' ,skiprows=1, header=None)
                # st.write(data_upload)
                num_columns = len(data_upload.columns)
                if (num_columns==2):
                    col0 = data_upload.iloc[1:, 0]
                    col1 = data_upload.iloc[1:, 1]
                if (num_columns==3):
                    col0 = data_upload.iloc[1:, 1]
                    col1 = data_upload.iloc[1:, 2]
                    
            if uploaded_file.type == "text/plain":  # Đối với file txt
                data_upload = pd.read_csv(uploaded_file, delimiter='\s+',skiprows=1, header=None)
                # st.write(data_upload)
                num_columns = len(data_upload.columns)
                if (num_columns==2):
                    col0 = data_upload.iloc[1:, 0]
                    col1 = data_upload.iloc[1:, 1]
                if (num_columns==3):
                    col0 = data_upload.iloc[1:, 1]
                    col1 = data_upload.iloc[1:, 2]
                    
            if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":  # Đối với file Excel
                data_upload = pd.read_excel(uploaded_file, engine="openpyxl",skiprows=1, header=None)
                # st.write(data_upload)
                num_columns = len(data_upload.columns)
                if (num_columns==2):
                    col0 = data_upload.iloc[1:, 0]
                    col1 = data_upload.iloc[1:, 1]
                if (num_columns==3):
                    col0 = data_upload.iloc[1:, 1]
                    col1 = data_upload.iloc[1:, 2]
        #-----------------------------------------------------------------------------------#
            plt.figure(dpi = 300)
            fig, ax = plt.subplots()
            # ax.plot(abs_wl[ :, 0], abs_wl[ :, 1],'r',  label='predicted results', marker='o', markersize=4, markevery=27)
            # ax.plot(col0, col1,'b',  label="user's data", marker='s', markersize=4, markevery=int(len(col0)/30))
            ax.plot(abs_wl[ :, 0], abs_wl[ :, 1],'r', label='predicted results')
            ax.plot(col0, col1,'b', label="user's data")
            ax.set_xlabel("wavelength(nm)")
            ax.set_ylabel("Efficiency")
            ax.set_xlim([200, 3000])
            ax.set_ylim([0, 1])
            ax.legend()
            st.pyplot(fig)
    #----------------Hieu suat hap thu-------------------------------------------------#
    st.write("The average absorption efficiency of :blue[**%s**] at d =  **%d** nm, h1 = **%d** nm is: **%.2f** %% " %(add_selectbox, number, number+30, 100*efficiency(abs_wl)))
    st.write('The maximum absorption efficiency of :blue[**%s**] is **%.2f** %% at d= **%d** nm , h1 = **%d** nm' %(add_selectbox, H0*100, D0, D0+30))  
    #------------------------------Tao va lưu du lieu------------------------------------#
    with col2:
        # st.write("Data")
        data = pd.DataFrame(abs_wl, columns=['Wavelength', 'Efficiency'])
        data_csv = st.dataframe(data, height=380, width=200)
    
        #save fiel as txt
        data2 = data.to_csv(index=False, sep='\t')
        st.download_button(
            label="Download as TXT",
            data=data2, 
            file_name='data.txt',
            mime='text/csv')
        
    st.markdown("In the future, we can develop our program to determine the absorption of metamaterials with more structural parameters and the presence of the dielectric layer sandwiched by two plasmonic layers as following.")
    st.image("3D/fig2.jpeg", use_column_width=True)
