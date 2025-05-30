import streamlit as st
import pandas as pd
import altair as alt
import os

# Load the data
df = pd.read_csv('floor_plan_comparisons.csv')

# Sidebar filters
st.sidebar.title("🏢 Filter Floor Plans")
projects = df["Project"].unique()
selected_projects = st.sidebar.multiselect("Select Projects", projects, default=projects)

floors = df["Floor"].unique()
selected_floors = st.sidebar.multiselect("Select Floors", floors, default=floors)

# Filtered dataframe
filtered_df = df[df["Project"].isin(selected_projects) & df["Floor"].isin(selected_floors)]

# Title
st.title("📊 Floor Plan Comparison Dashboard")

# Show filtered data
# Floor Plan Images - Side by Side
st.subheader("🖼️ Floor Plan Images")

for floor in selected_floors:
    st.markdown(f"### Floor: {floor}")
    
    cols = st.columns(len(selected_projects))  # One column per project

    for i, project in enumerate(selected_projects):
        filename = f"{project.lower().replace(' ', '_')}_{floor.lower().replace(' ', '')}.jpg"
        filepath = os.path.join("floorplans", filename)

        with cols[i]:
            st.markdown(f"**{project}**")
            if os.path.exists(filepath):
                st.image(filepath, use_container_width=True)
            else:
                st.warning("Image not found")


st.subheader("📋 Filtered Floor Plan Details")
st.dataframe(filtered_df)

# Total Area by Project
st.subheader("🏠 Total Built-up Area by Project")
total_area = filtered_df.groupby("Project")["Area (sqft)"].sum().reset_index()

bar_chart = alt.Chart(total_area).mark_bar().encode(
    x=alt.X("Project:N", sort="-y"),
    y="Area (sqft):Q",
    tooltip=["Project", "Area (sqft)"],
    color="Project:N"
).properties(width=700, height=400)

st.altair_chart(bar_chart)

# Room-wise area comparison
st.subheader("📐 Room Area Comparison")
room_chart = alt.Chart(filtered_df).mark_bar().encode(
    x="Room Name:N",
    y="Area (sqft):Q",
    color="Project:N",
    tooltip=["Project", "Room Name", "Area (sqft)"]
).properties(width=800).interactive()

st.altair_chart(room_chart)

# Download CSV
st.download_button(
    label="⬇️ Download Filtered CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_floor_plans.csv",
    mime="text/csv"
)
