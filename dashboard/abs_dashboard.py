import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

months_in_turkish = {'Ocak':1,
                     'Şubat':2,
                     'Mart':3,
                     'Nisan':4,
                     'Mayıs':5,
                     'Haziran':6,
                     'Temmuz':7,
                     'Ağustos':8,
                     'Eylül':9,
                     'Ekim':10,
                     'Kasım':11,
                     'Aralık':12}

@st.cache
def load_data(nrows):
    data = pd.read_csv('abs_fixed_data.csv')
    data['tarih'] = pd.to_datetime(data['tarih'])
    return data

#data_load_state = st.text('Loading data...')
data = load_data(10000)
#data_load_state.text('Data hafızaya alındı.')
unq = data['month'].unique()
params = data.columns
#unq2 = months_in_turkish[unq]
#st.write(list(months_in_turkish.keys()))

df = pd.DataFrame()

st.title('ABS Lojistik Aylık Rapor')
st.text('E-Liner Lojistik raporlama sistemi ile aylık tüm iş datasını gözlemleyebilirsiniz.')

def filterMonths(x):
    months = unq
    if(x in months):
        return True
    else:
        return False

filteredMonths = filter(filterMonths, list(months_in_turkish.values()))

month_to_filter_text = st.sidebar.selectbox('Rapor Tarihi Seciniz', list(months_in_turkish.keys()), 8)
month_to_filter = months_in_turkish[month_to_filter_text]
#month_to_filter = st.slider('Hangi ay?', 7,9,9)
filtered_data = data[data.month == month_to_filter]

#st.write('Toplam fatura: ' filtered_data['toplam_fatura'].sum())

if st.checkbox('Datayı göster'):
    st.subheader('Özet data')
    st.write(filtered_data.describe())
    if st.checkbox('Detayları göster'):
        st.write(filtered_data)
        if st.checkbox('Tüm datayı göster'):
            st.write(data)

#month_to_filter = st.slider('month', 7, 9, 9)
#
#st.subheader(f'{month_to_filter}. ayda kesilen faturalar')

#c = alt.Chart(filtered_data).mark_circle().encode(x='a', y='b', size='c', color='c')

#st.altair_chart(c, width=-1)

#st.write(month_to_filter)

#group_labels = ['ok']
#fig = ff.create_distplot(filtered_data, group_labels, bin_size=[.1, .25, .5])

#st.plotly_chart(fig)

data_dropped = data.drop( columns = ['month', 'tarih', 'sefer_no'])

data_to_filter = st.sidebar.selectbox('Hangi data?', data_dropped.columns)

#x = [date2num(date) for (date, value) in data]
#y = [value for (date, value) in data]

#fig = plt.figure()
#
#graph = fig.add_subplot(111)

# Plot the data as a red line with round markers
#graph.plot(data['tarih'],data['toplam_fatura'],'r-o')

# Set the xtick locations to correspond to just the dates you entered.
#graph.set_xticks(data['tarih'])

# Set the xtick labels to correspond to just the dates you entered.
#graph.set_xticklabels(
       # data['tarih'].strftime("%Y-%m-%d")
      #  )

#plt.show()

st.line_chart(filtered_data[data_to_filter])
st.bar_chart(filtered_data[data_to_filter])
#filtered_data2 = data[data.month == month_to_filter]
#st.subheader(f'Map of all pickups at {month_to_filter}:00')
#st.map(filtered_data2)

## streamlit run xxx.py
