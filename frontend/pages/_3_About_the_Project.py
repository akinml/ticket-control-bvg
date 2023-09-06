import streamlit as st

# setting config to "wide" so that charts and other elements are properly displayed
st.set_page_config(layout="wide")

def page_3_about_project():
    st.title("Welcome to BVG Controls:wave:")

    # ###
    # Prediction: RandomForestClassifier, output 0 or 1 > control / no control
    st.header("About this Project", divider='rainbow')
    st.markdown("This is a study project for a Data Science bootcamp. \
             We are a team of enthusiasts interested in tackling unconventional challenges (:heart: dirty data :heart: complex APIs :heart:). \
                We do not seek to promote any illegal activity. We share a vision to promote \
                    Zero-Fare Public Transport in the context of Global Warming and increasing Inequality.\
                        Data used for this project has been scraped from a public Telegram Channel. \
                            We have not obtained personal data of users and are aligned with the General Data Protection Regulation.\
                                You can view our work on GitHub. \
                                Do not hesitate to contact us if you have any questions.", )


    st.header("Our Vision: Zero-Fare Public Transport", divider='rainbow')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.subheader("Community benefits")
        st.write("make the system more accessible and fair for low-income residents")
    with col2:
        st.subheader("Operational benefits")
        st.write("decrease congestion on road traffic, fewer traffic accidents, savings from reduced wear and tear on roads")
    with col3:
        st.subheader("Global benefits")
        st.write("zero-fare public transport could mitigate the problems of global warming and oil depletion")






# Main app
def main():
    page_3_about_project()



if __name__ == "__main__":
    main()
