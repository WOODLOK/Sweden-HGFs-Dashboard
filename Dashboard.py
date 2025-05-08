import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.express as px
import squarify
import pandas as pd
import pydeck as pdk
import plotly.express as px
import altair as alt

# Define WHU color scheme
WHU_COLORS = {
    'PRIMARY': '#05467A',      # WHU Blue
    'SECONDARY': '#00A5DC',    # WHU Light Blue
    'ACCENT': '#4F2683',       # Kellogg Purple
    'BACKGROUND': '#E6EBEE',   # Silver Grey
    'TEXT_DARK': '#505459',    # Anthracite
    'TEXT_LIGHT': '#FFFFFF',   # White
    'CHART_COLORS': [
        '#05467A',  # WHU Blue
        '#00A5DC',  # WHU Light Blue
        '#4F2683',  # Kellogg Purple
        '#00BFB3',  # Turquoise
        '#FF8200',  # Orange
        '#7AB800',  # Green
        '#A81538',  # Red
        '#4B0082',  # Indigo
        '#FFD700',  # Gold
        '#2E8B57'   # Sea Green
    ]
}

# Page config with WHU styling
st.set_page_config(
    page_title="Sweden Company Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for WHU theme
st.markdown("""
    <style>
    /* Main page background */
    .stApp {
        background-color: rgba(230, 235, 238, 0.3) !important;  /* Changed from 0.7 to 0.3 opacity */
    }
    
    /* Top bar styling */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 70, 122, 0.95) !important;
    }
    
    /* Navigation title styling */
    .sidebar-title {
        color: white !important;
        font-weight: bold !important;
        font-size: 24px !important;
        margin: 20px 20px 30px 20px !important;
        padding: 0 !important;
    }

    /* Style radio buttons as modern buttons */
    section[data-testid="stSidebar"] .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 0 20px;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        font-size: 16px !important;
        padding: 10px 15px;
        border-radius: 4px;
        position: relative;
    }

    section[data-testid="stSidebar"] .stRadio input:checked + label {
        color: #05467A !important;
        background-color: white;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] .stRadio input:not(:checked) + label:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    /* Hide the radio button circle */
    section[data-testid="stSidebar"] .stRadio input {
        display: none;
    }

    /* Style the radio button text */
    section[data-testid="stSidebar"] .stRadio label div[data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        white-space: nowrap !important;
        width: 100% !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #05467A !important;
        font-family: Arial, sans-serif;
        font-size: 24px !important;
        padding: 20px 0 10px 0;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #e6e6e6;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 16px 0;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 16px;
        color: #505459;
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #05467A;
    }

    /* Section headers */
    .section-header {
        color: #05467A !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        margin: 24px 0 16px 0 !important;
        padding: 0 !important;
    }

    /* Table styling */
    .dataframe {
        background-color: #FFFFFF;
        border-radius: 8px;
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .dataframe th {
        background-color: #00A5DC;  /* WHU Light Blue */
        color: white;
        font-weight: 600;
        padding: 12px;
        text-align: center;
        border-bottom: 1px solid #E6E6E6;
    }
    .dataframe td {
        color: #505459;
        padding: 12px;
        text-align: center;
        border-bottom: 1px solid #F0F0F0;
    }
    .dataframe tr:nth-child(even) {
        background-color: rgba(0, 165, 220, 0.1);  /* WHU Light Blue with opacity */
    }
    .dataframe tr:nth-child(odd) {
        background-color: #FFFFFF;
    }
    .dataframe tr:hover {
        background-color: rgba(0, 165, 220, 0.15);
    }
    .topic-tag {
        background-color: #e6f3ff;
        color: #0066cc;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 2px;
        display: inline-block;
    }

    /* Chart text colors */
    .vega-embed .vega-title, .vega-embed .vega-text {
        fill: #05467A !important;
    }
    .vega-embed .vega-axis-title, .vega-embed .vega-axis-label {
        fill: #505459 !important;
    }
    .vega-embed .vega-legend-title, .vega-embed .vega-legend-label {
        fill: #505459 !important;
    }

    /* Navigation button fix */
    .nav-button {
        background-color: transparent;
        border: none;
        color: white !important;
        cursor: pointer;
        display: block;
        font-size: 16px;
        margin: 5px 0;
        padding: 10px 15px;
        text-align: left;
        width: 100%;
        border-radius: 4px;
        transition: all 0.3s ease;
    }

    .nav-button:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    .nav-button.active {
        background-color: white;
        color: #05467A !important;
        font-weight: 500;
    }

    /* Keep sidebar text white */
    section[data-testid="stSidebar"] {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    section[data-testid="stSidebar"] p {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Custom CSS for sidebar
st.markdown("""
    <style>
    /* Sidebar title */
    .sidebar-title {
        color: white !important;
        font-weight: bold !important;
        font-size: 24px !important;
        margin: 20px 0 30px 20px !important;
        padding: 0 !important;
    }

    /* Move radio buttons to align with Navigation text */
    section[data-testid="stSidebar"] .stRadio > div {
        padding-left: 20px !important;
    }

    /* Style radio buttons */
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_excel("Sweden_merged_with_all_topics_and_growth_category.xlsx")
    df["Company Age"] = 2023 - df["Founded Year"]
    return df

# Load data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Sidebar navigation with title
st.sidebar.markdown('<p class="sidebar-title">Navigation</p>', unsafe_allow_html=True)

# Replace custom navigation with Streamlit radio buttons
page = st.sidebar.radio("", ["General Analytics", "Topic Dispersion", "Geological Dispersion", "Age Dispersion"], label_visibility="collapsed")

if page == "General Analytics":
    # General Analytics Dashboard
    st.title("🏢 General Company Analytics")
    
    # Custom CSS for card-like metrics
    st.markdown("""
        <style>
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #e6e6e6;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        .metric-title {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #333;
        }
        .metric-tags {
            margin-top: 10px;
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .topic-tag {
            background-color: #e6f3ff;
            color: #0066cc;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Summary metrics in cards
    col1, col2, col3 = st.columns(3)
    
    # Total Companies card
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">📊 Total Companies</div>
                <div class="metric-value">{len(df):,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Average Company Age card
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">⏳ Average Company Age</div>
                <div class="metric-value">{df['Company Age'].mean():.1f} years</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Top Topics card with tags
    with col3:
        # Get top 3 topics with full names
        all_topics = sum([x.split('; ') for x in df["All Topics"].dropna()], [])
        top_topics = pd.Series(all_topics).value_counts().head(3)
        
        # Create HTML for topic tags
        topic_tags_html = ''.join([f'<span class="topic-tag">#{topic}</span>' for topic in top_topics.index])
        
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🏷️ Popular Topics</div>
                <div class="metric-tags">
                    {topic_tags_html}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Create two rows with two columns each for the charts
    row1_col1, row1_col2 = st.columns(2)
    
    # Regional Distribution
    with row1_col1:
        st.markdown('<h3 class="section-header">Regional Distribution</h3>', unsafe_allow_html=True)
        region_counts = df["Region in country clean"].value_counts().reset_index()
        region_counts.columns = ["Region", "Count"]
        chart = alt.Chart(region_counts).mark_arc(
            innerRadius=50,
            cornerRadius=4,
            stroke='#E6EBEE',  # Match the main background color
            strokeWidth=2
        ).encode(
            theta="Count:Q",
            color=alt.Color(
                "Region:N",
                scale=alt.Scale(range=WHU_COLORS['CHART_COLORS']),
                legend=alt.Legend(
                    orient="right", 
                    labelLimit=200,
                    fillColor='transparent',  # Use transparent instead of None
                    padding=10,
                    strokeColor='transparent'  # Use transparent instead of None
                )
            ),
            tooltip=["Region", "Count"]
        ).properties(
            height=300,
            background='transparent'  # Use transparent instead of None
        ).configure_view(
            strokeWidth=0
        )
        st.altair_chart(chart, use_container_width=True)

    # Top Topics
    with row1_col2:
        st.markdown('<h3 class="section-header">Top Topics</h3>', unsafe_allow_html=True)
        topic_series = pd.Series(all_topics)
        topic_counts = topic_series.value_counts().head(10)
        
        # Create figure with transparent background
        plt.figure(figsize=(10, 6), facecolor='none')
        
        # Define shorter but accurate names for topics
        topic_name_mapping = {
            'professional, scientific, & technical services': 'Tech Services',
            'information technology': 'IT',
            'software': 'Software',
            'business services': 'Business',
            'manufacturing': 'Manufacturing',
            'industrial': 'Industrial',
            'healthcare': 'Healthcare',
            'financial services': 'Finance',
            'retail': 'Retail',
            'education': 'Education',
            'telecommunications': 'Telecom',
            'construction': 'Construction',
            'transportation': 'Transport',
            'real estate': 'Real Estate',
            'media': 'Media',
            'amusement park & leisure destination management': 'Leisure',
            'consumer lending & financial services': 'Consumer Finance',
            'advanced technical products & services': 'Tech Products',
            'construction information & business intelligence': 'Construction Info',
            'healthcare staffing & recruitment services': 'Health Staff',
            'it services & digital transformation': 'IT Services'
        }
        
        # Create labels first
        labels = []
        tooltip_data = []  # Store data for tooltips
        
        # Sort topics by count to identify top two
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        
        for topic, count in topic_counts.items():
            # Store full data for tooltips
            tooltip_data.append((topic, count))
            
            if topic in [sorted_topics[0][0], sorted_topics[1][0]]:
                labels.append(f'{topic}\n{count}')
            else:
                # For other blocks, use shortened name
                short_name = topic_name_mapping.get(topic.lower(), topic)
                # Split into two lines if needed
                if len(short_name) > 8:
                    labels.append(f'{short_name}\n{count}')
                else:
                    labels.append(f'{short_name} {count}')
        
        # Replace labels for specific topics with just their counts
        for i, (topic, count) in enumerate(topic_counts.items()):
            if topic.lower() == 'passenger land transportation' or topic.lower() == 'commercial real estate acquisition':
                labels[i] = str(count)
        
        # Create color gradient from light blue to WHU blue
        colors = [f'#{int(5 + (179-5)*i/9):02x}{int(70 + (199-70)*i/9):02x}{int(122 + (214-122)*i/9):02x}'
                 for i in range(len(topic_counts))]
        
        # Create treemap with adjusted text size based on rectangle size
        rects = squarify.plot(sizes=topic_counts.values,
                     label=labels,
                     color=colors,
                     alpha=0.9,
                     pad=0,  # No padding between blocks
                     text_kwargs={'color': 'white',
                                'fontsize': 10,  # Increased font size from 8 to 10
                                'fontweight': 'bold'})  # Remove ha parameter since it's handled internally
        
        # Add tooltips
        def on_hover(event):
            if event.inaxes:
                for i, rect in enumerate(rects):
                    if rect.contains(event)[0]:
                        topic, count = tooltip_data[i]
                        # Create a text box for the tooltip with larger font
                        bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec="gray", alpha=0.9)
                        plt.gca().text(0.5, 1.05, f'{topic}\nCount: {count}', 
                                     transform=plt.gca().transAxes,
                                     ha='center',
                                     va='bottom',
                                     bbox=bbox_props,
                                     fontsize=12)  # Increased tooltip font size from 10 to 12
                        plt.draw()
                        break
                else:
                    # Clear any existing tooltip
                    for text in plt.gca().texts:
                        text.set_visible(False)
                    plt.draw()
        
        # Connect the hover event
        plt.connect('motion_notify_event', on_hover)
        
        plt.axis('off')
        plt.tight_layout()
        
        # Display the plot in Streamlit
        st.pyplot(plt.gcf())
        
        # Clear the current figure
        plt.close()

    row2_col1, row2_col2 = st.columns(2)

    # Age Distribution
    with row2_col1:
        st.markdown('<h3 class="section-header">Age Distribution</h3>', unsafe_allow_html=True)
        
        # Define custom bins and labels
        bins = [0, 5, 10, 20, 30, 50, 100]
        labels = ['0-5', '5-10', '10-20', '20-30', '30-50', '50-100']
        
        # Create age bins with custom ranges
        df['Age Bin'] = pd.cut(df['Company Age'], 
                             bins=bins,
                             labels=labels,
                             include_lowest=True)
        
        # Calculate counts for each bin
        age_dist = df['Age Bin'].value_counts().sort_index().reset_index()
        age_dist.columns = ['Age Group', 'Count']
        
        # Create the pyramid chart
        chart = alt.Chart(age_dist).mark_bar(
            cornerRadius=4,
            color=WHU_COLORS['PRIMARY']  # WHU Blue
        ).encode(
            x=alt.X('Count:Q',
                   axis=alt.Axis(title='Number of Companies'),
                   scale=alt.Scale(domain=[0, age_dist['Count'].max()])),
            y=alt.Y('Age Group:N',
                   sort=labels[::-1],
                   axis=alt.Axis(title=None)),
            tooltip=['Age Group', 'Count']
        ).properties(
            height=300,
            background='transparent'
        ).configure_axis(
            grid=True,
            gridColor='rgba(80, 84, 89, 0.1)'
        ).configure_view(
            stroke=None
        )
        
        st.altair_chart(chart, use_container_width=True)

    # Founding Trends
    with row2_col2:
        st.markdown('<h3 class="section-header">Founding Trends</h3>', unsafe_allow_html=True)
        # Filter data from 1925 to 2020
        yearly_data = df[(df["Founded Year"] >= 1925) & (df["Founded Year"] <= 2020)].copy()
        year_range = pd.DataFrame({'Year': range(1925, 2021)})
        yearly_counts = yearly_data["Founded Year"].value_counts().reset_index()
        yearly_counts.columns = ["Year", "Count"]
        # Merge with full year range to include years with zero counts
        yearly_counts = pd.merge(year_range, yearly_counts, on="Year", how="left").fillna(0)
        yearly_counts = yearly_counts.sort_values("Year")
        
        base = alt.Chart(yearly_counts).encode(
            x=alt.X("Year:Q", title="Year", scale=alt.Scale(domain=[1925, 2020])),
            y=alt.Y("Count:Q", title="Number of Companies")
        )

        line = base.mark_line(
            color=WHU_COLORS['PRIMARY'],  # WHU Blue
            strokeWidth=3
        )

        points = base.mark_circle(
            color=WHU_COLORS['PRIMARY'],  # WHU Blue
            size=50
        ).encode(
            tooltip=["Year:Q", "Count:Q"]
        )

        chart = (line + points).properties(
            height=300,
            background='transparent'
        ).configure_view(
            strokeWidth=0
        )
        st.altair_chart(chart, use_container_width=True)

    # Employee Table with improved formatting
    with st.container():
        st.markdown('<h3 class="section-header">Top Companies by Employee Count</h3>', unsafe_allow_html=True)
        employee_df = df[["Company name Latin alphabet", "Number of employees 2023", "City Latin Alphabet", "All Topics"]].copy()
        employee_df = employee_df.sort_values("Number of employees 2023", ascending=False).head(10).reset_index(drop=True)
        
        # Add ranking column starting from 1
        employee_df.index = range(1, len(employee_df) + 1)
        
        # Format the DataFrame
        employee_df = employee_df.rename(columns={
            'Company name Latin alphabet': 'Company',
            'Number of employees 2023': 'Employees',
            'City Latin Alphabet': 'Location',
            'All Topics': 'Sectors'
        })

        # Custom CSS for the table
        st.markdown("""
        <style>
        .employee-table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background-color: white;
        }
        .employee-table th {
            background-color: #00A5DC;
            color: white;
            font-weight: 700;  /* Make text bold */
            text-align: center;  /* Center align header text */
            padding: 12px 15px;
            font-size: 14px;
            vertical-align: middle;  /* Vertically center text */
        }
        .employee-table td {
            padding: 12px 15px;
            font-size: 14px;
            color: #333;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        .employee-table tr:nth-child(even) {
            background-color: rgba(128, 128, 128, 0.1);  /* Grey with 10% opacity */
        }
        .employee-table .sector-tag {
            display: inline-block;
            background-color: #e8f4f8;
            color: #0066cc;
            padding: 4px 8px;
            margin: 2px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
        }
        </style>
        """, unsafe_allow_html=True)

        # Convert DataFrame to HTML with custom formatting
        def format_sectors(sectors):
            if pd.isna(sectors):
                return ''
            tags = [f'<span class="sector-tag">#{topic.strip()}</span>' for topic in sectors.split(';')]
            return ' '.join(tags)

        # Create HTML table manually
        html_table = '<table class="employee-table">'
        # Headers
        html_table += '<tr><th></th><th>Company</th><th>Employees</th><th>Location</th><th>Sectors</th></tr>'
        
        # Rows
        for idx, row in employee_df.iterrows():
            html_table += f'<tr>'
            html_table += f'<td>{idx}</td>'  # Ranking
            html_table += f'<td>{row["Company"]}</td>'
            html_table += f'<td>{int(row["Employees"]):,}</td>'
            html_table += f'<td>{row["Location"]}</td>'
            html_table += f'<td>{format_sectors(row["Sectors"])}</td>'
            html_table += '</tr>'
        
        html_table += '</table>'
        
        st.markdown(html_table, unsafe_allow_html=True)

elif page == "Topic Dispersion":
    # Topic Dispersion
    st.title("Topic Dispersion")

    # Get all topics and their counts for Top N calculations
    all_topics = sum([x.split('; ') for x in df["All Topics"].dropna()], [])
    topic_counts = pd.Series(all_topics).value_counts()
    all_unique_topics = sorted(set(all_topics))
    
    # Topic selection filter with "Select All" option
    st.subheader("Topic Filter")
    col1, col2 = st.columns([2, 1])
    with col1:
        select_all = st.checkbox("Select All Topics", value=True)
    with col2:
        top_n = st.slider("Number of top topics to compare", 5, 20, 10)

    if select_all:
        selected_topics = all_unique_topics
    else:
        selected_topics = st.multiselect("Select Topics to Analyze", all_unique_topics)

    if not selected_topics:
        st.warning("Please select at least one topic to analyze")
        st.stop()

    # Get top N topics
    top_n_topics = topic_counts.head(top_n).index.tolist()

    # Create two rows with two columns each for the analysis
    row1_col1, row1_col2 = st.columns(2)

    # Average Company Age Analysis
    with row1_col1:
        st.subheader("Average Company Age by Topic")
        
        # Calculate ages for top N topics
        top_n_ages = []
        for topic in top_n_topics:
            topic_companies = df[df["All Topics"].str.contains(topic, na=False)]
            avg_age = topic_companies["Company Age"].mean()
            top_n_ages.append({"Topic": topic, "Average Age": avg_age, "Category": f"Top {top_n} Topics"})
        
        # Calculate ages for selected topics (if different from top N)
        selected_ages = []
        if not select_all:
            for topic in selected_topics:
                if topic not in top_n_topics:
                    topic_companies = df[df["All Topics"].str.contains(topic, na=False)]
                    avg_age = topic_companies["Company Age"].mean()
                    selected_ages.append({"Topic": topic, "Average Age": avg_age, "Category": "Selected Topics"})
        
        # Combine data
        age_df = pd.DataFrame(top_n_ages + selected_ages)
        
        # Create chart with WHU colors
        chart = alt.Chart(age_df).mark_bar().encode(
            x=alt.X("Topic:N", sort="-y"),
            y="Average Age:Q",
            color=alt.Color("Category:N", scale=alt.Scale(
                range=[WHU_COLORS['PRIMARY'], WHU_COLORS['SECONDARY']]
            )),
            tooltip=["Topic", "Average Age", "Category"]
        ).properties(
            height=300,
            background='transparent'
        ).configure_view(
            strokeWidth=0
        )
        st.altair_chart(chart, use_container_width=True)

    # Number of Employees Analysis
    with row1_col2:
        st.subheader("Total Employees by Topic")
        
        # Calculate employees for top N topics
        top_n_employees = []
        for topic in top_n_topics:
            topic_companies = df[df["All Topics"].str.contains(topic, na=False)]
            total_employees = topic_companies["Number of employees 2023"].sum()
            top_n_employees.append({"Topic": topic, "Total Employees": total_employees, "Category": f"Top {top_n} Topics"})
        
        # Calculate employees for selected topics
        selected_employees = []
        if not select_all:
            for topic in selected_topics:
                if topic not in top_n_topics:
                    topic_companies = df[df["All Topics"].str.contains(topic, na=False)]
                    total_employees = topic_companies["Number of employees 2023"].sum()
                    selected_employees.append({"Topic": topic, "Total Employees": total_employees, "Category": "Selected Topics"})
        
        # Combine data
        emp_df = pd.DataFrame(top_n_employees + selected_employees)
        
        # Create chart with WHU colors
        chart = alt.Chart(emp_df).mark_bar().encode(
            x=alt.X("Topic:N", sort="-y"),
            y="Total Employees:Q",
            color=alt.Color("Category:N", scale=alt.Scale(
                range=[WHU_COLORS['PRIMARY'], WHU_COLORS['SECONDARY']]
            )),
            tooltip=["Topic", "Total Employees", "Category"]
        ).properties(
            height=300,
            background='transparent'
        ).configure_view(
            strokeWidth=0
        )
        st.altair_chart(chart, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    # Growth Categories Analysis
    with row2_col1:
        st.subheader("Companies in Growth Categories by Topic")
        
        # Define all growth categories
        growth_categories = ['Gazelle', 'Mature', 'Scaleup', 'Superstar']
        
        # Calculate growth for top N topics
        top_n_growth = []
        for topic in top_n_topics:
            topic_companies = df[df["All Topics"].str.contains(topic, na=False)]
            for category in growth_categories:
                count = topic_companies[topic_companies["Growth Category"] == category].shape[0]
                top_n_growth.append({
                    "Topic": topic,
                    "Growth Category": category,
                    "Count": count,
                    "Is Selected": False
                })
        
        # Add selected topics
        if not select_all:
            for topic in selected_topics:
                if topic not in top_n_topics:
                    topic_companies = df[df["All Topics"].str.contains(topic, na=False)]
                    for category in growth_categories:
                        count = topic_companies[topic_companies["Growth Category"] == category].shape[0]
                        top_n_growth.append({
                            "Topic": topic,
                            "Growth Category": category,
                            "Count": count,
                            "Is Selected": True
                        })
        
        # Create dataframe and sort topics
        growth_df = pd.DataFrame(top_n_growth)
        topic_totals = growth_df.groupby("Topic")["Count"].sum().sort_values(ascending=False)
        topic_order = topic_totals.index.tolist()
        
        # Create chart with WHU colors
        chart = alt.Chart(growth_df).mark_bar().encode(
            x=alt.X("Topic:N", sort=topic_order),
            xOffset="Growth Category:N",
            y=alt.Y("Count:Q"),
            color=alt.Color("Growth Category:N", scale=alt.Scale(
                domain=growth_categories,
                range=[
                    WHU_COLORS['PRIMARY'],      # WHU Blue
                    WHU_COLORS['SECONDARY'],    # WHU Light Blue
                    WHU_COLORS['ACCENT'],       # Kellogg Purple
                    WHU_COLORS['CHART_COLORS'][3]  # Turquoise
                ]
            )),
            opacity=alt.condition(
                alt.datum["Is Selected"],
                alt.value(1),
                alt.value(0.6)
            ),
            tooltip=["Topic", "Growth Category", "Count"]
        ).properties(
            height=300,
            background='transparent'
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            labelAngle=45
        )
        st.altair_chart(chart, use_container_width=True)

    # Customer Segments Analysis
    with row2_col2:
        st.subheader("Customer Segments by Topic")
        if "Customer Segment" in df.columns:
            # Define all possible customer segments
            all_segments = ['B2B', 'B2C', 'B2G']
            
            # Calculate segments for top N topics
            top_n_segments = []
            for topic in top_n_topics:
                topic_companies = df[df["All Topics"].str.contains(topic, na=False)]
                for segment in all_segments:
                    count = topic_companies[topic_companies["Customer Segment"].str.contains(segment, na=False)].shape[0]
                    top_n_segments.append({
                        "Topic": topic,
                        "Segment": segment,
                        "Count": count,
                        "Is Selected": False
                    })
            
            # Add selected topics
            if not select_all:
                for topic in selected_topics:
                    if topic not in top_n_topics:
                        topic_companies = df[df["All Topics"].str.contains(topic, na=False)]
                        for segment in all_segments:
                            count = topic_companies[topic_companies["Customer Segment"].str.contains(segment, na=False)].shape[0]
                            top_n_segments.append({
                                "Topic": topic,
                                "Segment": segment,
                                "Count": count,
                                "Is Selected": True
                            })
            
            # Create dataframe and sort topics
            segment_df = pd.DataFrame(top_n_segments)
            topic_totals = segment_df.groupby("Topic")["Count"].sum().sort_values(ascending=False)
            topic_order = topic_totals.index.tolist()
            
            # Create chart with WHU colors
            chart = alt.Chart(segment_df).mark_bar().encode(
                x=alt.X("Topic:N", sort=topic_order),
                xOffset="Segment:N",
                y=alt.Y("Count:Q"),
                color=alt.Color("Segment:N", scale=alt.Scale(
                    domain=['B2B', 'B2C', 'B2G'],
                    range=[
                        WHU_COLORS['PRIMARY'],    # WHU Blue
                        WHU_COLORS['SECONDARY'],  # WHU Light Blue
                        WHU_COLORS['ACCENT']      # Kellogg Purple
                    ]
                )),
                opacity=alt.condition(
                    alt.datum["Is Selected"],
                    alt.value(1),
                    alt.value(0.6)
                ),
                tooltip=["Topic", "Segment", "Count"]
            ).properties(
                height=300,
                background='transparent'
            ).configure_view(
                strokeWidth=0
            ).configure_axis(
                labelAngle=45
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Customer Segment data not available in the dataset")


elif page == "Geological Dispersion":
    st.title("Geological Dispersion")
    
    df_geo = pd.read_csv("Sweden_final_coordinates_complete.csv")
    df_geo = df_geo.dropna(subset=["latitude", "longitude"])

    # ---  Map part (3D Hexagon Layer) ---
    st.subheader("3D Heatmap of High-Growth Firms in Sweden")

    view_state = pdk.ViewState(
        latitude=62.0,
        longitude=17.0,
        zoom=4.5,
        pitch=60,
        bearing=0,
    )

    hex_layer = pdk.Layer(
        "HexagonLayer",
        data=df_geo,
        get_position='[longitude, latitude]',
        radius=7000,
        elevation_scale=80,
        elevation_range=[0, 3000],
        pickable=True,
        extruded=True,
        coverage=1,
        auto_highlight=True,
    )

    r = pdk.Deck(
        layers=[hex_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={"text": "{position}"}
    )

    st.pydeck_chart(r)

    st.markdown("---")

  
    st.subheader("Regional Distribution (Altair View)")

    region_counts_alt = df_geo["Region in country clean"].value_counts().reset_index()
    region_counts_alt.columns = ["Region", "Count"]

    chart = alt.Chart(region_counts_alt).mark_arc(
        innerRadius=50,
        cornerRadius=4,
        stroke='#E6EBEE',
        strokeWidth=2
    ).encode(
        theta="Count:Q",
        color=alt.Color(
            "Region:N",
            scale=alt.Scale(range=WHU_COLORS['CHART_COLORS']),
            legend=alt.Legend(
                orient="right",
                labelLimit=200,
                fillColor='transparent',
                padding=10,
                strokeColor='transparent'
            )
        ),
        tooltip=["Region", "Count"]
    ).properties(
        height=300,
        background='transparent'
    ).configure_view(
        strokeWidth=0
    )

    st.altair_chart(chart, use_container_width=True)

  
    st.markdown("---")
    st.subheader("Regional Distribution by Category")

    col1, col2 = st.columns(2)

    with col1:
        category = st.selectbox(
            "Select a category to filter:",
            ["Growth Category", "Customer Segment"]
        )

    with col2:
        options = sorted(df_geo[category].dropna().unique())
        selected = st.multiselect(
            f"Select {category} group(s):",
            options,
            default=options[:2]
        )

    df_filtered = df_geo[df_geo[category].isin(selected)]

    region_group = df_filtered["Region in country clean"].value_counts().reset_index()
    region_group.columns = ["Region", "Company Count"]

    fig = px.bar(
        region_group,
        x="Region",
        y="Company Count",
        title=f"Company Distribution by Region for selected {category}",
        labels={"Company Count": "Number of Companies"},
        color_discrete_sequence=["#1f77b4"]
    )

    st.plotly_chart(fig, use_container_width=True)




elif page == "Age Dispersion":
    st.title("Age Dispersion")

    import plotly.express as px

    st.markdown("## Company Age Distribution by Category")


    col1, col2 = st.columns(2)

    with col1:
        category_col = st.selectbox(
            "Choose comparison dimension:",
            ["Growth Category", "Customer Segment"]
        )

    with col2:
        group_options = sorted(df[category_col].dropna().unique())
        selected_groups = st.multiselect(
            f"Select {category_col} groups:",
            options=group_options,
            default=group_options[:2]
        )

  
    df_density = df[df[category_col].isin(selected_groups)]
    df_density = df_density[df_density["Company Age"].notna()]

    st.markdown("---")

    # ---  Box Plot ---
    st.subheader("Company Age: Median & Range View")
    fig_box = px.box(
        df_density,
        x=category_col,
        y="Company Age",
        color=category_col,
        hover_data=["Company name Latin alphabet", "Number of employees 2023", "Customer Segment"],
        height=400
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # ---  Strip Plot ---
    st.subheader("Individual Age of all companies")
    fig_strip = px.strip(
        df_density,
        x=category_col,
        y="Company Age",
        color=category_col,
        hover_data=["Company name Latin alphabet", "Number of employees 2023", "Customer Segment"],
        stripmode="overlay",
        height=400
    )
    st.plotly_chart(fig_strip, use_container_width=True)




# Update chart configurations
def configure_chart_theme(chart):
    return chart.configure_view(
        strokeWidth=0,
        backgroundColor='rgba(230, 235, 238, 0.5)'  # Semi-transparent background
    ).configure_axis(
        labelColor=WHU_COLORS['TEXT_DARK'],
        titleColor=WHU_COLORS['TEXT_DARK'],
        gridColor='rgba(80, 84, 89, 0.1)',
        labelFontSize=16,
        titleFontSize=16
    ).configure_legend(
        labelColor=WHU_COLORS['TEXT_DARK'],
        titleColor=WHU_COLORS['TEXT_DARK'],
        padding=10,
        labelFontSize=16,
        symbolStrokeWidth=2,
        cornerRadius=4
    ).configure_title(
        fontSize=20,
        color=WHU_COLORS['PRIMARY']
    )

# Update chart colors and styling
def create_bar_chart(data, x_field, y_field, title=None):
    return alt.Chart(data).mark_bar(
        color=WHU_COLORS['PRIMARY']
    ).encode(
        x=alt.X(x_field, title=None),
        y=alt.Y(y_field, title=None),
        tooltip=[x_field, y_field]
    ).properties(
        title=title,
        height=300
    ).configure_view(
        strokeWidth=0
    )

# Wrap each chart section in a container
def create_chart_section(title, chart):
    st.markdown(f"""
        <div class="chart-container">
            <h3>{title}</h3>
        </div>
    """, unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True) 