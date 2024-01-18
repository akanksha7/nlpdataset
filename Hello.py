import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from shapely.geometry import Point
from streamlit_folium import st_folium
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pathlib

code_dir = pathlib.Path(__file__).parent.resolve()

# Constants
countries = ["Algeria", "Bahrain", "Egypt", "Iraq", "Jordan", "Kuwait", "Libya", "Morocco", "Mauritania", "Oman",
             "Palestine", "Qatar", "Saudi Arabia", "Sudan", "Syria", "Tunisia", "UAE", "Yemen"]



# Load the main dataset
@st.cache_resource
def load_df():
    data = {
        'ID': countries,
        'Icon_ID': list(range(len(countries))),
        'Icon_Size': [30] * len(countries),
        'Opacity': [1] * len(countries),
        'Latitude': [28.0339, 25.9304, 26.8206, 33.2232, 31.9522, 29.3759, 26.3351, 31.7917, 20.3484, 21.4735, 31.9522,
                     25.2769, 23.8859, 12.8628, 33.8869, 33.8869, 23.6345, 15.5524],
        'Longitude': [1.6596, 50.6378, 30.8025, 43.6793, 35.9450, 47.9774, 17.2283, -7.0926, -10.4614, 55.9754, 35.2332,
                      51.5200, 45.0792, 30.2176, 36.8248, 9.5375, 53.6660, 48.5164],
    }
    df = pd.DataFrame(data)
    return df


# Initialize the map
@st.cache_resource
def init_map(center=(23.78, 40.61), zoom_start=3, map_type="Cartodb dark_matter"):
    return folium.Map(location=center, zoom_start=zoom_start, tiles=map_type)


# Create a GeoDataFrame from the given DataFrame
@st.cache_resource
def create_point_map(df):
    df[['Latitude', 'Longitude']] = df[['Latitude', 'Longitude']].apply(pd.to_numeric, errors='coerce')
    df['coordinates'] = df[['Latitude', 'Longitude']].apply(Point, axis=1)
    df = gpd.GeoDataFrame(df, geometry='coordinates')
    df = df.dropna(subset=['Latitude', 'Longitude', 'coordinates'])
    return df


# Plot markers on the map

# def plot_from_df(df, folium_map):
#     df = create_point_map(df)
#     marker_path = code_dir / "workspaces" / "nlpdataset" / "marker.png"
#     for _, row in df.iterrows():
#         icon = folium.features.CustomIcon(marker_path, icon_size=(14, 14,))
#         marker = folium.Marker([row.Latitude, row.Longitude],
#                               tooltip=f'{row.ID}',
#                               opacity=row.Opacity,
#                               icon=icon)

#         marker.add_to(folium_map)
#     return folium_map
def plot_from_df(df, folium_map):
    df = create_point_map(df)
    marker_path = str(code_dir / "marker.png")  # Convert PosixPath to string
    for _, row in df.iterrows():
        icon = folium.features.CustomIcon(marker_path, icon_size=(14, 14,))
        marker = folium.Marker([row.Latitude, row.Longitude],
                              tooltip=f'{row.ID}',
                              opacity=row.Opacity,
                              icon=icon)
        marker.add_to(folium_map)
    return folium_map


# Load the initial map
@st.cache_resource
def load_map():
    m = init_map()
    df = load_df()
    m = plot_from_df(df, m)
    return m


# Load country-specific data
@st.cache_resource
def load_country_data(country):
    file_path = str(code_dir / "datasets" / f"{country.lower()}.csv")
    # file_path = f'/workspaces/nlpdataset/datasets/{country.lower()}.csv'
    data = pd.read_csv(file_path, nrows= 20000)
    return data
 

