import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


helpline_state = 'Central'
image = Image.open('hospital.png')
sir_img = Image.open('SIR.png')
video = open('Covid.mp4','rb')
video_bytes = video.read()

#df = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')

#st.title("Covid-19 India")
st.markdown("<h1 style='text-align: center; color: black; font-size : 3rem'>Covid-19 India</h2>", unsafe_allow_html=True)
#st.image(image)



@st.cache
def load_data():
    df = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
    df['Date_time'] = df['Date'].apply(lambda dt : dt + ' 2020')
    df['Date_time'] = pd.to_datetime(df['Date_time'])
    df['Daily Active'] = df['Daily Confirmed'] - df['Daily Deceased'] - df['Daily Recovered']
    df['Total Active'] = df['Total Confirmed'] - df['Total Deceased'] - df['Total Recovered']
    df = df[['Date','Date_time', 'Daily Confirmed', 'Total Confirmed','Daily Active', 'Total Active','Daily Recovered',
       'Total Recovered', 'Daily Deceased', 'Total Deceased']]

    df_state = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
    df_state = df_state[['State', 'Confirmed', 'Recovered', 'Deaths', 'Active']]
    df_state.sort_values('Confirmed', ascending=False, inplace=True)

    df_district = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
    df_district = df_district[['State', 'District', 'Confirmed', 'Active', 'Recovered', 'Deceased', 'Last_Updated' ]]

    df_helpline = pd.read_csv('helpline.csv')

    return df.set_index('Date_time'), df_state[1:], df_district, df_helpline

df, df_state, df_district, df_helpline = load_data()


st.subheader('Last updated on ' + df['Date'][df.shape[0]-1])
st.markdown('')

st.sidebar.image(image)
st.sidebar.title('Prevention')
st.sidebar.subheader('Wear a mask. Save lives.')
st.sidebar.markdown('- Wear a face cover')
st.sidebar.markdown('- Wash your hands')
st.sidebar.markdown('- Keep a safe distance')
st.sidebar.video(video_bytes)
st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

helpline_state = st.sidebar.selectbox('State Helpline Number',df_helpline['State'])

st.sidebar.success(df_helpline[df_helpline['State']==helpline_state]['Helpline'].values[0])


if st.sidebar.button('Contact Developer'):
    st.sidebar.markdown('**Tanmay Sharma**')
    st.sidebar.markdown('Data Scientist')
    st.sidebar.markdown('Linkdin : _https://www.linkedin.com/in/tanmay-sharma-75718b195/_')
    st.sidebar.markdown('Github : _https://github.com/tansha31_')


# display total Confirmed, total Active, total Recovered, total Deceased, daily stats
st.error('Confirmed :__ ' + str(df.iloc[df.shape[0]-1][2]) + '__ ( +' + str(df.iloc[df.shape[0]-1][1]) + ' )'  )
st.info('Active :__ ' + str(df.iloc[df.shape[0]-1][4]) + '__ ( +' + str(df.iloc[df.shape[0]-1][3]) + ' )'  )
st.success('Recovered :__ ' + str(df.iloc[df.shape[0]-1][6]) + '__ ( +' + str(df.iloc[df.shape[0]-1][5]) + ' )'  )
st.warning('Deceased :__ ' + str(df.iloc[df.shape[0]-1][8]) + '__ ( +' + str(df.iloc[df.shape[0]-1][7]) + ' )'  )

st.markdown('')
st.markdown('### State-Wise Cases')
st.write('Data Dimension : ' + str(df_state.shape[0]) + ' rows and ' + str(df_state.shape[1]) + ' columns.')
st.write(df_state)

st.markdown('')
st.write('Cumulative Plot of Total Cases')
st.line_chart(df[['Date','Total Confirmed','Total Active', 'Total Recovered', 'Total Deceased']])

st.write('Cumulative Plot of Daily Cases')
st.line_chart(df[['Date','Daily Confirmed','Daily Active', 'Daily Recovered', 'Daily Deceased']])


states = ['Rajasthan', 'Maharashtra', 'Tamil Nadu', 'Andhra Pradesh',
       'Karnataka', 'Delhi', 'Uttar Pradesh', 'West Bengal', 'Bihar',
       'Telangana', 'Gujarat', 'Assam', 'Odisha', 'Haryana',
       'Madhya Pradesh', 'Kerala', 'Punjab', 'Jammu and Kashmir',
       'Jharkhand', 'Chhattisgarh', 'Uttarakhand', 'Goa', 'Tripura',
       'Puducherry', 'Manipur', 'Himachal Pradesh', 'Nagaland',
       'Arunachal Pradesh', 'Andaman and Nicobar Islands', 'Ladakh',
       'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
       'Meghalaya', 'Sikkim', 'Mizoram', 'State Unassigned',
       'Lakshadweep']


