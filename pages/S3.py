import os.path
import sys

import streamlit as st
from botocore.exceptions import ClientError

sys.path.append("../localstack_gui")

from s3_svc import delete_object, get_object, list_buckets, write_object, list_objects, download_object, \
    create_bucket, delete_bucket, AWS_S3_CUSTOM_ENDPOINT_URL

st.text_input(label="Configured AWS services endpoint url for S3",
              placeholder=AWS_S3_CUSTOM_ENDPOINT_URL,
              help="""
                This is the endpoint the application will use to contact AWS. 
                Change it by setting AWS_S3_CUSTOM_ENDPOINT_URL envinronment variable
              """,
              disabled=True)


def delete_object_btn_handler(selected_bucket_name: str, object_key: str):
    print(f"to delete {object_key}")
    delete_object(selected_bucket_name, object_key)


@st.experimental_dialog(title="Object Details", width="large")
def detail_dialog(selected_bucket_name: str, object_key: str):
    print(f"details of {object_key}")
    get_object_result = get_object(selected_bucket_name, object_key)
    st.write(get_object_result)


def download_btn_handler(selected_bucket_name: str, object_key: str):
    output_file_folder = os.path.dirname(os.path.abspath(__file__))
    download_object(selected_bucket_name, object_key, os.path.join(output_file_folder, object_key))
    st.success(f"Download completed! File saved in {output_file_folder} folder", icon="✅")


@st.experimental_dialog(title="Upload object", width="large")
def upload_dialog():
    with st.form("upload_form", clear_on_submit=True, border=False):
        uploaded_file = st.file_uploader("Upload a file into the selected bucket")
        key_prefix = st.text_input(label="Enter the key prefix of the object (end with / character !)")
        if st.form_submit_button("Upload!"):
            bytes_data = uploaded_file.getvalue()
            write_object(selected_bucket, f"{key_prefix}{uploaded_file.name}", bytes_data)
            st.success("File uploaded, refresh to view the file!", icon="✅")


if "success_notification" in st.session_state:
    st.success(st.session_state["success_notification"], icon="✅")
    del st.session_state["success_notification"]

if "error_notification" in st.session_state:
    st.error(st.session_state["error_notification"])
    del st.session_state["error_notification"]

st.title("Buckets")

list_buckets_response = list_buckets()
bucket_names = list(map(lambda b: b.get("Name"), list_buckets_response))
selected_bucket = st.selectbox("Choose a bucket to see its content", bucket_names)

st.markdown("---")
st.markdown("### bucket content")

if selected_bucket:
    objects = list_objects(selected_bucket)
    for obj in objects:
        st.markdown(f"""- {obj.get("Key")}""")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            with st.popover("Download", use_container_width=True):
                with st.form(f"download_form_{obj.get("Key")}", clear_on_submit=True, border=False):
                    output_file_folder = os.path.dirname(os.path.abspath(__file__))
                    output_file_path = os.path.join(output_file_folder, obj.get("Key").split("/")[-1])
                    output_file_path = st.text_input(placeholder=f"output file: {output_file_path}", key=obj.get("Key"),
                                                     label="------------------------------Enter the file output path (the current project directory is the default)------------------------------")
                    if st.form_submit_button("Download!"):
                        download_object(selected_bucket, obj.get("Key"), output_file_path)
                        st.success(f"Download completed! File saved in {output_file_folder} folder", icon="✅")
        with c2:
            if st.button("Details", key=f"detail_{obj.get("Key")}", use_container_width=True):
                detail_dialog(selected_bucket, obj.get("Key"))
        with c3:
            st.button("Delete", on_click=delete_object_btn_handler, args=(selected_bucket, obj.get("Key"),),
                      key=f"delete_{obj.get("Key")}", use_container_width=True)

st.markdown("---")

if st.button("Upload into bucket", use_container_width=True):
    upload_dialog()

with st.popover("Create Bucket", use_container_width=True):
    with st.form("create_bucket_form", clear_on_submit=True, border=False):
        bucket_name = st.text_input(label="Bucket name")
        submitted = st.form_submit_button("Create It!")
        if submitted:
            create_bucket(bucket_name)
            st.session_state["success_notification"] = "Bucket created!"
            st.rerun()

if st.button(f"Delete bucket: {selected_bucket}", type="primary"):
    try:
        delete_bucket(selected_bucket)
        st.session_state["success_notification"] = "Bucket deleted!"
        st.rerun()
    except ClientError as c:
        st.session_state["success_notification"] = c.response.get("Error").get("Message")
