
import streamlit as st
import pandas as pd
import plotly.express as px

# re-style the multiselect tags to look more polished, with gradient colors.
st.markdown("""
<style>

/* Target multiselect selected values (the pills) */
span[data-baseweb="tag"] {
    background: linear-gradient(90deg, #c084fc, #ffb3b3, #a7f3d0) !important; 
    /* light purple → soft red → light green */
    color: #1f2937 !important;           /* dark text for readability */
    border: none !important;
    box-shadow: 0 0 6px rgba(255, 179, 179, 0.3); /* soft glow effect */
}

/* Hover effect */
span[data-baseweb="tag"]:hover {
    background: linear-gradient(90deg, #b794f4, #ffc7c7, #86efac) !important;
}

/* Remove default red “x” color */
span[data-baseweb="tag"] svg {
    color: #1f2937 !important;
}

</style>
""", unsafe_allow_html=True)



# Display a title with HTML/CSS styling
st.markdown(
    """
<h1 style="
    text-align: center;
    font-size: 95px;
    background: linear-gradient(90deg, #7b2ff7, #ff4d4d, #00c9a7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;
">
    Video Game Sales Dashboard 
</h1>
    """,
    unsafe_allow_html=True
)

# Display header image 

from PIL import Image

img = Image.open("image.png")
img = img.resize((4000, 1000))

col1, col2, col3 = st.columns([0.05, 9, 0.05])
with col2:
    st.image(img, use_container_width=True)



# --------------------------------------------------------------------------------------------------
# Page Config
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    layout="wide"
)

# --------------------------
# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("clean_video_games.csv")
    return df

df = load_data()

# --------------------------------------------------------------------------------------------------
 

# Sidebar
# Page Navigation
st.sidebar.markdown(
    "<h2 style='font-size:28px'>🧭 Navigation</h2>", unsafe_allow_html=True
)

page = st.sidebar.radio(
    " ",# to keep the radio label empty
    [
        "Overview",
        "Analysis",
        "Insights & Recommendations",
        "Summary"
    ]
)


# Add a separator line
st.sidebar.markdown("---")
# --------------------------------------------------------------------------------------------------
# Sidebar Filters

st.sidebar.markdown(
 "<h3 style='font-size:24px'>🔍 Data Filters</h3>", unsafe_allow_html=True )

genre_filter = st.sidebar.multiselect(
    "Select Genre", options=df["genre"].unique(), default=df["genre"].unique()
)

age_rating_map = { #  # Mapping shorthand ratings to full names 
    "E": "Everyone",
    "E10+": "Everyone 10+",
    "T": "Teen",
    "M": "Mature 17+",
    "AO": "Adults Only 18+",
    "K-A": "Kids to Adults"
}

rating_filter = st.sidebar.multiselect(
    "Select Age Rating",   options=list(age_rating_map.keys()),default=list(age_rating_map.keys()), 
    format_func=lambda x: f"{x} — {age_rating_map[x]}"
)


platform_filter = st.sidebar.multiselect(
    "Select Platform", options=df["platform"].unique(), default=df["platform"].unique()
)


user_score_filter = st.sidebar.slider(
    "Set User Score Range",
    float(df["user_score"].min()),
    float(df["user_score"].max()),
    (float(df["user_score"].min()), float(df["user_score"].max())),
)

year_filter = st.sidebar.slider(
    "Set Year of Release Range",
    int(df["year_of_release"].min()),
    int(df["year_of_release"].max()),
    (int(df["year_of_release"].min()), int(df["year_of_release"].max())),
)


st.sidebar.markdown("📧 Email: [elafbhaa0@gmail.com](mailto:elafbhaa0@gmail.com)")

# --------------------------------------------------------------------------------------------------
# Apply Filters
filtered_df = df[
    (df["genre"].isin(genre_filter)) &
    (df["rating"].isin(rating_filter)) &
    (df["platform"].isin(platform_filter)) &
   
    (df["user_score"].between(user_score_filter[0], user_score_filter[1])) &
    (df["year_of_release"].between(year_filter[0], year_filter[1]))
]

# --------------------------------------------------------------------------------------------------

