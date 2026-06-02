import streamlit as st
# if "count" not in st.session_state:
#     st.session_state["count"] = 1

# if st.button("カウントアップ"):
#     st.session_state["count"] = st.session_state["count"] + 1

# st.write(st.session_state["count"])

if "kibun_history" not in st.session_state:
    st.session_state["kibun_history"] = []

col1, col2, col3, col4= st.columns(4)

with col1:
    if st.button("嬉しい"):
        st.session_state["kibun_history"].append("嬉しい")

with col2:
    if st.button("悲しい😢"):
        st.session_state["kibun_history"].append("悲しい")

with col3:
    if st.button("眠い😪"):
        st.session_state["kibun_history"].append("眠い")

with col4:
    if st.button("お腹すいた🍕"):
        st.session_state["kibun_history"].append("腹すいた")

for kibn in st.session_state["kibun_history"]:
    st.write(kibn)