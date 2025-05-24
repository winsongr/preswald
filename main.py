import pandas as pd
import plotly.express as px
import preswald

# Load and prep the data
try:
    cars = pd.read_csv("data/electric_cars_dataset.csv")
except Exception as e:
    print(f"Couldn't load dataset: {e}")
    cars = pd.DataFrame()

cars.drop_duplicates(inplace=True)
cars = cars.dropna(subset=["VIN (1-10)", "Model", "Make", "Electric Range"])
cars["Electric Range"] = pd.to_numeric(cars["Electric Range"], errors="coerce")
cars["Base MSRP"] = pd.to_numeric(cars["Base MSRP"], errors="coerce")
cars["Model Year"] = pd.to_numeric(cars["Model Year"], errors="coerce")
cars = cars.dropna()

preswald.text(
    "# Welcome to ElectraStats!\nCurious about electric cars? Let’s dig into the numbers and see what’s really happening on the roads. 🚗⚡"
)

# 1. Who’s got the longest legs?
top_range = (
    cars.groupby("Make")["Electric Range"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
preswald.text(
    "**1. Who’s got the longest legs?**\nThese car brands are pushing the limits on how far you can go on a single charge. Here are the top 10 by average range."
)
fig1 = px.bar(
    top_range,
    x="Make",
    y="Electric Range",
    labels={"Electric Range": "Avg Electric Range (miles)", "Make": "Make"},
    text=top_range["Electric Range"].round(1),
    title="Top 10 Makes by Average Electric Range",
)
fig1.update_traces(textposition="outside", marker_color="mediumseagreen")
fig1.update_layout(template="plotly_white")
preswald.plotly(fig1)

# 2. The priciest rides
top_price = (
    cars[["Model", "Base MSRP"]]
    .sort_values(by="Base MSRP", ascending=False)
    .head(10)
)
preswald.text(
    "**2. The priciest rides**\nWant to know which EVs cost the most? Here are the 10 models with the highest sticker prices."
)
preswald.table(top_price)

# 3. Where are all the EVs?
state_ev_counts = cars["State"].value_counts().reset_index()
state_ev_counts.columns = ["State", "Count"]
preswald.text(
    "**3. Where are all the EVs?**\nSome states are way ahead in EV adoption. Here’s where you’ll spot the most electric cars."
)
fig2 = px.bar(
    state_ev_counts.head(10),
    x="State",
    y="Count",
    labels={"Count": "Number of EVs", "State": "State"},
    text=state_ev_counts["Count"],
    title="Top 10 States by Electric Vehicle Count",
)
fig2.update_traces(textposition="outside", marker_color="cornflowerblue")
fig2.update_layout(template="plotly_white")
preswald.plotly(fig2)

# 4. Who gets the clean fuel perks?
cafv = (
    cars.groupby("State")["Clean Alternative Fuel Vehicle (CAFV) Eligibility"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .reset_index(name="CAFV Eligibility (%)")
    .sort_values(by="CAFV Eligibility (%)", ascending=False)
    .head(10)
)
preswald.text(
    "**4. Who gets the clean fuel perks?**\nSome states make it easier to go green. These 10 have the highest share of EVs eligible for CAFV benefits."
)
fig3 = px.bar(
    cafv,
    x="State",
    y="CAFV Eligibility (%)",
    labels={"CAFV Eligibility (%)": "% Eligible for CAFV", "State": "State"},
    text=cafv["CAFV Eligibility (%)"].round(1),
    title="Top 10 States by CAFV Eligibility %",
)
fig3.update_traces(textposition="outside", marker_color="tomato")
fig3.update_layout(template="plotly_white")
preswald.plotly(fig3)

# 5. How far do most EVs go?
preswald.text(
    "**5. How far do most EVs go?**\nHere’s a look at the spread of electric ranges—see where most cars land, and who’s breaking the mold."
)
fig4 = px.histogram(
    cars,
    x="Electric Range",
    nbins=30,
    labels={"Electric Range": "Electric Range (miles)"},
    title="Distribution of Electric Range",
)
fig4.update_layout(template="plotly_white")
preswald.plotly(fig4)

# 6. The crowd favorites
popular = cars["Model"].value_counts().head(10).reset_index()
popular.columns = ["Model", "Count"]
preswald.text(
    "**6. The crowd favorites**\nThese models are everywhere—here are the 10 most common EVs on the road."
)
preswald.table(popular)