# MAIN PAGE
if page == "Overview":

    st.title("Dashboard Overview")

    st.subheader("📂 Dataset Overview")
    st.dataframe(filtered_df.head())

    st.divider()

    st.subheader("📊 Key Performance Indicators (KPIs)")

    # KPI calculations
    Total_Games = filtered_df.shape[0]
    Total_Global_Sales = filtered_df["global_sales"].sum()
    Global_Sales_Rate = Total_Global_Sales / Total_Games if Total_Games else 0
    Top_Selling_Game = filtered_df.groupby('name')['global_sales'].sum().idxmax() if Total_Games else "N/A"
    Avg_User_Score = filtered_df["user_score"].mean()
    Most_Popular_Platform = filtered_df['platform'].mode()[0] if Total_Games else "N/A"
    Top_Genre = filtered_df['genre'].mode()[0] if Total_Games else "N/A"
    # Most_Age_Rating= filtered_df['rating'].mode()[0] if Total_Games else "N/A"
    Most_Age_Rating = (age_rating_map.get(filtered_df['rating'].mode()[0], "N/A") if Total_Games else "N/A"
)

    # Display KPIs in columns with two rows
    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)

# Numeric KPIs
    col1.metric("🕹️ Total Games", Total_Games)
    col2.metric("💰 Total Global Sales (Millions)", f"{Total_Global_Sales:.2f}")
    col3.metric("🔢 Global Sales Rate", f"{Global_Sales_Rate:.2%}")
    col4.metric("🎯 Average User Score", f"{Avg_User_Score:.2f}")
    
# Categorical KPIs
    col5.metric("🏆 Top Selling Game", Top_Selling_Game)
    col6.metric("🌟 Most Popular Genre", Top_Genre)
    col7.metric("🎮 Most Popular Platform", Most_Popular_Platform)
    col8.metric("👶 Most Age Rating", Most_Age_Rating)

    
