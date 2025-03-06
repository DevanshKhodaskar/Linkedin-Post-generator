import streamlit as st 

from few_shots import load_posts
def main():
    st.title("LinkedIn post Generator")
    col1 ,col2 ,col3 = st.columns(3)
    with col1:
        df_posts, unique_tags = load_posts()
        st.selectbox("Title",options = unique_tags.get_tags())
                





if __name__ == '__main__':
    main()