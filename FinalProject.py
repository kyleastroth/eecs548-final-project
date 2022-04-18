import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
import os

st.write("# Case Study: Boise, Idaho")
st.write("### What is the public perception of the risks of wildfire smoke?")
st.write("##### In 2019, researchers at the University of California, Irvine collected a dataset of 2360 randomly selected samples from the Boise Metropolitan Area in Idaho that gathered information about activity levels during wildfire smoke threats, the perception of wildfire smoke as a hazard, and any wildfire smoke related health issues.")
st.write('##### Idaho ranks fifth in US states for wildfire risk, and exposure to wildfire smoke particles can cause serious health risks, specifically for people with pre-existing conditions.')
st.write('### Exploratory analysis of the dataset demographics')

data_path = os.path.abspath('export_dataframe.csv')

#df = pd.read_csv('/home/kyleastroth/UMich/eecs548/export_dataframe.csv')
df = pd.read_csv(data_path)

base = alt.Chart(df).encode(
    theta=alt.Theta('count(Gender):Q', stack=True), 
    color=alt.Color("Gender:N", legend=None),
    tooltip=[alt.Tooltip('count(Gender):Q', title="Num of Participants")]
).transform_filter(
    (datum.Gender != '0')
).properties(
    title='Gender of Participants'
)

pie = base.mark_arc(outerRadius=80)
text = base.mark_text(radius=120, size=16).encode(text="Gender:N")

chart1 = pie + text
# chart1 = chart1.configure_title(
#     fontSize=16
# ).configure_view(
#     strokeWidth=0
# )


base = alt.Chart(df).encode(
    theta=alt.Theta('count(GeneralHealth):Q', stack=True), 
    color=alt.Color("GeneralHealth:N", legend=None),
    tooltip=[alt.Tooltip('count(GeneralHealth):Q', title="Num of Participants")]
).transform_filter(
    (datum.GeneralHealth != '0')
).properties(
    title='General Health of Participants'
)

pie = base.mark_arc(outerRadius=80)
text = base.mark_text(radius=120, size=16).encode(text="GeneralHealth:N")

chart2 = pie + text
# chart2 = chart2.configure_title(
#     fontSize=16
# ).configure_view(
#     strokeWidth=0
# )

st.altair_chart(chart1 | chart2)

barChart = alt.Chart(df).mark_bar().encode(
    x=alt.X('count(IncomeLevel):Q', title="Number of Participants"),
    y=alt.Y('IncomeLevel:N', title='Income', 
            sort=[
                "$100,000 or more",
                "$75,000 to $99,999",
                "$50,000 to $74,999",
                "$25,000 to $49,999",
                "$25,000 or less"
            ]),
    tooltip=[alt.Tooltip('count(IncomeLevel):Q', title="Num of Participants")]
).transform_filter(
    (datum.IncomeLevel != '0')
).properties(
    title="Income Level of Participants",
    height=200,
    width=822
)

barChart.configure_title(
    fontSize=16
).configure_axis(
    labelFontSize=12,
    titleFontSize=12
)

st.altair_chart(barChart)

st.write('#### Is wildfire smoke as serious of a public health threat as other natural disasters, such as hurricanes or tornadoes?')

bars = alt.Chart(df).mark_bar().encode(
    x=alt.X('count(PublicHealthThreat):O', title="Number of Participants"),
    y=alt.Y('PublicHealthThreat:O',
            title=None,
            sort=['Much more severe/important', 'Somewhat more severe/important', 'About as severe/important',
                 'Somewhat less severe/important', 'Much less severe/important']
           ),
    color=alt.Color('IncomeLevel',
                    legend=alt.Legend(title='Income Level', labelFontSize=12, titleFontSize=12),
                    sort=['$25,000 or less', '$25,000 to $49,999', '$50,000 to $74,999', 
                          '$75,000 to $99,999', '$100,000 or more']
                   ),
    tooltip=[alt.Tooltip('count(PublicHealthThreat):Q', title="Num of Participants")]
).transform_filter(
    (datum.IncomeLevel != '0') &
    (datum.PublicHealthThreat != '0')
).properties(
    height=150,
    width=600
).configure_axis(
    labelFontSize=12,
    titleFontSize=12
)

st.altair_chart(bars)

st.write('#### Have you, or anyone in your household, experienced wildfire smoke-related illness?')

base = alt.Chart(df).encode(
    theta=alt.Theta('count(SmokeRelatedIllness):Q', stack=True), 
    color=alt.Color("SmokeRelatedIllness:N", legend=None),
    tooltip=[alt.Tooltip('count(SmokeRelatedIllness):Q', title="Num of Participants")]
).transform_filter(
    (datum.SmokeRelatedIllness != '0')
)

pie = base.mark_arc(outerRadius=120)
text = base.mark_text(radius=160, size=16).encode(text="SmokeRelatedIllness:N")

chart = pie + text
# chart.configure_view(
#     strokeWidth=0
# )

st.altair_chart(chart)

st.write('#### Would participants consider evacuating due to wildfire smoke?')

base = alt.Chart(df).transform_aggregate(
    num_people='count()',
    groupby=['IncomeLevel', 'ConsiderEvacuatingHome']
).encode(
    alt.X('IncomeLevel:O', scale=alt.Scale(paddingInner=0), title="Income Level"),
    alt.Y('ConsiderEvacuatingHome:O', scale=alt.Scale(paddingInner=0), title=None),
).transform_filter(
    (datum.IncomeLevel != '0') &
    (datum.ConsiderEvacuatingHome != '0') &
    (datum.ConsiderEvacuatingHome != 'Prefer not to answer')
)

heatmap = base.mark_rect().encode(
    color=alt.Color('num_people:Q',
                    scale=alt.Scale(scheme='orangered'),
                    legend=alt.Legend(direction='horizontal',
                                      title='Num of Participants',
                                      labelFontSize=12,
                                      titleFontSize=12)
                   )
)

text = base.mark_text(baseline='middle').encode(
    text='num_people:Q',
    color=alt.condition(
        alt.datum.num_people > 200,
        alt.value('white'),
        alt.value('black')
    )
)

heatmap1 = (heatmap + text).properties(
    height=150,
    width=200
)
# .configure_axis(
#     labelFontSize=12,
#     titleFontSize=14
# )

base = alt.Chart(df).transform_aggregate(
    num_people='count()',
    groupby=['GeneralHealth', 'ConsiderEvacuatingHome']
).encode(
    alt.X('GeneralHealth:O', scale=alt.Scale(paddingInner=0), title="General Health"),
    alt.Y('ConsiderEvacuatingHome:O', scale=alt.Scale(paddingInner=0), title=None),
).transform_filter(
    (datum.GeneralHealth != '0') &
    (datum.ConsiderEvacuatingHome != '0') &
    (datum.ConsiderEvacuatingHome != 'Prefer not to answer')
)

heatmap = base.mark_rect().encode(
    color=alt.Color('num_people:Q',
                    scale=alt.Scale(scheme='purpleblue'),
                    legend=alt.Legend(direction='horizontal', 
                                      title='Num of Participants',
                                      labelFontSize=12,
                                      titleFontSize=12)
                   )
)

text = base.mark_text(baseline='middle').encode(
    text='num_people:Q',
    color=alt.condition(
        alt.datum.num_people > 400,
        alt.value('white'),
        alt.value('black')
    )
)

heatmap2 = (heatmap + text).properties(
    height=150,
    width=200
)
# .configure_axis(
#     labelFontSize=12,
#     titleFontSize=14
# )

st.altair_chart(heatmap1 | heatmap2)