
import streamlit as st
import requests

import smtplib
from email.mime.text import MIMEText
import streamlit.components.v1 as components


st.set_page_config(
        page_title="Download",
        page_icon=":floppy_disk:",
        layout="wide"
)


# def load_lottie_url(url):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# #----------LOAD ASSETs-------------------

# lottie_coding = load_lottie_url("https://lottie.host/89678da3-dcf7-40d9-842f-e7ea0086f77a/JwH2v6MU1d.json")

#----------HEADER-SECTION----------------
header_right, header_left = st.columns((2,1))

with header_right:
    st.title("Summarization Dataset")

with header_left:
    st_lottie(lottie_coding, height=150 ,key="coding")

tab1, tab2 = st.tabs(["VISUALIZATION","DOWNLOAD"]);

with tab1:
    left_col_v, right_col_v = st.columns((1,2), gap="large");
    countries = ["Algeria", "Bahrain", "Egypt", "Iraq", "Jordan", "Kuwait", "Libya", "Morocco","Muritania", "Oman", "Palestine", "Qatar", "Saudi Arabia", "Sudan", "Syria", "Tunisia", "UAE", "Yemen"]
    with left_col_v:
            option = st.selectbox(
   "Select Country",
   (countries),
   index=None,
   placeholder="Select country",
    )
    
    with right_col_v:
        html_temp = """<script type='module' src='https://prod-useast-b.online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js'></script><tableau-viz id='tableau-viz' src='https://prod-useast-b.online.tableau.com/t/nlpdataset/views/Kuwait/Sheet1' width='1470' height='689' hide-tabs toolbar='bottom' ></tableau-viz>"""
        components.html(html_temp, width=500, height=500)


with tab2:
    with st.container():
        left_column, right_column = st.columns((2,1), gap="large")
        with left_column:
            st.markdown("<h4 style='text-align: center;'>DOWNLOAD DATASET</h4>", unsafe_allow_html=True)
            st.write("##")
            st.write(
            """
            Downloading the complete data requires accepting the data licensing terms. Please submit the form here. 
            Shortly after filling the form and agreeing to the license you will receive a download link to the email you provided. 
            The download includes the complete training, development, and released test data splits.
            """
            )
            form =  st.form("form", clear_on_submit=True)
            with form:
                name = st.text_input(label="Name",placeholder="Enter Full Name")
                email = st.text_input(label="Email",placeholder="Enter Email Address")
                org = st.text_input(label="Organization",placeholder="Organization Name")
                terms = st.checkbox(label="I agree to the terms of use",value=False) 
                
                submit = st.form_submit_button(label="Submit")


                # email_sender = 
                if submit:
                    try:
                        msg = MIMEText(org)
                        msg['From'] = "email_sender"
                        msg['To'] = email
                        msg['Subject'] = form

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(email_sender, password)
                        server.sendmail(email_sender, email_receiver, msg.as_string())
                        server.quit()
                        st.success('Email sent successfully! 🚀')
                    except Exception as e:
                        st.error(f"Erreur lors de l’envoi de l’e-mail : {e}")
      
  

        with right_column:
            st.markdown("<h4 style='text-align: center;'>FORMAT</h4>", unsafe_allow_html=True)
            st.write("##")
            st.write(
                """
            CORNELL NEWSROOM contains three large files for training, development, and released test sets. Each of these files uses the compressed JSON line format. Each line is an object representing a single article-summary pair. An example summary object:

            """)
            st.json(
            {       
                "text": "...",
                "summary": "...",
                "title": "...",
                "archive": "http://...",
                "date": 20160302060024,
                "density": 1.25,
            "coverage": 0.75,
            "compression": 12.5,
            "compression_bin": "medium",
            "coverage_bin": "low",
            "density_bin": "abstractive"
            })
            st.write("""
            The date is an integer using the Internet Archive date format: YYYYMMDDHHMMSS. Density and coverage scores are provided for convenience, computed using the summary analysis tool also provided. Data subset and subsets by density, coverage, and compression are also provided. For example, in Python, each data file can be read as follows:

            import json, gz

            path = "train.jsonl.gz"
            data = []

            with gz.open(path) as f:
            for ln in f:
            obj = json.loads(ln)
            data.append(obj)
            """
                )

st.write("---")

#-------------FOOTER SECTION----------

# footer="""<style>
# a:link , a:visited{
# color: blue;
# background-color: transparent;
# text-decoration: underline;
# }

# a:hover,  a:active {
# color: red;
# background-color: transparent;
# text-decoration: underline;
# }

# .footer {
# position: fixed;
# left: 0;
# bottom: 0;
# width: 100%;
# background-color: #861f41;
# color: white;
# text-align: center;
# font-family:Inter;
# font-size:1reml;
# justify-content: space-around;
# }
# </style>
# <div class="footer">
# <p>@Copyright ...lllm</p>
# <p>link 1 | link 2 | link 3 | link 4</p>
# </div>
# """
# st.markdown(footer,unsafe_allow_html=True)


# if __name__ == "__main__":
#     run()
