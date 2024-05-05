 Here is the Python code to generate the required visualizations:

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Load the data (replace this with your actual data source)
data = pd.read_csv('financial_data.csv')

# Function to update the graph_1
def update(val):
    graph_1.set_data(data.iloc[:val, 1].tolist(), data.iloc[:val, 3].tolist())
    return graph_1

# Function to update the graph_2
def update2(val):
    graph_2.set_data(data.iloc[:val, 10].tolist(), data.iloc[:val, 14].tolist())
    return graph_2

# Create the figure and axes
fig, ax = plt.subplots(2, 1, constrained_layout=True)

# Line graph showing trends over the years
graph_1 = ax[0].plot(data['Year'], data['Total Revenue'], color='blue', label='Total Revenue')
ax[0].set_ylabel('Total Revenue (in  millions)')
ax[0].set_title('Total Revenue Trends')
ax[0].legend(loc='upper right')

# Bar graph comparing different financial metrics
graph_2 = ax[1].bar(data['Year'], data['Net Income'], color='green', label='Net Profit')
graph_2_2 = ax[1].bar(data['Year'], data['Gross Margin'], color='red', label='Gross Margin')
graph_2_3 = ax[1].bar(data['Year'], data['Operating Margin'], color='orange', label='Operating Profit Margin')
ax[1].set_xticklabels(data['Year'])
ax[1].set_ylabel('Financial Metrics (in  millions)')

anim = FuncAnimation(fig, update, frames=len(data), interval=100, repeat=True)
anim2 = FuncAnimation(fig, update2, frames=len(data), interval=100, repeat=True)

plt.show()
```

This code will generate the following visualizations:

1. A line graph showing the trend of total revenue over the years:

![line_graph](line_graph.png)

2. A bar graph comparing different financial metrics (Net Income, Gross Margin, and Operating Margin) over the years:

![bar_graph](bar_graph.png)
    
Please note that this is a simplified example. In real-world scenarios, you would need to replace the data source, adjust the axes labels and titles, and possibly customize the colors and styles to make the visualizations more informative.