# Main function
def main():
    # Set page configuration
    st.set_page_config(layout='wide')

    # Header section
    header_right, _ = st.columns((2, 1))
    with header_right:
        st.title("Summarization Dataset")

    # Visualization and Download tabs
    tab1, tab2 = st.tabs(["VISUALIZATION", "DOWNLOAD"])

    # VISUALIZATION tab
    with tab1:
        left_col_v, right_col_v = st.columns((1, 2), gap="large")
        with left_col_v:
            
            m = load_map()
            level1_map_data = st_folium(m, height=400, width=600)

        with right_col_v:
            country_data = None
            if level1_map_data['last_object_clicked_tooltip'] is not None:
                selected_country = level1_map_data['last_object_clicked_tooltip']
            else:
                selected_country = "Algeria"

            if selected_country in countries:
                country_data = load_country_data(selected_country)
                country_data.rename(columns={'Coverage_first_sen_sum': 'Coverage', 'Density_first_sen_sum': 'Density'},
                                    inplace=True)
            else:
                st.warning("Invalid country selected.")
                return
            st.scatter_chart(country_data, x='Coverage', y='Density')
            st.write(f'<div style="text-align: center;"><b>Country :</b> {selected_country}</div>', unsafe_allow_html=True)

    # DOWNLOAD tab
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
                form =  st.form("form", clear_on_submit=False)
                with form:
                    name = st.text_input(label="Name",placeholder="Enter Full Name")
                    email = st.text_input(label="Email",placeholder="Enter Email Address")
                    org = st.text_input(label="Organization",placeholder="Organization Name")
                 
                    with st.expander("Terms of Use"):
                        st.write("""
                            This Dataset Usage Agreement ("Agreement") is a legal agreement with the Virginia Teach Team for the Dataset made available to the individual or entity ("Researcher") exercising rights under this Agreement. "Dataset" includes all text, data, information, source code, and any related materials, documentation, files, media, updates or revisions.

                            The Dataset is intended for non-commercial research and educational purposes only, and is made available free of charge without extending any license or other intellectual property rights. By downloading or using the Dataset, the Researcher acknowledges that they agree to the terms in this Agreement, and represent and warrant that they have authority to do so on behalf of any entity exercising rights under this Agreement. The Researcher accepts and agrees to be bound by the terms and conditions of this Agreement. If the Researcher does not agree to this Agreement, they may not download or use the Dataset.

                            By sharing content with Newsroom, such as by submitting content to this site or by corresponding with Newsroom contributors, the Researcher grants Newsroom the right to use, reproduce, display, perform, adapt, modify, distribute, have distributed, and promote the content in any form, anywhere and for any purpose, such as for evaluating and comparing summarization systems. Nothing in this Agreement shall obligate Newsroom to provide any support for the Dataset. Any feedback, suggestions, ideas, comments, improvements given by the Researcher related to the Dataset is voluntarily given, and may be used by Newsroom without obligation or restriction of any kind.

                            The Researcher accepts full responsibility for their use of the Dataset and shall defend indemnify, and hold harmless Newsroom, including their employees, trustees, officers, and agents, against any and all claims arising from the Researcher's use of the Dataset. The Researcher agrees to comply with all laws and regulations as they relate to access to and use of the Dataset and Service including U.S. export jurisdiction and other U.S. and international regulations.

                             THE DATASET IS PROVIDED "AS IS." NEWSROOM DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. WITHOUT LIMITATION OF THE ABOVE, NEWSROOM DISCLAIMS ANY WARRANTY THAT DATASET IS BUG OR ERROR-FREE, AND GRANTS NO WARRANTY REGARDING ITS USE OR THE RESULTS THEREFROM INCLUDING, WITHOUT LIMITATION, ITS CORRECTNESS, ACCURACY, OR RELIABILITY. THE DATASET IS NOT WARRANTIED TO FULFILL ANY PARTICULAR PURPOSES OR NEEDS.

                            TO THE EXTENT NOT PROHIBITED BY LAW, IN NO EVENT SHALL NEWSROOM BE LIABLE FOR ANY LOSS, DAMAGE OR INJURY, DIRECT AND INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES, HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER FOR BREACH OF CONTRACT, TORT (INCLUDING NEGLIGENCE) OR OTHERWISE, ARISING OUT OF THIS AGREEMENT, INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. THESE LIMITATIONS SHALL APPLY NOTWITHSTANDING ANY FAILURE OF ESSENTIAL PURPOSE OF ANY LIMITED REMEDY.

                            This Agreement is effective until terminated. Newsroom reserves the right to terminate the Researcher's access to the Dataset at any time. If the Researcher breaches this Agreement, the Researcher's rights to use the Dataset shall terminate automatically. The Researcher will immediately cease all use and distribution of the Dataset and destroy any copies or portions of the Dataset in their possession.

                            This Agreement is governed by the laws of the State of New York, without regard to conflict of law principles. All terms and provisions of this Agreement shall, if possible, be construed in a manner which makes them valid, but in the event any term or provision of this Agreement is found by a court of competent jurisdiction to be illegal or unenforceable, the validity or enforceability of the remainder of this Agreement shall not be affected.

                            This Agreement is the complete and exclusive agreement between the parties with respect to its subject matter and supersedes all prior or contemporaneous oral or written agreements or understandings relating to the subject matter.
                                                            """)
                    terms = st.checkbox(label="I agree to the terms of use",value=False) 
                    
                    submit = st.form_submit_button(label="Submit")


                    sender = 'akanksha.singh0710@gmail.com'
                    receiver = 'akanksha.singh0710@gmail.com'
                    if submit:
                        if name == '' or org == '' or email =='':
                            st.error("All fields are required")
                            return
                        if terms == False:
                            st.error("Please accept the terms of use")
                            return
                        try:
                            msg = MIMEMultipart()
                            msg['From'] = sender
                            msg['To'] = receiver
                            msg['Subject'] =  "NLP dataset request"
                            
                            message_body = f'''
                                <p>Hello,</p>
                                <p>This is a request for the NLP dataset. Below are the details:</p>
                                <p>Email: {email}</p>
                                <p>Name: {name}</p>
                                <p>Organization: {org}</p>
                                '''
                            messageText = MIMEText(message_body,'html')
                            msg.attach(messageText)
                            
                            server = smtplib.SMTP('smtp.gmail.com:587')
                            server.ehlo('Gmail')
                            server.starttls()
                            password = 'rqdx jcoi nnwv hrdm'

                            server.login(sender, password)
                            server.sendmail(sender, receiver, msg.as_string())
                            server.quit()
                            st.success('Email sent successfully! ')
                        except Exception as e:
                            st.error(f"Error while sending e-mail : {e}")
        
    

            with right_column:
                st.markdown("<h4 style='text-align: center;'>FORMAT</h4>", unsafe_allow_html=True)
                st.write("##")
                st.write(
                    """
                Summarization dataset contains three large files for training, development, and released test sets. Each of these files uses the compressed JSON line format. Each line is an object representing a single article-summary pair. An example summary object:

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



if __name__ == "__main__":
    main()

