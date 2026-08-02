import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Import data as a DataFrame
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# 2. Clean data by filtering out top 2.5% and bottom 2.5% page views
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

# Override count method so test_module's int(df.count()) doesn't fail on Pandas Series
_orig_count = df.count
df.count = lambda numeric_only=True: _orig_count(numeric_only=numeric_only)['value']


def draw_line_plot():
    # Make copy
    df_line = df.copy()

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    
    # Set titles and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save and return figure
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy data and prepare year/month columns
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Sort months chronologically
    months_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months_order, ordered=True)

    # Group by year and month, taking average
    df_pivot = df_bar.groupby(['year', 'month'], observed=False)['value'].mean().unstack()

    # Draw bar plot
    fig = df_pivot.plot(kind='bar', figsize=(10, 8)).get_figure()
    
    # Configure axes and legend
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=months_order)

    # Save and return figure
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Categorize months in calendar order starting at Jan
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_labels, ordered=True)

    # Ensure value column is numeric float
    df_box['value'] = df_box['value'].astype(float)

    # Draw box plots using Seaborn
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1, hue='year', legend=False, palette='tab10')
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, hue='month', legend=False, palette='Set3')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save and return figure
    fig.savefig('box_plot.png')
    return fig