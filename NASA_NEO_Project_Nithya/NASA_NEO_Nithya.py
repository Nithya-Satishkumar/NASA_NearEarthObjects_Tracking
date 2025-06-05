import streamlit as st
import pandas as pd
import pymysql
import datetime
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
st.header("🌌🪐 NASA - Near Earth Objects Tracking Application ☄️🚀 🌑")
st.markdown("<br>", unsafe_allow_html=True)

myconnection = pymysql.connect(
                host = "127.0.0.1",
                user="root",
                passwd="Aadhu#1207",
                database = "NEO")
cursor_NEO = myconnection.cursor()

### Using Option menu for Navigation

with st.sidebar:
    selection = option_menu("Asteroid Approaches", ["Filter Criteria", "Queries"],icons=['search', 'table'], menu_icon="cast", default_index=1)

### Below code will be execute if Filter Criteria is selected in sidebar ###

if selection == "Filter Criteria":
    
    st.markdown(''':rainbow-background[:violet[***Select the required range of values to display result***]] ''')
    st.markdown("<br>", unsafe_allow_html=True)
    ## Defining Page Layout with 3 columns ##
    
    col1,spacer,col2,spacer,col3 = st.columns([1, 0.2, 1,0.2,1]) 

    ### Range slider is used for allowing users to select a range of values for data display ###
    with col1:
        magnitude = st.slider("Minimum Magnitude",13.81,32.61,(13.81,32.61))
        minEstDia = st.slider("Minimum Estimated Diameter(Km)",0.00,4.62,(0.00,4.62))
        maxEstDia = st.slider("Maximum Estimated Diameter(Km)",0.00,10.30,(0.00,10.30))
        #startDate = st.date_input("Start Date",datetime.date(2024,1,1))
        button2=st.button("Filter 🧲")

    ### Hazard field has only two values . Hence selectbox is used ###
    with col2:
        velocity = st.slider("Relative Velocity Kmph",1418.00,173072.00,(1418.00,173072.00))
        astroUnit = st.slider("Astronomical Unit",0.00,0.50,(0.00,0.50))
        hazard = st.selectbox("Show Potentially Hazardous Asteroids",options=[0,1],index=0)
        #endDate = st.date_input("End Date",datetime.date(2025,4,13))

    ### Date picker is used for user friendly approach ###
    with col3:
        startDate = st.date_input("Start Date",datetime.date(2024,1,1))
        endDate = st.date_input("End Date",datetime.date(2025,4,13))

    ### If Filter button is clicked , below code will be executed ###
    
    if button2:
        query="""SELECT ast.name as NAME,ast.absolute_magnitude_h as MINIMUM_MAGNITUDE,
                ast.estimated_diameter_min_km as MINIMUM_ESTIMATED_DIAMETER_Km,
                ast.estimated_diameter_max_km as MAXIMUM_ESTIMATED_DIAMETER_Km,ast.is_potentially_hazardous_asteroid as HAZARD,
                cls.close_approach_date as CLOSE_APPROACH_DATE,cls.relative_velocity_kmph as RELATIVE_VELOCITY_Kmph,
                cls.astronomical as ASTRONOMICAL_UNITS,cls.miss_distance_km as MISS_DISTANCE_Km,
                cls.miss_distance_lunar as MISS_DISTANCE_LUNAR,cls.orbiting_body as ORBITING_BODY
                FROM asteroids ast,close_approach cls
                WHERE ast.id=cls.neo_reference_id
                AND ast.absolute_magnitude_h BETWEEN %s AND %s
                AND ast.estimated_diameter_min_km BETWEEN %s AND %s
                AND ast.estimated_diameter_max_km BETWEEN %s AND %s
                AND ast.is_potentially_hazardous_asteroid = %s
                AND cls.close_approach_date BETWEEN %s AND %s
                AND cls.relative_velocity_kmph BETWEEN %s AND %s
                AND cls.astronomical BETWEEN %s AND %s """
        
        params=[magnitude[0],magnitude[1],minEstDia[0],minEstDia[1],maxEstDia[0],maxEstDia[1],
                hazard,startDate,endDate,velocity[0],velocity[1],astroUnit[0],astroUnit[1]]
        print(query)
        print(params)
        cursor_NEO.execute(query,params)
        rows=cursor_NEO.fetchall()
        columns=[desc[0] for desc in cursor_NEO.description]
        data=pd.DataFrame(rows,columns=columns)
        st.subheader("☄️ Filtered Asteroids details 🌠")
        st.dataframe(data)
        

