import streamlit as st
import pandas as pd
import pickle
from streamlit_option_menu import option_menu
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


st.set_page_config(
    page_title="Sunrise Senior Livings",
    page_icon="senior-living-home.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

pickle_in = open('model.pkl', 'rb')
svm_classifier = pickle.load(pickle_in)

pickle_in=open('Rfmodel.pkl','rb')
rf_classifier=pickle.load(pickle_in)

def svm_predict(dist,pressure,hrv,sugar_level,spo2,acc):
    if pressure=='Low Blood Pressure':
        pressure=0
    elif pressure =='Medium Level Blood Pressure':
        pressure=1
    else:
        pressure=2

    if acc == "Less Than +-3g":
        acc=0
    else:
        acc=1

    prediction= svm_classifier.predict([[dist,pressure,hrv,sugar_level,spo2,acc]])

    if prediction == 0:
        pred = "Not fall"
    elif prediction ==1:
        pred = "may slip/trip/fumble"
    else:
        pred = "definitely fall"

    return pred

def age_predict(age):
    if age == 'Less than 1year':
        return 0
    elif age== '1yr-13yr':
        return 1
    elif age== '14yr-20yr':
        return 2
    elif age=='21yr-30yr':
        return 3
    elif age=='31yr-40yr':
        return 4
    elif age== '41yr-50yr':
        return 5
    elif age == '51yr - 60yr':
        return 6
    elif age == '61yr - 70yr':
        return 7
    elif age == '71yr - 80yr':
        return 8
    elif age== '81yr - 90yr':
        return 9
    else:
        return 10


def type_injury_predict(type_injury):
    if type_injury=='Bruising':
        return 0
    elif type_injury=='Edema':
        return 1
    elif type_injury=='Fracture ':
        return 2
    elif type_injury=='Hematoma':
        return 3
    elif type_injury=='Head trauma ':
        return 4
    elif type_injury=='Spinal cord injury':
        return 5
    elif type_injury=='Wound dehiscence':
        return 6
    elif type_injury=='Cut':
        return 7
    elif type_injury=='excoriation':
        return 8    
    else:
        return 9


def loc_predict(location):
    if location=='Bathroom/shower':
        return 0
    elif location=='Exam room':
        return 1
    elif location=='Hallway':
        return 2
    elif location=='Medical office':
        return 3
    elif 'Medication: room':
        return 4
    elif location=='Nursing station':
        return 5
    elif 'Operating room':
        return 6
    elif location=='Others':
        return 7
    elif location=='Outpatient adverse event':
        return 8
    elif location =='Recovery room ':
        return 9    
    elif location=='Room':
        return 10
    elif location=='Surgical prep adverse event':
        return 11
    elif location=='Surgical table':
        return 12
    elif location=='Triage adverse event':
        return 13
    elif location=='Vaccination room':
        return 14
    else:
        return 15


def reason_predict(reason):
    if reason== 'Dizziness':
        return 0
    elif reason=='Equipment':
        return 1
    elif reason =='Human error':
        return 2
    elif reason=='Hypotension':
        return 3
    elif reason=='Loss of balance':
        return 4
    elif reason=='Mental confusion':
        return 5
    elif reason =='Mental confusion ':
        return 6
    elif reason=='Paralysis':
        return 7
    elif reason=='Muscle weakness':
        return 8
    elif reason=='Sedation':
        return 9
    elif reason=='Slip':
        return 10
    else:
        return 11


def rf_predict(age,type_injury,location,reason,bool_fall_risk,severity,gender):
    age=age_predict(age)
    type_injury=type_injury_predict(type_injury)
    location=loc_predict(location)
    reason=reason_predict(reason)

    if bool_fall_risk=='No':
        bool_fall_risk=0
    else:
        bool_fall_risk=1
    

    if severity=='Minor Injury':
        severity=0
    elif severity=='Adverse Injury':
        severity=1
    else:
        severity=2

    if gender=='Female':
        gender=0
    else:
        gender =1

    result=rf_classifier.predict([[age,type_injury,location,reason,bool_fall_risk,severity,gender]])
    if result ==0:
        return 'High Risk'
    elif result == 1:
        return 'Low Risk'
    else :
        return 'Moderate Risk'



def display_file(path):
    df= pd.read_csv(path)
    df['Pressure'] = df['Pressure'].replace([0,1,2], ['Low Pressure', 'Moderate Pressure','High Pressure'])
    df['Accelerometer'] = df['Accelerometer'].replace([0,1], ['Less Than +-3g', 'Greater than +-3g'])
    df['Decision '] = df['Decision '].replace([0,1,2], ['No Fall', 'Chances of Slip/Fumble','Definate Fall'])
    st.info("Dataset")
    AgGrid(df.head())
        

def main():
    logo = ['Compunnel-Digital-Logo.png','Sunrise_Senior_Living_New_Logo.jpg']

    col1 , col2= st.sidebar.columns(2)

    cd= 'Compunnel-Digital-Logo.png'
    col1.image(cd,use_column_width=True)

    sr = 'Sunrise_Senior_Living_New_Logo-removebg-preview.png'
    col2.image(sr)


    st.sidebar.title('''**Fall Prediction**''')

    upload_files = st.sidebar.file_uploader("Upload Data File",type=['csv'],accept_multiple_files=True)
    file_name=[]
    for i in upload_files:
        file_name.append(i.name)

    file_option=st.sidebar.selectbox("Select the file name",file_name)

    
    if upload_files:


        selection = option_menu(
            menu_title="",
            options=["Home","Prediction","Vizualization"],
            icons=["house","","clipboard-data"],
            orientation="horizontal"
        )

    if file_option=="cStick (1).csv":
        if selection=="Home":
            display_file("cStick (1).csv")
        if selection=="Prediction":
           
            dist=st.number_input("Enter the distance")     
            pressure=st.selectbox("Blood Pressure",('Low Blood Pressure','Medium Level Blood Pressure','High Blood Pressure'))       
            hrv=st.number_input("Enter Heart Rate Variability(HRV)")
            sugar_level=st.number_input("Enter Sugar Level")
            spo2=st.slider('Enter SpO2 level', 0,100,80)
            acc=st.selectbox('Select Accelerometer range',("Less Than +-3g","Greater Than +-3g"))

            col1, col2, col3,col4,col5,col6,col7,col8,col9 = st.columns(9)
            if col5.button('Predict'):
                result = svm_predict(dist,pressure,hrv,sugar_level,spo2,acc)

                if result =="Not fall":
                    st.success('The person will {}'.format(result) )
                elif result =="may slip/trip/fumble":
                    st.warning('The person will {}'.format(result))
                else:
                    st.error('The person will {}'.format(result))

        if selection=="Vizualization":
            st.info('PowerBI Dashboard')
            st.markdown('<iframe title="Senior Livings Analytics - Page 1" width="800" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiN2E3MjExMTUtZWQ2ZS00OWU3LWI3OWEtODU5NTViOWI1MmU5IiwidCI6ImE2MTdlYzYwLTBhYjMtNDBiZS05MjhmLWJmMzY1MzA4NDkxYSIsImMiOjF9" frameborder="0" allowFullScreen="true"></iframe>',unsafe_allow_html=True)
            # Dashboard= IFrame(src="https://app.powerbi.com/view?r=eyJrIjoiN2E3MjExMTUtZWQ2ZS00OWU3LWI3OWEtODU5NTViOWI1MmU5IiwidCI6ImE2MTdlYzYwLTBhYjMtNDBiZS05MjhmLWJmMzY1MzA4NDkxYSIsImMiOjF9&pageName=ReportSection",width=1000,height=600)

    if file_option=="data.csv":
        if selection=="Home":
            display_file("data.csv")
        if selection=="Prediction":
            gender=st.radio('Select Gender',('Male','Female'))
            age=st.selectbox("Select Age Range",('Less than 1year','1yr-13yr','14yr-20yr','21yr-30yr','31yr-40yr','41yr-50yr','51yr - 60yr','61yr - 70yr','71yr - 80yr','81yr - 90yr','90yr above'))
            type_injury=st.selectbox("Select the type of Injury occured",('Bruising','Cut','Edema','Excoriation','Fracture','Head Trauma','Hematoma','Spinal Cord Injury','No Injury'))
            location=st.selectbox("Select the location in which injury took place",('Waiting room', 'Room', 'Bathroom/shower', 'Hallway','Recovery room ', 'Others', 'Medication room', 'Exam room','Outpatient adverse event', 'Surgical table', 'Medical office','Surgical prep adverse event', 'Triage adverse event','Vaccination room', 'Operating room', 'Nursing station'))
            reason=st.selectbox('Reason for Incident',('Loss of balance', 'Mental confusion', 'Slip','Hypotension', 'Paralysis', 'Unconciousness/Faint', 'Dizziness','Muscle weakness', 'Equipment', 'Human error', 'Sedation','Mental confusion '))
            bool_fall_risk=st.radio('Select if any involvement of medication with fall risk',('Yes','No'))
            severity=st.select_slider('Select Severity of incident',('Minor Injury','Adverse Injury','Serious Injury'))

            col1, col2, col3,col4,col5,col6,col7,col8,col9 = st.columns(9)
            if col5.button('Check'):
                result=rf_predict(age,type_injury,location,reason,bool_fall_risk,severity,gender)
                if result=='High Risk':
                    st.error(result)
                elif result=='Low Risk':
                    st.success(result)
                else:
                    st.warning(result)
                      

        if selection=="Vizualization":
            st.markdown('<iframe title="powerbi-data-report-12 - Page 1" width="800" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiZDM1ZGFjZGQtNjZkZS00MWMxLTk4M2EtMTFiYTlkNDdjZjg2IiwidCI6ImE2MTdlYzYwLTBhYjMtNDBiZS05MjhmLWJmMzY1MzA4NDkxYSIsImMiOjF9" frameborder="0" allowFullScreen="true"></iframe>',unsafe_allow_html=True)


        
        
   



if __name__=='__main__':
    main()
