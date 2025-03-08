import streamlit as st 
from post_generator import generate_post
from few_shots import load_posts,get_tags
def main():
    st.title("LinkedIn post Generator")
    col1 ,col2 ,col3 = st.columns(3)
    with col1:
        df_posts, unique_tags = load_posts()
        selected_tag =  st.selectbox("Title",options =get_tags())
    with col2:
        selected_length = st.selectbox("Length",options = ["Short","Medium","Long"])

    with col3:
        selected_language =  st.selectbox("Language",options = ["English","Hinglish"])
                

    if st.button("Generate Post"):
        st.write(f"Generating post for {selected_tag} tag with {selected_length} length in {selected_language} language")
        post = generate_post(selected_length,selected_language,selected_tag)
        st.write(post)




if __name__ == '__main__':
    main()