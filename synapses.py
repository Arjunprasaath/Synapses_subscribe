# Synapses subscription page.
# Initialisation
import streamlit as st
import pandas as pd
from gspread_pandas import Spread,Client
from google.oauth2 import service_account

# Default variables
spreadsheetname = "Synapses-data"
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope, creds=credentials)
spread = Spread(spreadsheetname, client = client)
sh = client.open(spreadsheetname)

# Get the sheet as dataframe
def load_sheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    print(df)
    return df

# Update to Sheet
def update_sheet(spreadsheetname, dataframe):
    col = ['name', 'email', 'status']
    spread.df_to_sheet(dataframe[col], sheet = spreadsheetname,index = False)
    st.sidebar.info('Details have been updated')

# Disables the input text boxes
def disable():
    st.session_state["disabled"] = True

# Updating the details submitted to the DB
def subscribe(a, b):
    if a!= "" and b!= '':
        st.balloons()
        print("second",a , b)
        new = {'name': [a], 'email' : [b], 'status': ['pending']} 
        new_df = pd.DataFrame(new)
        df = load_sheet('DB')
        new_df = pd.concat([df, new_df])
        update_sheet('DB', new_df)
        st.success("You are subscribed!:thumbsup: You can close this tab now.")
        disable()  

# Main function
def main(): 

    st.title("Synapses :link:")
    st.markdown("Welcome to the cutting-edge world of information with Synapse :link:, the trailblazing newsletter \
                crafted entirely by :red[artificial intelligence] :robot_face: . As the pioneering newsletter of its kind in \
                India, Synapse promises to deliver:")
    st.markdown("- :orange[a seamless fusion of the latest news] :newspaper:")
    st.markdown("- :blue[curated content] :mag:")
    # st.markdown("- :red[captivating insights] :star2:")
    st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        padding-left:20px;
        padding-up:0px;
    }
    </style>
    ''', unsafe_allow_html=True)

    st.markdown("all intelligently tailored by AI. :green[Join the new era of newsletters]")
    st.header(":violet[Subscribe] :orange[now!]")

    with st.form(key = "form"):

        if "disabled" not in st.session_state:
            st.session_state["disabled"] = False

        name = st.text_input("Name", max_chars = 20, placeholder = "eg. Dave", disabled = st.session_state.disabled)
        
        while name != '':
            if all(chr.isalpha() or chr.isspace() for chr in name):
                break
            else:
                st.error('Please type in a string ', icon="🚨")
                break

        email_id = st.text_input("Email ID", max_chars = 30, placeholder = "eg. dave@gmail.com", disabled = st.session_state.disabled)
        sub_button = st.form_submit_button("Subscribe!", type = "primary", on_click = disable)

    if sub_button:
        subscribe(name, email_id)

    st.divider()
    st.caption('By SAGI - Sustainable Artificial General Intelligence')

if __name__ == "__main__":
    main()