### Below code will be execute if Queries is selected in sidebar ###

if selection == "Queries":  
    options = st.selectbox("Choose a query",["1.Show how many times each asteroid has approached Earth",
                                    "2.Average velocity of each asteroid over multiple approaches",
                                    "3.List top 10 fastest asteroidsSort asteroids by maximum estimated diameter (descending)",
                                    "4.List of potentially hazardous asteroids that have approached Earth more than 3 times",
                                    "5.Display the month with the most asteroid approaches",
                                    "6.The asteroid with the fastest ever approach speed",
                                    "7.Sorted List of asteroids by maximum estimated diameter (descending)",
                                    "8.Display an asteroid whose closest approach is getting nearer over time",
                                    "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
                                    "10.List names of asteroids that approached Earth with velocity > 50,000 km/h",
                                    "11.Show how many approaches happened per month",
                                    "12.Display the asteroid with the highest brightness",
                                    "13.Get number of hazardous vs non-hazardous asteroids",
                                    "14.Show asteroids that passed closer than the Moon",
                                    "15.Show asteroids that came within 0.05 AU(Astronomical Units)",
                                    "16.List the asteroid size information",
                                    "17.List of approaches per day sorted from highest to lowest",
                                    "18.Asteroid with the minimum estimated diameter",
                                    "19.Show all the required information regarding potentially hazardous asteroid",
                                    "20.Information regarding the distance by which the asteroids missed hitting Earth",
                                    "21.Show the Average miss distance",
                                    "22.Display the Date with the highest number of approaches"],placeholder='Select an option...',index=None)

    button1=st.button("Show Query Result 🧪")

    ## Defining a function for fetching query results ####
    def query_result(query):
        cursor_NEO.execute(query)
        result = cursor_NEO.fetchall()
        columns = [desc[0] for desc in cursor_NEO.description]
        data = pd.DataFrame(result,columns=columns)
        st.dataframe(data) 

