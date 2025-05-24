import pandas as pd
import plotly.express as px
import preswald

df = pd.read_csv("data/electric_cars_dataset.csv")
fig = px.scatter(
    df,
    x="Model",
    y="Electric Range",
    text="Make",
    title="Electric Range vs. Model",
    labels={"Model": "Model", "Electric Range": "Electric Range"},
)

fig.update_traces(
    textposition="top center", marker=dict(size=12, color="lightblue")
)
fig.update_layout(template="plotly_white")


preswald.text("# Welcome to ElectraStats!")
preswald.text("This is a dashboard for electric car data. 🎉")
preswald.plotly(fig)
preswald.table(df)
