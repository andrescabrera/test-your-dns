import pandas as pd
import altair as alt

# Sample data (replace with your actual data loading)
data = {
    "IP": [
        "207.138.36.249", "200.11.138.11", "190.94.212.10", "201.249.140.166",
        "190.94.247.154", "190.94.212.75", "181.233.89.54", "190.120.249.60",
        "200.75.135.226", "45.230.168.17", "200.74.203.116", "190.202.135.58",
        "186.24.48.97", "201.234.231.130", "190.6.31.100", "190.216.247.150",
        "186.166.202.49", "200.35.75.249", "45.187.94.147", "200.35.79.41",
        "200.35.94.41", "200.44.190.134", "200.35.74.49", "200.35.110.9"
    ],
    "ASNCity": [
        "AS266841 GALANET SOLUTION C.A.Caracas", "AS8048 CANTV Servicios, VenezuelaCaracas",
        "AS8053 IFX Networks Venezuela C.A.Caracas", "AS8048 CANTV Servicios, VenezuelaCaracas",
        "AS8053 IFX Networks Venezuela C.A.Caracas", "AS8053 IFX Networks Venezuela C.A.Caracas",
        "AS271907 COLNETWORK C.A.Cabimas", "AS264628 CORPORACION FIBEX TELECOM, C.A.Valencia",
        "AS11562 Net Uno, C.A.Caracas", "AS266742 SOLUCIONES DCN NETWORK C.ACaracas",
        "AS21980 Dayco Telecom, C.A.Caracas", "AS8048 CANTV Servicios, VenezuelaCoro",
        "AS6306 TELEFONICA VENEZOLANA, C.A.Maracaibo", "AS3549 Level 3 Parent, LLCCaracas",
        "AS11562 Net Uno, C.A.Maracay", "AS3549 Level 3 Parent, LLCCaracas",
        "AS6306 TELEFONICA VENEZOLANA, C.A.Barcelona", "AS6306 TELEFONICA VENEZOLANA, C.A.Barquisimeto",
        "AS269829 MARACAIBO NET C.AMaracaibo", "AS6306 TELEFONICA VENEZOLANA, C.A.San Carlos del Zulia",
        "AS6306 TELEFONICA VENEZOLANA, C.A.Caracas", "AS8048 CANTV Servicios, VenezuelaCaracas",
        "AS6306 TELEFONICA VENEZOLANA, C.A.Barquisimeto", "AS6306 TELEFONICA VENEZOLANA, C.A.Caracas"
    ],
    "Milliseconds": [
        9, 216, 156, 468, 246, 277, 1561, 309, 2160, 1759, 352, 261, 261, 353, 211, 281, 989, 176, 0, 0, 0, 0, 0, 0
    ],
    "Reliability": [
        "100 %", "100 %", "100 %", "100 %", "100 %", "100 %", "100 %", "100 %",
        "100 %", "100 %", "100 %", "100 %", "99.95 %", "99.9 %", "99.61 %",
        "98.44 %", "87.25 %", "76.67 %", "49.94 %", "39.26 %", "37.5 %",
        "24.99 %", "22.56 %", "8.17 %"
    ]
}

df = pd.DataFrame(data)

# Extract AS and Business from ASNCity
df[['AS', 'Business', 'City']] = df['ASNCity'].str.split(' ', n=2, expand=True)
df['Business'] = df['Business'].str.replace(r'C\.A\.', '', regex=True).str.strip()  # Clean C.A.

# Convert Reliability to numeric (remove %)
df['Reliability'] = df['Reliability'].str.replace('%', '', regex=True).astype(float)

# Remove failing DNS entries (Milliseconds <= 0)
df = df[df['Milliseconds'] > 0]

# Create the chart, ordered by Milliseconds (ascending)
chart = alt.Chart(df).mark_bar().encode(
    y=alt.Y('IP:N', title='IP Address', sort=alt.EncodingSortField(field="Milliseconds", order="ascending")),
    x=alt.X('Milliseconds:Q', title='Milliseconds'),
    tooltip=['IP', 'AS', 'Business', 'Reliability', 'Milliseconds']
).properties(
    title='Milliseconds by IP Address (Failing DNS Removed, Ordered)'
).interactive()

text = chart.mark_text(
    align='left',
    baseline='middle',
    dx=3
).encode(
    text=alt.Text('Milliseconds', format='.0f')
)

final_chart = chart + text

final_chart.save("ip_milliseconds_chart.json")
