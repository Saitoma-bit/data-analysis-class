# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# set config page

st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="👤",
    layout="wide"
) 

@st.cache_data  # => this is called decorator 
def load_data():
    try:
        df = pd.read_csv("data/employee_cleaned_data.csv")
       #st.success("Employee dataset load successfully.")
        return df
    except FileNotFoundError as e:
        st.warning(f"An error occured: {e}")

def create_sidebar_filters(df):
    st.sidebar.header("Employee Filters")

    department = st.sidebar.multiselect(
        "Select Department(s)",
        options=df["Department"].unique(),
        default=df["Department"].unique()
    )

    location = st.sidebar.multiselect(
        "Select Office Location(s)",
        options=df["office_location"].unique(),
        default=df["office_location"].unique()
    )

    remote = st.sidebar.radio(
        "Select Remote", 
        options=["All", "Yes", "No"],
        index=0
    )

    return department, location, remote

def filter_data(df, department, location, remote):
  filtered_df = df[df["Department"].isin(department) & df["office_location"].isin(location)]
  if remote != "All":
      filtered_df = filtered_df[filtered_df["Remote"] == remote]
  return filtered_df


def display_metrics(filtered_df):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
      st.metric("👤 Total Employee", len(filtered_df))

    with col2:
      avg_salary = filtered_df['Salary'].mean() if len(filtered_df) > 0 else 0
      st.metric("💲 Average Salary", f"${avg_salary:,.2f}")

    with col3:
      avg_performance = filtered_df['Performance'].mean() if len(filtered_df) > 0 else 0
      st.metric("📊 Average Performance", f"{avg_performance:.2f}")

    with col4:
      remote_pct = (filtered_df['Remote'] == 'Yes').sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
      st.metric("👤 Remote Worker", f"{remote_pct:.1f}%")



def display_charts(filtered_df):
   
   if len(filtered_df) ==0:
      st.warning("No filter data to display. please adjust the data from the sidebar")
      return
      
   col1, col2 = st.columns(2)

   with col1: 
      st.subheader("Employees Distribution By Department")
      dept_count = filtered_df["Department"].value_counts()
      fig1 =px.pie(
         values=dept_count.values,
         names=dept_count.index,
         hole=0.4
      )
      st.plotly_chart(fig1, width="stretch")

   with col2:
      st.subheader("Average Salary by Department")
      avg_salary = filtered_df.groupby("Department")["Salary"].mean().sort_values(ascending=False)
      fig2 = px.bar(
         x=avg_salary.values,
         y=avg_salary.index,
      )
      fig2.update_layout(
         xaxis_title="Salary",
         yaxis_title="Finance"
      )
      st.plotly_chart(fig2, width="stretch")
   
   col3, col4 = st.columns(2)

   with col3:
      st.subheader("Performance Distribution")
      fig3 = px.histogram(
         filtered_df, x="Performance", nbins=6
      )
      fig3.update_traces(
         marker_line_color="white",
         marker_line_width=1
      )
      fig3.update_layout(
         xaxis_title="Performance",
         yaxis_title="Count"
      )
      st.plotly_chart(fig3, width="stretch")

   with col4:
      st.subheader("Employee by location")
      location_count = filtered_df["office_location"].value_counts()
      fig4 = px.bar(
         x=location_count.index, 
         y=location_count.values
      )

      fig4.update_layout(
         xaxis_title="Office Location",
         yaxis_title = "Count"
      )

      st.plotly_chart(fig4, width="stretch")

def display_table_data(filtered_df):
   if len(filtered_df) > 0:
      st.dataframe(filtered_df, width="stretch", height=300)
   else:
      st.warning("No employee data to display")


def main():
  # load dataset
    df = load_data()

    #sidebar
    department, location, remote = create_sidebar_filters(df)

    #filtered_data
    filtered_df = filter_data(df, department, location, remote)


    st.title("Employee Dashboard")
    st.markdown("---")


    #display metrics
    display_metrics(filtered_df)

    #display chart
    st.markdown("---")
    display_charts(filtered_df)

    #display dataframe
    st.markdown("---")
    display_table_data(filtered_df)



main()
