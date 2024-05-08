![image](https://github.com/Dhusha/Capstone-02-Phonepe-Project/assets/165916395/83bdd07e-75db-47ba-8178-f26b1bd632a6)

# DATA VISUALIZATION AND EXPLORATION: A USER-FRIENDLY TOOL USING STREAMLIT AND PLOTLY

## Introduction

Welcome to PhonePe Pulse, where data meets innovation! Our interactive web application offers a captivating exploration of over 2000+ Crore transactions spanning across the vibrant landscape of India. As PhonePe boasts a commanding 45% market share, delve into a treasure trove of invaluable insights into the digital payment trends shaping the nation. Explore freely, download reports, and embark on an enlightening journey through India's digital financial landscape, all available on the PhonePe Pulse website and GitHub.

## The Tools of Transformation

- **Plotly**: Unleash the visual potential of your data.
- **Pandas**: Sculpt and mold your data with unparalleled flexibility.
- **mysql.connector**: Seamlessly integrate database operations into your workflow.
- **Streamlit**: Craft intuitive user interfaces that engage and captivate.
- **json**: Navigate and manipulate JSON files with ease.

## The Adventure Unfolds

Embark on a thrilling journey through my workflow.

### Step 1: Empowerment Through Libraries

Equip yourself with the arsenal of libraries essential for your journey. Install and import with ease to unlock a world of possibilities.

If the libraries are already installed then we have to import those into our script by mentioning the below codes.

        import pandas as pd
        import mysql.connector as sql
        import streamlit as st
        import plotly.express as px
        import os
        import json
        from streamlit_option_menu import option_menu
        from PIL import Image
  
 

### Step 2: Unearth Data Treasures
Embark on a quest to unearth data treasures! Clone the GitHub repository to uncover the rich tapestry of insights hidden within PhonePe Pulse.

### Step 3: Shape Your Narrative
Craft your story with precision and finesse. Transform raw JSON files into elegant DataFrames, shaping your data into a compelling narrative.
    
    path1 = "Path of the JSON files"
    agg_trans_list = os.listdir(path1)

    # Give any column names that you want
    columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],'Transaction_amount': []}

Looping through each and every folder and opening the json files appending only the required key and values and creating the dataframe.

    for state in agr_trns_list:
    current_states = path1 + state + "/"
    #print(current_states)
    agr_year_list = os.listdir(current_states)
    #print(agr_year_list)
    
    for year in agr_year_list:
        current_year = current_states + year + "/"
        agr_file_list = os.listdir(current_year)

        for file in agr_file_list:
            current_file = current_year + file 
            data=open(current_file,"r")   #r=read

            A=json.load(data)
            for i in A["data"]["transactionData"]:
                name=i["name"]
                count=i["paymentInstruments"][0]["count"]
                amount=i["paymentInstruments"][0]["amount"]
                column1["Transaction_type"].append(name)
                column1["Transaction_count"].append(count)
                column1["Transaction_amount"].append(amount)
                column1["States"].append(state)
                column1["Years"].append(year)
                column1["Quater"].append(int(file.strip(".json")))
        aggregated_transaction = pd.DataFrame(column1)
    

### Step 4: Forge Connections
Forge powerful connections between your data and the digital realm. Establish a bridge to the MySQL database, allowing your insights to permeate through the fabric of the digital landscape.

   **Creating the connection between python and mysql**
   
        mydb = sql.connect(host="localhost",
                   user="username",
                   password="password",
                   database= "phonepe_pulse"
                  )
        mycursor = mydb.cursor(buffered=True)
        
   **Creating tables in Mysql**
   
       sql_query="CREATE TABLE agr_trns (States VARCHAR(255), Years INT, Quater INT, Transaction_type VARCHAR(255), Transaction_count BIGINT, Transaction_amount BIGINT)"
      mycursor.execute(sql_query)
      mydb.commit()
      
      insert_query="INSERT INTO agr_trns(States,Years,Quater,Transaction_type,Transaction_count,Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)"
      data=aggregated_transaction.values.tolist()
      mycursor.executemany(insert_query,data)
      mydb.commit()

### Step 5: Dashboard Creation

To create a colorful and insightful dashboard, I've used Plotly libraries in Python to create an interactive and visually appealing dashboard. Plotly's built-in Pie, Bar, Geo map functions are used to display the data on charts and maps, while Streamlit is used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.

### Step 6: Data Retrieval

Finally, if needed, use the "mysql-connector-python" library to connect to the MySQL database and fetch the data into a Pandas dataframe.





