import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from mayavi import mlab
from pandas import DataFrame 
from PIL import Image
import os
#-------------------------Input----------------------------------------------------#
add_selectbox = st.sidebar.selectbox(
    "Select material",
    ("Au", "Nb", "TiN", "Ta", "TiC", "Ti",  "VC",  "VN")
)
number = st.sidebar.number_input('Please enter the inner diameter of the cylinder into the box below.',value  = 200, step = 10)
st.sidebar.markdown("""
In the materials specifications:
\n\n - d represents the inner radius of the cylinder
\n\n - D represents the outer radius of the cylinder
\n\n - h1 represents the center-to-center distance between two adjacent cylinders with a default value of 430nm""")
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
#----------------Goi ham va ve do thi--------------------------------------------#
if st.button("Run"):
    if (add_selectbox == "Au"): Au_model(number)
    if (add_selectbox == "Nb"): Nb_model(number)
    if (add_selectbox == "TiN"): TiN_model(number)
    if (add_selectbox == "Ta"): Ta_model(number)
    if (add_selectbox == "TiC"): TiC_model(number)
    if (add_selectbox == "Ti"): Ti_model(number)
    if (add_selectbox == "VC"): VC_model(number)
    if (add_selectbox == "VN"): VN_model(number)
    
    st.subheader("The absorption spectrum")
    plt.figure(dpi = 300)
    fig, ax = plt.subplots()
    ax.plot(abs_wl[ :, 0], abs_wl[ :, 1])
    ax.set_xlabel("wavelength(nm)")
    ax.set_ylabel("Abs")
    ax.set_xlim([200, 3000])
    ax.set_ylim([0, 1])
    st.pyplot(fig)
    #----------------Hieu suat hap thu-------------------------------------------------#
    H = 0
    for i in range(0, 1002, 1):
        H += ((abs_wl[i+1, 1]+abs_wl[i, 1])/2) *(abs_wl[i+1, 0] - abs_wl[i, 0] )
    H = H/2700
    st.markdown("The average absorption efficiency of :blue[**%s**] at d =  %d, h1 = %d is: **%.2f** %% " %(add_selectbox, number, number+30, 100*H))
    #------------------------------Tao va lưu du lieu------------------------------------#
    col1, col2 = st.columns([2.5, 1])
    with col2:
        st.subheader("Data")
        data = pd.DataFrame(abs_wl, columns=['Wavelength', 'Abs'])
        data_csv = st.dataframe(data, height=500, width=400)
    
        #save fiel as CSV
        data1 = data.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=data1, 
            file_name='data.csv',
            mime='text/csv')
    
        #save fiel as txt
        data2 = data.to_csv(index=False, sep='\t')
        st.download_button(
            label="Download data as TXT",
            data=data2, 
            file_name='data.txt',
            mime='text/csv')
    #------------------------------Hinh anh vat lieu---------------------------------------#
    def img3d(d):
        D = d + 30 
        h1 = D
        mlab.options.offscreen = True
        mlab.figure(size=(700, 700), bgcolor=(1, 1, 1))
        x = np.array([0, 1, 1, 0, 0, 1, 1, 0])*(430*2+D+200) 
        y = np.array([0, 0, 1, 1, 0, 0, 1, 1])*(430+D+200)
        z = np.array([0, 0, 0, 0, -1, -1, -1, -1])*150
        t = [[0, 1, 2], [2, 3, 0], 
            [4, 5, 6], [6, 7, 4], 
            [0, 1, 5], [5, 4, 0], 
            [1, 2, 6], [1, 6, 5], 
            [2, 3, 7], [7, 6, 2], 
            [0, 3, 4], [4, 7, 3]]
        mlab.triangular_mesh(x, y, z, t, color=(0.8, 0.7, 0.65))
        #set
        theta = np.linspace(0, 2*np.pi, 50)
        h = np.linspace(0, h1, 50)
        theta, h = np.meshgrid(theta, h)
    
        for i in range(0, 3, 1):
            for r in np.linspace(d/2, D/2, 30):
                x3 = 430*i + D/2 + 100 + (r)*np.cos(theta)
                y3 = D/2 + 100 + (r)*np.sin(theta)
                mlab.mesh(x3, y3, h, color=(0.8, 0.7, 0.65))
    
        for i in range(0, 3, 1):
            for r in np.linspace(d/2, D/2, 30):
                x3 = 430*i + D/2 + 100 + (r)*np.cos(theta)
                y3 = 430 + D/2 + 100 + (r)*np.sin(theta)
                mlab.mesh(x3, y3, h, color=(0.8, 0.7, 0.65))
    #--------------------------------------------------------------------#
    '''
    with col1: 
        st.subheader("Image of the material")
    
        img3d(number)
        def view(theta, phi):
            mlab.view(azimuth=60, elevation=70, distance=2500)#hinh anh ban dau khi chua thay doi goc
            mlab.view(theta, phi, distance=3000)
            mlab.savefig("3D/image.png")
            image_path = '3D/image.png'
    
            st.image(image_path)
            shutil.rmtree('3D')
    
        azimuth = st.slider('The azimuth argument specifies the angle "phi" on the x-y plane.', 0, 360, 60, 10)
        elevation = st.slider('The elevation argument specifies the angle "theta" from the z axis.', 0, 180, 70, 10)
        view(azimuth, elevation)
    '''