st.markdown('')
st.markdown('### District-Wise Cases')
district_state = st.selectbox('Select State',states)
st.write(df_district[df_district['State'] == district_state].drop(['State','Last_Updated'],axis=1).sort_values('Confirmed',ascending=False))


# SIR MODEL
st.markdown("""
## **SIR MODEL**
A basic compartmental model of how disease spreads
- **Suseptible people:** people who could catch the disease
- **Infected people:** people who have the disease and can spread it
- **Recovered/removed people:** people who had the disease and cannot get it again (but not in case of Covid-19)
""")

st.markdown('')
st.image(sir_img)

st.markdown("""
---
### **Susceptible to Infected...**
- **Contact Rate:** how often do infected and susceptible people come in contact?
- **Risk of Infection:** during one of those contacts, what is the chance of spreading the disease?
""")

st.markdown("""
---
### **Infected to Removed...**
Two ways to move from infected to removed:
- Get better
- Die
""")

st.markdown('**Recovery Period:** how long does it take to recover')
st.markdown('**Removal Rate:** 1 / recovery period, this is the rate at which people stop being infected')

st.markdown("""
---
### **What is R0?**
Movement between compartments:
- S to I is **effective contact rate:** contact_rate * risk_of_infection
- I to R is **removal rate:** 1 / recovery_period
""")

st.code("""
# Effective Contact Rate
4 * 0.10 = 0.4
""")

st.code("""
# Removal Rate (takes 14 days to recover)
1/12 = 0.0833
""")

st.code("""
# Basic Reproductive Rate: Effective Contact Rate / Removal Rate
0.4/0.0833 = 4.8019 (example)
""")

st.write('## **Covid-19 Peak Prediction**')
st.markdown('')
st.markdown('')

# reading data again
DF = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
DF['Date_time'] = DF['Date'].apply(lambda dt : dt + ' 2020')
DF['Date_time'] = pd.to_datetime(DF['Date_time'])
DF['Daily Active'] = DF['Daily Confirmed'] - DF['Daily Deceased'] - DF['Daily Recovered']
DF['Total Active'] = DF['Total Confirmed'] - DF['Total Deceased'] - DF['Total Recovered']
DF = DF[['Date','Date_time', 'Daily Confirmed', 'Total Confirmed','Daily Active', 'Total Active','Daily Recovered',
   'Total Recovered', 'Daily Deceased', 'Total Deceased']]

from scipy.integrate import odeint
from datetime import datetime, timedelta

# The SIR model differential equations.
def deriv(state, t, N, beta, gamma):
    S, I, R = state
    # Change in S population over time
    dSdt = -beta * S * I / N
    # Change in I population over time
    dIdt = beta * S * I / N - gamma * I
    # Change in R population over time
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

effective_contact_rate = 0.1076
recovery_rate = 1/14
total_pop = 14700000
recovered = 200
infected = 1000
susceptible = total_pop - infected - recovered

# A list of days, 0-160
days = range(0, 179 + DF.shape[0]-1)

# Use differential equations to predict spread of the virus
ret = odeint(deriv,
             [susceptible, infected, recovered],
             days,
             args=(total_pop, effective_contact_rate, recovery_rate))
S, I, R = ret.T

# Build a dataframe of predicted values
df_new = pd.DataFrame({
    'suseptible': S,
    'infected': I,
    'recovered': R,
    'day': days
})

l = []
for i in range(1,179):
    l.append(DF['Date_time'][DF.shape[0]-1] + timedelta(days=i))

old = DF['Date_time'].to_list()

final = np.array(old+l)

df_new['Date_Time'] = final
df_final = pd.concat([df_new,DF],axis=1)

st.line_chart(df_final.set_index('Date_Time')[['suseptible', 'infected', 'recovered','Total Active', 'Total Recovered',
       'Total Deceased']])

st.markdown("""
---
**Disclaimer:** Covid-19 modeling studies generally follow general approach. Forecasting models are often statistical in nature, fitting a line or curve to data and extrapolating from there — like seeing a pattern in a sequence of numbers and guessing the next number, without incorporating the process that produces the pattern.
""")
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown("<h5 style='text-align: center; color: black;'>© Covid-19 Tracker. All Rights Reserved.</h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: black;'>We stand with everyone fighting on the frontlines</h5>", unsafe_allow_html=True)
