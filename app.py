import streamlit as st
st.set_page_config(layout="wide")

from multiapp import MultiApp
# import apps here
import reference
# comment placeholder
import pyvis1

st.markdown('<style>' + open('assets/custom.css').read() + '</style>', unsafe_allow_html=True)

# initiate multiple app sidebar interface
app = MultiApp()

# add apps here, order matters
app.add_app("Pyvis", pyvis1.app)
app.add_app("Reference", reference.app)

with st.sidebar.expander("Feeling Philanthropic?"):
    st.caption("Feeling Philanthropic? Currently need $90 a month for website maintenance and API calls. Any amount helps, thank you! :blush:")
    st.image("QR Code.png")
    st.write("https://www.paypal.com/donate/?business=7AM8CH6ASCVRJ&no_recurring=0&item_name=About+40+dollars+a+month+for+website+maintenance+and+50+dollars+a+month+for+API+calls.&currency_code=USD")

# run apps
app.run()