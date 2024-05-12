import pandas as pd
import streamlit as st
import plotly.express as px
import os
import json
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from streamlit_option_menu import option_menu

# Setting up page configuration
icon = Image.open(r"C:\Users\tpsna\OneDrive\Desktop\VSCode\Phonepe\phonepe.png")
st.set_page_config(page_title="Phonepe Pulse Data Visualization | By Dhusha",
                    page_icon=icon,
                    layout="wide",
                    initial_sidebar_state="expanded",
                   menu_items={'About': """# This dashboard app is created by *Dhusha*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.markdown("**:violet[Hello! Welcome to the dashboard]** :wave:")

mydb = mysql.connector.connect(host="localhost", user="root", password="Dhusha98")
mycursor = mydb.cursor(buffered=True)
mycursor.execute('use phonepepulse')
mycursor = mydb.cursor(buffered=True)

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Top Charts", "Explore Data", "About"],
                            icons=["house", "graph-up-arrow", "bar-chart-line", "exclamation-circle"],
                            menu_icon="menu-button-wide",
                            default_index=0,
                            styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px",
                                                "--hover-color": "#6F36AD"},
                                    "nav-link-selected": {"background-color": "#6F36AD"}})

# MENU 1 - HOME
if selected == "Home":
    st.markdown("# :violet[Phonpe Pulse Data Visualization and Exploration]")
    st.markdown("## :white[A User-Friendly Tool Using Streamlit and Plotly] 🚀")

    col1, col2 = st.columns([4, 1], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github-Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit and Plotly")
        st.markdown("### :violet[Overview :]  This streamlit app can be used to visualize the PhonePe pulse data and gain lots of insights on Transactions, Number of users, Top 10 States, Districts, Pincodes. Bar charts, Pie charts and Geo map visualization are used to get insights.")
    with col2:
        st.image(r"C:\Users\tpsna\OneDrive\Desktop\VSCode\Phonepe\phonepe_image.webp")

if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        Years = st.slider("Years", min_value=2018, max_value=2023)
        Quater = st.slider("Quater", min_value=1, max_value=4)

    with col2:
        st.info(
            """
            ### Insights Menu :mag_right:
            Explore key insights including:
            
            - Overall ranking for a specific Year and Quarter.
            - Top 10 States, Districts, Pincodes by total transaction volume and spending.
            - Top 10 States, Districts, Pincodes by total PhonePe users and app usage frequency.
            - Top 10 Mobile Brands and their market share among PhonePe users.
            """
        )

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        col1, col2, col3 = st.columns([1, 1, 1], gap="small")

        with col1:
            st.markdown("### :violet[States]")
            mycursor.execute(f"""
                SELECT States, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_Amount
                FROM agr_trns
                WHERE Years = {Years} AND Quater = {Quater}
                GROUP BY States
                ORDER BY Total_Amount DESC
                LIMIT 10
            """)
            data1 = mycursor.fetchall()
            if data1:
                df1 = pd.DataFrame(data1, columns=['States', 'Total_Transactions', 'Total_Amount'])
                fig = px.pie(df1, values='Total_Amount',
                                names='States',
                                title='Top 10 States by Total Transactions',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Transactions'],
                                labels={'Total_Transactions': 'Total Transactions'})
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for selected period.")

        with col2:
            st.markdown("### :violet[Districts]")
            mycursor.execute(f"""
                SELECT Districts, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_Amount
                FROM map_trns
                WHERE Years = {Years} AND Quater = {Quater}
                GROUP BY Districts
                ORDER BY Total_Amount DESC
                LIMIT 10
            """)
            data2 = mycursor.fetchall()
            if data2:
                df2 = pd.DataFrame(data2, columns=['Districts', 'Total_Transactions', 'Total_Amount'])
                
                # Create bar chart using Plotly
                fig = px.bar(df2, x='Districts', y='Total_Amount', 
                            color='Total_Transactions',
                            title='Top 10 Districts by Total Transactions',
                            labels={'Districts': 'District', 'Total_Amount': 'Total Amount', 'Total_Transactions': 'Total Transactions'},
                            color_continuous_scale=px.colors.sequential.Agsunset)
                
                # Update layout
                fig.update_layout(xaxis_title='Districts', yaxis_title='Total Amount')
                
                # Display the bar chart
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for selected period.")

        with col3:
            st.markdown("### :violet[Pincodes]")
            mycursor.execute(f"""
                SELECT Pincodes, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_Amount
                FROM top_trns
                WHERE Years = {Years} AND Quater = {Quater}
                GROUP BY Pincodes
                ORDER BY Total_Amount DESC
                LIMIT 10
            """)
            data3 = mycursor.fetchall()
            if data3:
                df3 = pd.DataFrame(data3, columns=['Pincodes', 'Total_Transactions', 'Total_Amount'])
                fig = px.pie(df3, values='Total_Amount',
                                names='Pincodes',
                                title='Top 10 Pincodes by Total Transactions',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Transactions'],
                                labels={'Total_Transactions': 'Total Transactions'})
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for selected period.")

    # Top Charts - USERS
    elif Type == "Users":
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small")

        with col1:
            st.markdown("### :violet[Brands]")
            mycursor.execute(f"""
                SELECT Brands, SUM(Transaction_count) AS Total_Users, AVG(Percentage)*100 AS Avg_Percentage
                FROM agr_user
                WHERE Years = {Years} AND Quater = {Quater}
                GROUP BY Brands
                ORDER BY Total_Users DESC
                LIMIT 10
            """)
            data = mycursor.fetchall()
            if data:
                df1 = pd.DataFrame(data, columns=['Brands', 'Total_Users', 'Avg_Percentage'])
                fig = px.bar(df1,
                                title='Top 10 Brands by Total Users',
                                x="Total_Users",
                                y="Brands",
                                orientation='h',
                                color='Avg_Percentage',
                                color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for selected period.")

        with col2:
            st.markdown("### :violet[Top Users]")
            mycursor.execute("""
                SELECT States, Pincodes, RegisteredUsers, Total_Amount
                FROM top_user
                LIMIT 10
            """)
            top_user_data = mycursor.fetchall()
            if top_user_data:
                df2 = pd.DataFrame(top_user_data, columns=['States', 'Pincodes', 'RegisteredUsers', 'Total_Amount'])
                
                # Create bar chart using Plotly
                fig = px.bar(df2, 
                                title='Top 10 Users by State',
                                x='States', 
                                y='RegisteredUsers', 
                                color='Total_Amount',  # Use an existing column for coloring
                                color_continuous_scale=px.colors.sequential.Agsunset,
                                labels={'States': 'State', 'RegisteredUsers': 'Registered Users', 'Total_Amount': 'Total Amount'})
                    
                # Update layout
                fig.update_layout(xaxis_title='State', yaxis_title='Registered Users')
                    
                # Display the bar chart
                st.plotly_chart(fig, use_container_width=True)



# EXPLORE DATA - Transactions      
elif selected == "Explore Data":
    Years = st.sidebar.slider("**Years**", min_value=2018, max_value=2023)
    Quater = st.sidebar.slider("Quater", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns(2)

    # Explore DATA - Transactions:
    if Type == "Transactions":
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"""
                SELECT States,
                        SUM(Transaction_count) as Total_Transactions,
                        SUM(Transaction_amount) AS Total_Amount
                    FROM map_trns
                WHERE Years = {Years} AND Quater = {Quater}
                GROUP BY States
                ORDER BY States
            """)
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Total_Transactions', 'Total_Amount'])
            df2 = pd.read_csv(r"C:\Users\tpsna\OneDrive\Desktop\VSCode\Phonepe\States.csv")  # Assuming this CSV contains state names
            df1.State = df2
            fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='States',
                                color='Total_Amount',  # Change this to 'Total_Users' or 'Total_Appopens'
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"""
                SELECT States, 
                        SUM(Transaction_count) AS Total_Transactions, 
                        SUM(Transaction_amount) AS Total_Amount 
                FROM map_trns 
                WHERE Years = {Years} AND Quater = {Quater} 
                GROUP BY States 
                ORDER BY States
            """)
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Total_Transactions', 'Total_Amount'])
            df2 = pd.read_csv(r"C:\Users\tpsna\OneDrive\Desktop\VSCode\Phonepe\States.csv")
            df1['Total_Transactions'] = df1['Total_Transactions'].astype('object')
            df1.States = df2
            fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='States',
                                color='Total_Transactions',  # Change this to 'Total_Transactions' or 'Total_Amount'
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"""
            SELECT Transaction_type, 
                    SUM(Transaction_count) AS Total_Transactions, 
                    SUM(Transaction_amount) AS Total_Amount 
            FROM agr_trns 
            WHERE Years = {Years} AND Quater = {Quater} 
            GROUP BY Transaction_type 
            ORDER BY Transaction_type
        """)
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_Amount'])
        fig = px.bar(df,
                        title='Transaction_type vs Total_Transactions',
                        x="Transaction_type",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_Amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=False)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                                        ('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                        'Uttarakhand', 'West Bengal'), index=30)
        mycursor.execute(f"""
            SELECT States, Districts, Years, Quater,
                    SUM(Transaction_count) AS Total_Transactions,
                    SUM(Transaction_amount) AS Total_Amount
            FROM map_trns
            WHERE Years = {Years} AND Quater = {Quater} AND States = '{selected_state}'
            GROUP BY States, Districts, Years, Quater
            ORDER BY States, Districts
        """)

        df1 = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Districts', 'Years', 'Quater',
                                                            'Total_Transactions', 'Total_Amount'])
        fig = px.bar(df1,
                        title=selected_state,
                        x="Districts",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_Amount',  # Change this to 'Total_Users' or 'Total_Appopens'
                        color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

# EXPLORE DATA - USERS      
    elif Type == "Users":
        st.markdown("## :violet[Overall State Data - User App opening frequency]")

        mycursor.execute(f"""
                            SELECT States,
                                    SUM(RegisteredUsers) AS Total_Users,
                                    SUM(AppOpens) AS Total_Appopens
                            FROM map_user
                            WHERE Years = {Years} AND Quater = {Quater}
                            GROUP BY States
                            ORDER BY States""")
                
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['States','Total_Users','Total_Appopens'])
        df2 = pd.read_csv(r"C:\Users\tpsna\OneDrive\Desktop\VSCode\Phonepe\States.csv")
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.States = df2
        fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='States',  # Correcting the column name to match DataFrame
                            color='Total_Appopens',
                            color_continuous_scale='sunset')
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## :violet[Select any State to explore more]")
        mycursor.execute(f"""
            SELECT States, 
                SUM(RegisteredUsers) AS Total_Users, 
                SUM(AppOpens) AS Total_Appopens 
            FROM map_user 
            WHERE Years = {Years} AND Quater = {Quater}
            GROUP BY States
            ORDER BY Total_Users DESC, Total_Appopens DESC
            LIMIT 10""")
        result = mycursor.fetchall()

        # Convert SQL result to DataFrame
        df = pd.DataFrame(result, columns=['States', 'Total_Users', 'Total_Appopens'])

        # Melt DataFrame to long format for plotting
        df_melted = pd.melt(df, id_vars=['States'], value_vars=['Total_Users', 'Total_Appopens'],
                            var_name='Metric', value_name='Count')

        # Create grouped horizontal bar chart using Plotly
        fig = px.bar(df_melted, y='States', x='Count', color='Metric', orientation='h',
                    barmode='group', title=f'Total Users and Total AppOpens by State for Year {Years} Quarter {Quater}',
                    labels={'States': 'State', 'Count': 'Count', 'Metric': 'Metric'},
                    color_discrete_map={'Total_Users': 'orange', 'Total_Appopens': 'blue'})

        # Update layout
        fig.update_layout(yaxis_tickangle=-45)

        # Display Plotly chart in Streamlit
        st.plotly_chart(fig)

# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.markdown("[GitHub Profile](https://github.com/Dhusha)")
      
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image(r"C:\Users\tpsna\OneDrive\Desktop\VSCode\Phonepe\insurancephonepe.png")
