import streamlit as st

def intro():
    import streamlit as st

    st.write("# Welcome to Carbon RKayd! 👋")
    st.sidebar.success("Select the Option.")

    st.markdown(
        """
        This is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select a Option from the dropdown on the left**

       
    """
    )

def Data_Dictionary_Comparing():

    from collections import defaultdict
    from pathlib import Path
    import sqlite3

    #import openpyxl

    import streamlit as st
    import altair as alt
    import pandas as pd

    from io import StringIO
    from io import BytesIO



    Otput_Final = 'Whizard_compar\\2017-P Empire Distr\\output_Final_R06'

    # -----------------------------------------------------------------------------


    # -----------------------------------------------------------------------------
    st.write("# Welcome to Carbon RKayd! 👋")
    st.markdown(
            """
            **👈 Select a Input Logix Data Dictionary from the dropdown on the below to compare the revised Logix Data Dictionary.

           
        """
        )

    st.markdown(
         """
                

                ### Choose a Logix Data Dictionary Old Input File
         """

               
            )
    Intput_File_old = st.file_uploader("")
    if Intput_File_old is not None:   
        Input_old = pd.read_excel(Intput_File_old,sheet_name="WHizard Data Dict",skiprows=5)
        
        #st.write(Assets_Input) 
    
    st.markdown(
         """
                

                ### Choose a Logix Data Dictionary New Input File
         """

               
            )

    Intput_File_new = st.file_uploader(" ")
    if Intput_File_new is not None:
        Input_new = pd.read_excel(Intput_File_new,sheet_name="WHizard Data Dict",skiprows=5)


        data_Final=Input_old.compare(Input_new,keep_shape=True, keep_equal=False)
        data_Final.insert(0,'name_Old','')
        data_Final["name_Old"]= Input_old["Conveyor/ Device Name"]
        data_Final.insert(1,'name_New','')
        data_Final["name_New"]= Input_new["Conveyor/ Device Name"]
        #data_Final.to_excel(Otput_Final)
        #test

        #Assets_File.name = "Output_"+Assets_File.name
        flnme =  Otput_Final
            #flnme = st.text_input('Enter Excel file name (e.g. email_data.xlsx)')
        if flnme != "":
            if flnme.endswith(".xlsx") == False:  # add file extension if it is forgotten
                flnme = flnme + ".xlsx"
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                data_Final.to_excel(writer, sheet_name='Sheet1')
        st.write("Output filename:", flnme)
        st.download_button(label="Download Excel workbook", data=buffer.getvalue(), file_name=flnme, mime="application/vnd.ms-excel")
            
 



def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from collections import defaultdict
    from pathlib import Path
    import sqlite3

    import streamlit as st
    import altair as alt
    import pandas as pd

    #import openpyxl

    from io import StringIO
    from io import BytesIO

    from urllib.error import URLError

    Otput_Final = 'Whizard_compar\\2017-P Empire Distr\\output_Final_R06'

    st.write("# Welcome to Carbon RKayd! 👋")
    st.markdown(
            """
            **👈 Select a Input File from the dropdown on the below .

           
        """
        )

    st.markdown(
         """
                

                ### Choose a IcoUnifiedConfig_Assets Input File
         """

               
            )
    Intput_File_old = st.file_uploader("")
    if Intput_File_old is not None:   
        Input_old = pd.read_excel(Intput_File_old,sheet_name="WHizard Data Dict",skiprows=5)
        
        #st.write(Assets_Input) 
    
    st.markdown(
         """
                

                ### Choose a IcoUnifiedConfig_AlarmWorX64 Server Input File
         """

               
            )

    Intput_File_new = st.file_uploader(" ")
    if Intput_File_new is not None:
        Input_new = pd.read_excel(Intput_File_new,sheet_name="WHizard Data Dict",skiprows=5)


        data_Final=Input_old.compare(Input_new,keep_shape=True, keep_equal=False)
        data_Final.insert(0,'name_Old','')
        data_Final["name_Old"]= Input_old["Conveyor/ Device Name"]
        data_Final.insert(1,'name_New','')
        data_Final["name_New"]= Input_new["Conveyor/ Device Name"]
        #data_Final.to_excel(Otput_Final)
        #test

        #Assets_File.name = "Output_"+Assets_File.name
        flnme =  Otput_Final
            #flnme = st.text_input('Enter Excel file name (e.g. email_data.xlsx)')
        if flnme != "":
            if flnme.endswith(".xlsx") == False:  # add file extension if it is forgotten
                flnme = flnme + ".xlsx"
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                data_Final.to_excel(writer, sheet_name='Sheet1')
        st.write("Output filename:", flnme)
        st.download_button(label="Download Excel workbook", data=buffer.getvalue(), file_name=flnme, mime="application/vnd.ms-excel")   

page_names_to_funcs = {
    "—": intro,
    "Data Dictionary Comparing": Data_Dictionary_Comparing,
    #"Mapping Demo": mapping_demo,
    "AlarmWorX Description Mapping ": data_frame_demo
}

demo_name = st.sidebar.selectbox("Choose a Options", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()