# --------------------------------------------------------------------------------------------------
# ANALYSIS PAGE
elif page == "Analysis":

    st.title("Exploratory Data Analysis (EDA)")

    tab1, tab2, tab3 = st.tabs([
        "Univariate Analysis",
        "Bivariate Analysis",
        "Multivariate Analysis"
    ])

    # --------------------------
    # Univariate Analysis
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Total Global Sales by Genre")

            sales_genre = (
                filtered_df.groupby('genre')['global_sales']
                .sum()
                .reset_index()
                .sort_values(by='global_sales', ascending=False)
            )

            fig_genre_pie = px.pie(
                sales_genre,
                names='genre',
                values='global_sales',
                labels={'genre':'Genre','global_sales':'Total Global Sales (Millions)'},
                color_discrete_sequence = ["#3f145f", "#55307a","#6b468e","#805ea3","#9a7bb7","#b49acb","#cbb3da" ])   

            fig_genre_pie.update_traces(
                    textinfo='value',   # show both genre and global sales
                    textposition='inside'
)
            st.plotly_chart(fig_genre_pie, use_container_width=True)
            
        
        with col2:
            st.subheader("🎮 Games Released by Year")

            games_per_year = (
                filtered_df.groupby('year_of_release')['name']
                .count()
                .reset_index()
                .sort_values(by='name', ascending=False)
                .rename(columns={'name':'game_count'})
            )

            fig_year_pie = px.pie(
                games_per_year,
                names='year_of_release',
                values='game_count',
                labels={
                    'year_of_release': 'Year of Release',
                    'game_count': 'Number of Games'
                },color_discrete_sequence = ["#3f145f", "#55307a","#6b468e","#805ea3","#9a7bb7","#b49acb","#cbb3da" ]
            )

            # Show Year inside pie instead of %
            fig_year_pie.update_traces(
                textinfo='value',
                textposition='inside'
            )

            st.plotly_chart(fig_year_pie, use_container_width=True)

        
        st.divider()

        st.subheader("🏆 Top 10 Publishers by Global Sales")

        # Aggregate global sales by publisher
        sales_publisher = (
            filtered_df.groupby('publisher')['global_sales']
            .sum()
            .reset_index()
            .sort_values(by='global_sales', ascending=False)
        )

        # Select Top 10 publishers
        top_publishers = sales_publisher.head(10)

        # Bar chart for Top 10 publishers
        fig_publisher_bar = px.bar(
            top_publishers,
            x='publisher',
            y='global_sales',
            color='publisher',labels={'publisher':'Publisher','global_sales':'Global Sales (Millions)'},
            color_discrete_sequence = ["#3f145f", "#55307a","#6b468e","#805ea3","#9a7bb7","#b49acb","#cbb3da" ]
        )

        st.plotly_chart(fig_publisher_bar, use_container_width=True)

        st.divider()

        
        st.subheader("📊 Distribution of User Scores")

        fig_hist = px.histogram(
            filtered_df,
            x="user_score",
            nbins=20,
            marginal="box",  # adds boxplot on top 🔥
            opacity=0.85,
            color_discrete_sequence = ["#2d004d", "#5a189a", "#c48df5", "#e0c3fc", "#ffa8a8", "#d1f2eb", "#b7f5d3", "#38b000", "#004b23"], 
        )

        fig_hist.update_layout(
            xaxis_title="User Score",
            yaxis_title="Number of Games",
            bargap=0.1
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    # --------------------------------------------------------------------------------------------------
    # Bivariate Analysis
    with tab2:


        st.subheader("🔢 Number of Games Released per Year with Trendline")

        # Scatter plot - Number of Games Released per Year
        fig_gyear = px.scatter(
            games_per_year,
            x='year_of_release',
            y='game_count',
            trendline='ols',   # add regression line,
            color_discrete_sequence = ["#3f145f", "#55307a","#6b468e","#805ea3","#9a7bb7","#b49acb","#cbb3da" ],
            labels={'year_of_release':'Year of Release', 'game_count':'Number of Games'},
            template='plotly_white'
        )


        st.plotly_chart(fig_gyear, use_container_width=True)

        st.divider()

  
        st.subheader("💰 Global Sales vs User Score")

        fig_bi = px.scatter(
            filtered_df,
            x='user_score',
            y='global_sales',
            color='genre',
            size='global_sales',
            hover_data=['name'],labels={'genre':'Genre','user_score':'User Score','global_sales':'Total Global Sales (Millions)'}, 
            color_discrete_sequence = ["#3f145f", "#55307a","#6b468e","#805ea3","#9a7bb7","#b49acb","#cbb3da" ],
            trendline="ols",         
            trendline_scope="overall" # Apply across all data, not per genre
        )

        st.plotly_chart(fig_bi, use_container_width=True)

        st.divider()

        st.subheader("📈 Global Sales Trends of Top 10 Platforms")

        # Aggregate global sales by platform and year
        sales_platform_year = (
            filtered_df.groupby(['year_of_release', 'platform'])['global_sales']
            .sum()
            .reset_index()
        )

        # Compute total sales per platform (to find top 10 overall)
        top_platforms = (
            sales_platform_year.groupby('platform')['global_sales']
            .sum()
            .reset_index()
            .sort_values(by='global_sales', ascending=False)
            .head(10)['platform']
        )

        # Filter only top 10 platforms
        sales_top_platforms = sales_platform_year[
            sales_platform_year['platform'].isin(top_platforms)
        ]

        # Line chart: sales trend over years
        fig_platform_line = px.line(
            sales_top_platforms,
            x='year_of_release',
            y='global_sales',
            color='platform',
            labels={'year_of_release':'Year of Release','platform':'Platform','global_sales':'Total Global Sales (Millions)'},
            color_discrete_sequence = ["#2d004d", "#5a189a", "#c48df5", "#e0c3fc", "#ffa8a8", "#d1f2eb", "#b7f5d3", "#38b000", "#004b23"],
            markers=True,
        )

        st.plotly_chart(fig_platform_line, use_container_width=True)
        st.divider()

        st.subheader("⭐ Genre Performance: User Score vs Global Sales")

        # Aggregate by genre
        score_sales_genre = (
            filtered_df.groupby('genre')
            .agg(avg_score=('user_score','mean'),
                total_sales=('global_sales','sum'))
            .reset_index()
        )

        # Scatter plot
        fig_score_sales = px.scatter(
            score_sales_genre,
            x='avg_score',
            y='total_sales',
            text='genre',   # show genre labels
            size='total_sales',  # bubble size by sales
            color='avg_score',   # color by score
            labels={
                'avg_score':'Average User Score',
                'total_sales':'Total Global Sales (Millions)'
            },
            color_continuous_scale=["#3f145f", "#55307a", "#6b468e", "#805ea3","#9a7bb7", "#b49acb", "#cbb3da"]
        )

        # Improve readability
        fig_score_sales.update_traces(textposition='top center')
        

        st.plotly_chart(fig_score_sales, use_container_width=True)


    # --------------------------------------------------------------------------------------------------
    # Multivariate Analysis
       
        st.divider()
    
    with tab3:
        st.subheader("📈 Global Sales over Years by Genre")
        sales_year_genre = filtered_df.groupby(['year_of_release', 'genre'])['global_sales'].sum().reset_index()
        fig_multi = px.line(sales_year_genre, x='year_of_release', y='global_sales',
                            color='genre', markers=True,
                            labels={'year_of_release':'Year of Release', 'genre':'Genre','global_sales':'Global Sales (Millions)' },)
        st.plotly_chart(fig_multi, use_container_width=True)

        st.divider()

        st.subheader("📊 Global Sales by Genre and Age Rating")

        # Mapping shorthand ratings to full names
        rating_map = {
            "E": "Everyone",
            "E10+": "Everyone 10+",
            "M": "Mature",
            "EC": "Early Childhood",
            "RP": "Rating Pending",
            "K-A": "Kids to Adults",
            "AO": "Adults Only",
            "T": "Teen"
        }

        # Aggregate sales by genre and rating
        sales_platform_rating = (
            filtered_df.groupby(['genre', 'rating'])['global_sales']
            .sum()
            .reset_index()
        )

        # Map abbreviations to full names
        sales_platform_rating['rating'] = sales_platform_rating['rating'].map(rating_map)

        # Define the exact order of ratings to match your color list
        rating_order = [
            "Everyone",
            "Everyone 10+",
            "Mature",
            "Early Childhood",
            "Rating Pending",
            "Kids to Adults",
            "Adults Only",
            "Teen"
        ]

        # Assign categorical type with ordered categories
        sales_platform_rating['rating'] = pd.Categorical(
            sales_platform_rating['rating'],
            categories=rating_order,
            ordered=True
        )

       

        fig_platform_rating = px.bar(
            sales_platform_rating,
            x='genre',
            y='global_sales',
            color='rating',
            barmode='group',
            color_discrete_map={     # Mapping colors to ratings 
                "Everyone": "#3f145f",
                "Everyone 10+": "#55307a",
                "Mature": "#6b468e",
                "Early Childhood": "#805ea3",
                "Rating Pending": "#9a7bb7",
                "Kids to Adults": "#b49acb",
                "Adults Only": "#cbb3da",
                "Teen": "#e2d1e8"
              },
            labels={'rating': 'Age Rating', 'genre': 'Genre', 'global_sales': 'Global Sales (Millions)'}
        )

        st.plotly_chart(fig_platform_rating, use_container_width=True)


# =================================================
        st.divider()

        st.subheader("🔥 Global Sales Heatmap by Genre, Region, and Age Rating")
        
        # Melt the regional sales into long format
        sales_region = filtered_df.melt(
            id_vars=['genre', 'rating'],
            value_vars=['na_sales', 'eu_sales', 'jp_sales', 'other_sales'],
            var_name='region',
            value_name='sales'
        )

          # Rename region values for display
        region_map = {
                'na_sales': ' North America',
                'eu_sales': ' Europe',
                'jp_sales': ' Japan',
                'other_sales': ' Other Regions'
            }
        sales_region['region'] = sales_region['region'].map(region_map)

        # Aggregate global sales by genre, rating, and region
        sales_region_grouped = (
            sales_region.groupby(['genre', 'rating', 'region'])['sales']
            .sum()
            .reset_index()
        )

        # Alternative: facet by region with grouped heatmaps
        fig_facet = px.density_heatmap(
            sales_region_grouped,
            x='genre',
            y='rating',
            z='sales',
            facet_col='region',
            color_continuous_scale=["#3f145f", "#55307a", "#6b468e",
        "#805ea3", "#9a7bb7", "#b49acb", "#cbb3da"],
           labels={'rating':'Age Rating', 'genre':'Genre','region':'Region','sales':'Sales' },
         
        )

        st.plotly_chart(fig_facet, use_container_width=True)


# =================================================
# Insights & Recommendations PAGE
elif page == "Insights & Recommendations":

    st.title("Insights and Recommendations")

    st.markdown("""
### 🔍 Main Findings Insights

- Action games dominate the global market with the highest global sales.
- Nintendo publisher appear frequently among top-selling games.
- Video game sales were highest during 2005–2015.
---
        
### 💡Business Recommendations

- Focus development on Action & Sports games.  
- Improve game quality to increase user scores.
- Target high-performing years trends.
""")


# =================================================
# Summary PAGE
elif page == "Summary":

    st.title("Video Game Sales Summary")

    st.markdown("""


The **Video Game Sales Dashboard** offers an interactive way to explore and analyze global video game sales data.  
Users can filter by genre, Age rating, platform, user score, and release year to cover market trends and insights.

---     
        

## ✨ Dashboard Features
- **Overview Page**: Dataset overview with key performance indicators (KPIs).  
- **Exploratory Data Analysis (EDA)**: Univariate, bivariate, and multivariate visualizations.  
- **Insights & Recommendations**: Turning data into business success.  

---
        
## 🛠️ Technologies Used
- **Streamlit** – Web app interface.  
- **Pandas** – Data manipulation.  
- **Plotly Express** – Interactive visualizations.  

---

## 👨‍💻 Developed By
**Elaf Bahaa Aldein**  
📧 Email: [elafbhaa0@gmail.com](mailto:elafbhaa0@gmail.com)  
🐙 GitHub: [ElafBahaa](https://github.com/elafbhaa)  
🔗 LinkedIn: [Elaf Bahaa Aldein](https://www.linkedin.com/in/elaf-bahaa-aldein-50b7552aa/)


""")
