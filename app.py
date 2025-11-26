import streamlit as st
import pandas as pd

# -------------------------------------------------------
# Initialize session storage
# -------------------------------------------------------
if "sites" not in st.session_state:
    st.session_state.sites = {}

st.title("CER Wage Tool")


# -------------------------------------------------------
# Internal scale interpreter (hidden)
# -------------------------------------------------------
def interpret_scale(scale_str):
    try:
        nums = [int(n.strip()) for n in scale_str.split("-")]
        if len(nums) < 3:
            return None

        values = [nums[0]]
        current = nums[0]
        i = 1
        steps = 0
        max_steps = 2000

        while i < len(nums) and steps < max_steps:
            inc = nums[i]
            end = nums[i + 1] if i + 1 < len(nums) else None

            if end is None:
                current += inc
                values.append(current)
                break

            while current < end:
                current += inc
                values.append(current)
                steps += 1
                if steps >= max_steps:
                    break

            i += 2

        return values

    except:
        return None


# -------------------------------------------------------
# 1. Transaction selection (first thing user sees)
# -------------------------------------------------------
st.subheader("Select Transaction Type")

transaction_types = [
    "Home to Home → Promotion",
    "Home to Home → New Joinee Wage",
    "Home to Home → Confirmation",
    "Home to Home → Probation",
    "Home to Host → Transfer",
]

transaction = st.selectbox("Choose transaction", transaction_types)


# -------------------------------------------------------
# 2. Choose site(s) depending on transaction type
# -------------------------------------------------------

sites = list(st.session_state.sites.keys())
need_two_sites = transaction.startswith("Home to Host")

st.markdown("---")
st.subheader("Select Sites")

# Home → Home
if not need_two_sites:

    if len(sites) > 0:
        home_site = st.selectbox("Select Site", ["Add new site"] + sites)
    else:
        home_site = "Add new site"

    # If user chooses to add a site
    if home_site == "Add new site":
        st.markdown("### Add New Site")
        site_name = st.text_input("Site Name")

        upload_file = st.file_uploader(
            "Upload combined Excel (Sheet1=Employees, Sheet2=LTS)", type=["xlsx"]
        )

        if st.button("Save Site"):
            if site_name == "":
                st.error("Please enter a site name.")
            elif upload_file is None:
                st.error("Please upload the Excel file.")
            else:
                try:
                    xls = pd.ExcelFile(upload_file)
                    emp_df = pd.read_excel(xls, xls.sheet_names[0])
                    wage_df = pd.read_excel(xls, xls.sheet_names[1])

                    st.session_state.sites[site_name] = {
                        "employees": emp_df,
                        "wages": wage_df,
                    }
                    st.success(f"Site '{site_name}' saved successfully.")

                except Exception as e:
                    st.error(f"Error reading Excel file: {e}")

    else:
        st.success(f"Selected Site: {home_site}")


# Home → Host (Transfer)
else:
    st.write("Home → Host Transfer")

    # Select home site
    home_site = st.selectbox("Home Site", ["Add new site"] + sites)

    # Select host site
    host_site = st.selectbox("Host Site", ["Add new site"] + sites, key="host_site_select")

    for label, chosen in [("Home Site", home_site), ("Host Site", host_site)]:
        if chosen == "Add new site":
            st.markdown(f"### Add {label}")
            site_name = st.text_input(f"{label} Name", key=label)

            upload_file = st.file_uploader(
                f"Upload Excel for {label} (Sheet1=Employees, Sheet2=LTS)",
                type=["xlsx"],
                key=f"{label}_excel",
            )

            if st.button(f"Save {label}"):
                if site_name == "":
                    st.error("Please enter a site name.")
                elif upload_file is None:
                    st.error("Please upload the Excel file.")
                else:
                    try:
                        xls = pd.ExcelFile(upload_file)
                        emp_df = pd.read_excel(xls, xls.sheet_names[0])
                        wage_df = pd.read_excel(xls, xls.sheet_names[1])

                        st.session_state.sites[site_name] = {
                            "employees": emp_df,
                            "wages": wage_df,
                        }
                        st.success(f"{label} '{site_name}' saved successfully.")
                    except Exception as e:
                        st.error(f"Error reading Excel file: {e}")

    if home_site != "Add new site" and host_site != "Add new site":
        st.success(f"Selected Home: {home_site} → Host: {host_site}")


st.markdown("---")
st.info("UI ready. Next we will integrate wage logic for each transaction.")
