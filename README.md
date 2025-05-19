# mochi_health

In this take-home assessment, I was tasked with implementing a few features:
- Log a mood (through a dropdown), add a short note along with it, and append the result to a Google Sheet acting as a database.
- Visualize the mood using a bar chart for the mood counts of that specific day. The chart should auto-refresh, and be able to filter by day.

I deployed this app using Streamlit for the UI, matplotlib for the charts, and Google Sheets as the database. 

Further improvements:
If I had a bit more time, I could have implemented the filter by day feature a bit more cleanly, as I was having to press the submit button twice to refresh (this is part of the Streamlit learning curve). Otherwise, the implemented logic can handle other dates, and this can be tested by using 5-18-25 as the other date.
I also would have liked to polish the UI a bit more, but my goal was to move as quickly as possible, and to build out as much functionality as possible.
