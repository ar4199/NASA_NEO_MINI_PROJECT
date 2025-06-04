import streamlit as st
import pandas as pd
import pymysql 
from datetime import date
st.title("🌏NASA ASTEROID DASHBOARD")

conn = pymysql.connect(host = '127.0.0.1', user='root',passwd='Arahim4199',database='NASA_NEO_PROJECT')
curs=conn.cursor()


with st.sidebar:
    st.title("ASTEROID APPROACHES")
    tab=st.radio("CHOOSE A SECTION",["FILTER CRITERIA","QUERIES"])


if tab== "QUERIES":
    st.title ("NASA ASTEROID TRACKER")
    
    queries = {'1.Count how many times each asteroid has approached Earth':
           '''select id, count(*) as approach_count
           from asteroid
           group by id
           order by approach_count desc''',
           '2.Average velocity of each asteroid over multiple approaches':
           '''select NEO_REF_ID, avg(relative_velocity) as average_velocity_kmph 
           from CLOSE_APPROACH_DATA 
           group by NEO_REF_ID 
           order by average_velocity_kmph ''',
           '3.List top 10 fastest asteroids':
           '''SELECT neo_ref_id, MAX(relative_velocity) AS max_velocity_kph 
           FROM close_approach_data 
           GROUP BY neo_ref_id 
           ORDER BY max_velocity_kph DESC 
           LIMIT 10''',
           '4.Find potentially hazardous asteroids that have approached Earth more than 3 times':
           '''select id, name, count(neo_ref_id)as approach_count
           from asteroid
           join CLOSE_APPROACH_DATA on id=NEO_REF_ID
           where is_hazardous = 1
           group by id, name
           having count(NEO_REF_ID)>3  ''',
           '5.Find the month with the most asteroid approaches':
           '''SELECT MONTH(CLOSE_APPROACH_DATE) AS approach_month,  COUNT(*) AS total_approaches
           FROM CLOSE_APPROACH_DATA
           GROUP BY approach_month
           ORDER BY total_approaches DESC
           LIMIT 1''',
           '6.Get the asteroid with the fastest ever approach speed':
           '''select neo_ref_id, name, max(relative_velocity) as maximum_velocity
           from CLOSE_APPROACH_DATA
           join ASTEROID on id= NEO_REF_ID
           group by NEO_REF_ID, NAME 
           order by maximum_velocity
           limit 100''',
           '7.Sort asteroids by maximum estimated diameter (descending)':
           '''select id, est_dia_max_km,name
           from asteroid
           order by est_dia_max_km desc''',
          '8.An asteroid whose closest approach is getting nearer over time':
           '''select neo_ref_id, name, CLOSE_APPROACH_DATE,miss_distance_km
           from CLOSE_APPROACH_DATA
           join ASTEROID on NEO_REF_ID=id
           order by NEO_REF_ID, MISS_DISTANCE_KM, CLOSE_APPROACH_DATE''',
          '9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth.':
           '''select name, CLOSE_APPROACH_DATE,MISS_DISTANCE_KM
           from CLOSE_APPROACH_DATA
           join ASTEROID on id= NEO_REF_ID''',
           '10.List names of asteroids that approached Earth with velocity > 50,000 km/h':
           '''select name, id, relative_velocity
           from ASTEROID
           join CLOSE_APPROACH_DATA on id=NEO_REF_ID
           where RELATIVE_VELOCITY>50000''',
           '11.Count how many approaches happened per month':
           '''select month(CLOSE_APPROACH_DATE) as month , count(*) as no_appearances
           from CLOSE_APPROACH_DATA
           group by month (CLOSE_APPROACH_DATE)
           order by month''',
           '12.Find asteroid with the highest brightness':
           '''select id, name, absolute_magnitude
           from asteroid
           order by absolute_magnitude asc
           limit 1''',
           '13.Get number of hazardous vs non-hazardous asteroids':
           '''select is_hazardous,count(*) as hazard_count
           from ASTEROID
           group by IS_HAZARDOUS''',
           '14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance.':
           '''select name,CLOSE_APPROACH_DATE,miss_distance_lunar
           from CLOSE_APPROACH_DATA
           join ASTEROID on id=NEO_REF_ID
           where MISS_DISTANCE_LUNAR<=1''',
          '15.Find asteroids that came within 0.05 AU':
           '''select neo_ref_id, astronomical
           from CLOSE_APPROACH_DATA
           where ASTRONOMICAL <=0.05
           order by ASTRONOMICAL asc''',
          }
    selected_query = st.selectbox("CHOOSE AN OPTION", list(queries.keys()))
    query = queries[selected_query]

    try:
        df = pd.read_sql(query, conn)
        st.subheader(selected_query)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error running query: {e}")


elif tab == "FILTER CRITERIA":
    st.sidebar.header("Filter Criteria")
    st.write("YOU CAN PUT YOUR FILTERS HERE")

    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("Start Date", date(2024, 1, 1))
    with col2:
        end_date = st.date_input("End Date", date(2025, 5, 1))
    with col3:
        hazardous = st.selectbox("Hazardous", ["All", "Hazardous Only", "Non-Hazardous"])
    col4, col5, col6 = st.columns(3)
    with col4:
        rel_vel = st.slider("Relative Velocity (km/h)", 1400, 17500, (1400, 17500))
    with col5:
        au_range = st.slider("Astronomical Distance (AU)", 0.0, 0.50, (0.00, 0.50))
    with col6:
        abs_mag = st.slider("Absolute Magnitude", 13.0, 35.0, (13.0, 35.0))

    col7, col8 = st.columns(2)
    with col7:
        dia_min = st.slider("Estimated Min Diameter (km)", 0.0, 5.0, (0.0, 5.0))
    with col8:
        dia_max = st.slider("Estimated Max Diameter (km)", 0.0, 11.0, (0.0, 11.0))


    f_query=f'''SELECT ID, NAME, ABSOLUTE_MAGNITUDE, EST_DIA_MIN_KM, EST_DIA_MAX_KM, IS_HAZARDOUS,
                          CLOSE_APPROACH_DATE, RELATIVE_VELOCITY, ASTRONOMICAL, MISS_DISTANCE_KM, MISS_DISTANCE_LUNAR, ORBITING_BODY
                FROM ASTEROID
                JOIN CLOSE_APPROACH_DATA ON id = NEO_REF_ID
                WHERE CLOSE_APPROACH_DATE BETWEEN '{start_date}' AND '{end_date}'
                AND RELATIVE_VELOCITY BETWEEN {rel_vel[0]} AND {rel_vel[1]}
                AND ASTRONOMICAL BETWEEN {au_range[0]} AND {au_range[1]}
                AND ABSOLUTE_MAGNITUDE BETWEEN {abs_mag[0]} AND {abs_mag[1]}
                AND EST_DIA_MAX_KM BETWEEN {dia_max[0]} AND {dia_max[1]}
                AND EST_DIA_MIN_KM BETWEEN {dia_min[0]} AND {dia_min[1]}'''
    if hazardous == "Hazardous Only":
        f_query += " AND IS_HAZARDOUS = 1"
    elif hazardous == "Non-Hazardous":
        f_query += " AND IS_HAZARDOUS = 0"
        
    try:
        df = pd.read_sql(f_query, conn)
        st.subheader("filtered results")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error running query: {e}")