### After selecting the query , show the result only after button is clicked ###
    
    if options == "1.Show how many times each asteroid has approached Earth":
        if button1:
            query_result('select id,count(id) from asteroids group by id')

    elif options == "2.Average velocity of each asteroid over multiple approaches":
        if button1:
            query_result('select neo_reference_id,avg(relative_velocity_kmph) from close_approach group by neo_reference_id')

    elif options == "3.List top 10 fastest asteroidsSort asteroids by maximum estimated diameter (descending)":
        if button1:
            query_result('select neo_reference_id,relative_velocity_kmph from close_approach group by neo_reference_id,relative_velocity_kmph order by relative_velocity_kmph desc LIMIT 10')

    elif options == "4.List of potentially hazardous asteroids that have approached Earth more than 3 times":
        if button1:
            query_result("select neo_reference_id,count(neo_reference_id) as number_of_approaches from close_approach group by neo_reference_id having count(neo_reference_id) > '3' and neo_reference_id in (select id from asteroids where is_potentially_hazardous_asteroid = '1')")

    elif options == "5.Display the month with the most asteroid approaches":
        if button1:
            query_result("select  monthname(close_approach_date) as month,count(neo_reference_id) from close_approach group by close_approach_date order by count(neo_reference_id) desc LIMIT 1")

    elif options == "6.The asteroid with the fastest ever approach speed":
        if button1:
            query_result("select distinct neo_reference_id from close_approach where relative_velocity_kmph = (select max(relative_velocity_kmph) from close_approach)")

    elif options == "7.Sorted List of asteroids by maximum estimated diameter (descending)":
        if button1:
            query_result("select  distinct id,estimated_diameter_max_km from asteroids order by estimated_diameter_max_km desc")

    elif options == "8.Display an asteroid whose closest approach is getting nearer over time":
        if button1:
            query_result('select distinct neo_reference_id ,close_approach_date,miss_distance_km from close_approach order by miss_distance_km,close_approach_date desc limit 1')

    elif options == "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth":
        if button1:
            query_result('select distinct asteroids.name,close_approach.close_approach_date,close_approach.miss_distance_km from asteroids,close_approach where asteroids.id=close_approach.neo_reference_id order by close_approach_date desc')
 
    elif options == "10.List names of asteroids that approached Earth with velocity > 50,000 km/h":
        if button1:
            query_result("select distinct name from asteroids,close_approach where asteroids.id=close_approach.neo_reference_id and relative_velocity_kmph > '50000'")

    elif options == "11.Show how many approaches happened per month":
        if button1:
            query_result('select monthname(close_approach_date),count(close_approach_date) from close_approach group by monthname(close_approach_date)')
    
    elif options == "12.Display the asteroid with the highest brightness":
        if button1:
            query_result('select id,absolute_magnitude_h from asteroids  where absolute_magnitude_h=(select min(absolute_magnitude_h) from asteroids)')
            
    elif options == "13.Get number of hazardous vs non-hazardous asteroids":
        if button1:
            query_result("select count(distinct as1.id) as Hazardous,count(distinct as2.id) as NonHazardous from asteroids as1 JOIN asteroids as2 where as1.is_potentially_hazardous_asteroid='1' and as2.is_potentially_hazardous_asteroid='0'")
 
    elif options == "14.Show asteroids that passed closer than the Moon":
        if button1:
            query_result("select distinct neo_reference_id,close_approach_date ,miss_distance_lunar,miss_distance_km from close_approach where miss_distance_lunar < '1'")
 
    elif options == "15.Show asteroids that came within 0.05 AU(Astronomical Units)":
        if button1:
            query_result("select distinct neo_reference_id from close_approach where astronomical < '0.05'")
            
    elif options == "16.List the asteroid size information":
        if button1:
            query_result("select distinct name ,estimated_diameter_min_km,estimated_diameter_max_km from asteroids")

    elif options == "17.List of approaches per day sorted from highest to lowest":
        if button1:
            query_result("select close_approach_date,count(close_approach_date) from close_approach group by close_approach_date order by count(close_approach_date) desc")

    elif options == "18.Asteroid with the minimum estimated diameter":
        if button1:
            query_result("select distinct name from asteroids where estimated_diameter_min_km = (select min(estimated_diameter_min_km) from asteroids)")

    elif options == "19.Show all the required information regarding potentially hazardous asteroid":
        if button1:
            query_result("select distinct id,name,absolute_magnitude_h,estimated_diameter_min_km,estimated_diameter_max_km,close_approach_date,relative_velocity_kmph,astronomical,miss_distance_km,miss_distance_lunar from close_approach JOIN asteroids on asteroids.id=close_approach.neo_reference_id where asteroids.is_potentially_hazardous_asteroid ='1'")

    elif options == "20.Information regarding the distance by which the asteroids missed hitting Earth":
        if button1:
            query_result("select distinct neo_reference_id,miss_distance_km from close_approach order by miss_distance_km asc")

    elif options == "21.Show the Average miss distance":
        if button1:
            query_result("select avg(miss_distance_km) from close_approach")

    elif options == "22.Display the Date with the highest number of approaches":
        if button1:
            query_result("select  close_approach_date,count(neo_reference_id) from close_approach group by close_approach_date order by count(neo_reference_id) desc LIMIT 1")
         
    myconnection.close()



