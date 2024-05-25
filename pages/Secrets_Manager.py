import streamlit as st

from secrets_manager_svc import list_secrets, AWS_SM_CUSTOM_ENDPOINT_URL, upsert_secret, delete_secret, \
    describe_secret, get_secret_value

st.text_input(label="Configured AWS services endpoint url for Secrets Manager",
              placeholder=AWS_SM_CUSTOM_ENDPOINT_URL,
              help="""
                This is the endpoint the application will use to contact AWS. 
                Change it by setting AWS_SM_CUSTOM_ENDPOINT_URL envinronment variable
              """,
              disabled=True)


@st.experimental_dialog(title="Uspert Secret", width="large")
def upsert_dialog():
    with st.form("upsert_form", clear_on_submit=True, border=False):
        st.info(
            "What does Upsert mean?\n Add a secret, if a secret with the same secret \
            id is already present then updates it",
            icon="🙋‍♂️")
        secret_id = st.text_input(label="Secret Id",
                                  help="The identifier of the secret, if it already exists in the \
                                  secrets manager it will be updated")
        secret_value = st.text_input(label="Secret Value",
                                     help="The value of the secret, if a secret with the above secret id \
                                     already exists in the secrets manager this value will replace the existing one")
        if st.form_submit_button("Upsert secret"):
            upsert_secret(secret_id, secret_value)
            st.session_state["success_notification"] = f"Secret with id {secret_id} successfully upserted!"
            st.rerun()


@st.experimental_dialog("Secret Detail", width="large")
def detail_dialog(secret_id: str):
    st.markdown("### Secret Details")
    secret_detail = describe_secret(secret_id)
    st.write(secret_detail)


@st.experimental_dialog("Secret Value", width="large")
def secret_value_dialog(secret_id: str):
    st.markdown("### Secret Value")
    secret_value = get_secret_value(secret_id)
    st.write(secret_value)


def delete_secret_handler(secret_id: str):
    delete_secret(secret_id)


if "success_notification" in st.session_state:
    st.success(st.session_state["success_notification"], icon="✅")
    del st.session_state["success_notification"]

if "error_notification" in st.session_state:
    st.error(st.session_state["error_notification"])
    del st.session_state["error_notification"]

st.title("Secrets Manager")

if st.button("Upsert secret", use_container_width=True):
    upsert_dialog()

secrets_ids = list(map(lambda s: s.get("Name"), list_secrets().get("SecretList")))
st.markdown("""
---
### Secret Ids List
""")
if not secrets_ids:
    st.info("Your secrets manager is empty", icon="🥞")
for s_id in secrets_ids:
    st.markdown(f"- {s_id}")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("View Value", key=f"value_{s_id}", use_container_width=True):
            secret_value_dialog(s_id)
    with c2:
        st.button("Delete", key=f"delete_{s_id}", use_container_width=True, on_click=delete_secret_handler,
                  args=(s_id,))
    with c3:
        if st.button("Detail", key=f"detail_{s_id}", use_container_width=True):
            detail_dialog(s_id)
