
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
    "<h2 style='font-size:28px'>Navigation</h2>", unsafe_allow_html=True
)

page = st.sidebar.radio(
    " ",# to keep the radio label empty
    [
        "Overview",
        "Analysis",
        "Recommendations"

    ]
)


# Add a separator line
st.sidebar.markdown("---")
# --------------------------------------------------------------------------------------------------
# Sidebar Filters

st.sidebar.markdown(
 "<h3 style='font-size:24px'>Data Filters</h3>", unsafe_allow_html=True )

#genre_filter = st.sidebar.multiselect(
   # "Select Genre", options=df["genre"].unique(), default=df["genre"].unique())


with st.sidebar.expander("Select Genre", expanded=False):
    genre_filter = st.multiselect(
        label="",
        options=df["genre"].unique(),
        default=df["genre"].unique()
    )

age_rating_map = { #  # Mapping shorthand ratings to full names 
    "E": "Everyone",
    "E10+": "Everyone 10+",
    "T": "Teen",
    "M": "Mature 17+",
    "AO": "Adults Only 18+",
    "K-A": "Kids to Adults"
}

#rating_filter = st.sidebar.multiselect(
 #   "Select Age Rating",   options=list(age_rating_map.keys()),default=list(age_rating_map.keys()), 
 #   format_func=lambda x: f"{x} — {age_rating_map[x]}")

with st.sidebar.expander("Select Age Rating", expanded=False):
    rating_filter = st.multiselect(
        label="",
        options=list(age_rating_map.keys()),
        default=list(age_rating_map.keys()),
        format_func=lambda x: f"{x} — {age_rating_map[x]}"
    )



#platform_filter = st.sidebar.multiselect(
   # "Select Platform", options=df["platform"].unique(), default=df["platform"].unique())

with st.sidebar.expander("Select Platform", expanded=False):
    platform_filter = st.multiselect(
        label="",
        options=df["platform"].unique(),
        default=df["platform"].unique()
    )


#user_score_filter = st.sidebar.slider(
 #   "Set User Score Range",
  #  float(df["user_score"].min()),
   # float(df["user_score"].max()),
    #(float(df["user_score"].min()), float(df["user_score"].max())),
#)
with st.sidebar.expander("Set User Score Range", expanded=False):
    user_score_filter = st.slider(
        label="",
        min_value=float(df["user_score"].min()),
        max_value=float(df["user_score"].max()),
        value=(
            float(df["user_score"].min()),
            float(df["user_score"].max())
        ),
        step=0.1
    )


    
#year_filter = st.sidebar.slider(
 #   "Set Year of Release Range",
  #  int(df["year_of_release"].min()),
   # int(df["year_of_release"].max()),
    #(int(df["year_of_release"].min()), int(df["year_of_release"].max())),
#)


with st.sidebar.expander("Set Year of Release Range", expanded=False):
    year_filter = st.slider(
        label="",
        min_value=int(df["year_of_release"].min()),
        max_value=int(df["year_of_release"].max()),
        value=(
            int(df["year_of_release"].min()),
            int(df["year_of_release"].max())
        )
    )


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

    st.markdown("""
    The Video Game Sales **Dashboard** is an interactive tool for analyzing global video game sales and identifying market trends. Users can filter by Genre, Age Rating, Platform, User Score, and Release Year to explore performance across the gaming industry.
    """)

 


    tab1, tab2= st.tabs([
        "Dataset Overview & KPIs",
        "Data Dictionary"
    ])
    with tab1:
        st.subheader("Dataset Overview")

        st.markdown("""
        The **Dataset** provides comprehensive data on video game sales, and user insights globally, including details such as the game's name, platform, year of release, genre, publisher, sales in different regions, developer, and age rating.
    """)

    # Initialize number of rows ...................
        if "rows" not in st.session_state:
            st.session_state.rows = 5

    # Display dataframe
        st.dataframe(filtered_df.head(st.session_state.rows))

    # Show more button .......................
        if st.button("Show More Rows"):
            st.session_state.rows += 10


    
        st.divider()
        st.subheader("Key Performance Indicators (KPIs)")

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
        
    

    with tab2:   # Data Summary"
        
    
        st.subheader("Column Descriptions")
       

        column_data = {
            "Column": [
                "Index", "Name", "Platform", "Year_of_Release", "Genre", "Publisher",
                "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales",
              "User_Score", 
                "Developer", "Rating", "Sales_Category","Game_Age","Game_Age_Category"
            ],
            "Description": [
                "Unique identifier for each video game record.",
                "The name of the video game.",
                "The platform on which the game is available (PC, PS4, Xbox, etc.).",
                "The year in which the game was released.",
                "The genre of the game (Action, Sports, etc.).",
                "The company that published the game.",
                "Sales in North America (millions).",
                "Sales in Europe (millions).",
                "Sales in Japan (millions).",
                "Sales in other regions (millions).",
                "Total global sales (millions).",
                
                "Average score given by users.",
                
                "The company that developed the game.",
                "ESRB rating (E, T, M, etc.).",
                "Sales performance category (best_seller, medium, low)",
                "Number of years since the game’s release (current year − release year)",
                "Binned game age derived from release year (New, Recent, Old)"
            ]
        }

        df_desc = pd.DataFrame(column_data)
        st.dataframe(df_desc, use_container_width=True)

        
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
            st.subheader("Total Global Sales by Genre")

            sales_genre = (
                filtered_df.groupby('genre')['global_sales']
                .sum()
                .reset_index()
                .sort_values(by='global_sales', ascending=False).head(10)
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
            st.caption(""" 👉 Action and Sports genres dominate global sales, indicating strong market preference.""")
        
        with col2:
            st.subheader("Games Released by Year")

            games_per_year = (
                filtered_df.groupby('year_of_release')['name']
                .count()
                .reset_index()
                .sort_values(by='name', ascending=False).head(10)
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
            st.caption(" 👉 Game releases vary over time, with noticeable growth periods that reflect the expansion of the gaming industry.""")
        

        
        st.divider()

        st.subheader("Top 10 Publishers by Global Sales")

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
        st.caption("👉 Top 10 Publishers dominate the global sales, highlighting a highly concentrated and competitive market.")
        
        st.divider()

        
        st.subheader("Distribution of User Scores")

        fig_hist = px.histogram(
            filtered_df,
            x="user_score",
            nbins=20,
            marginal="box",  # adds boxplot on top 
            opacity=0.85,
            color_discrete_sequence = ["#2d004d", "#5a189a", "#c48df5", "#e0c3fc", "#ffa8a8", "#d1f2eb", "#b7f5d3", "#38b000", "#004b23"], 
        )

        fig_hist.update_layout(
            xaxis_title="User Score",
            yaxis_title="Number of Games",
            bargap=0.1
        )

        st.plotly_chart(fig_hist, use_container_width=True)
        st.caption(" 👉 Most games receive moderate to high user scores, reflecting generally positive user feedback." )
    # --------------------------------------------------------------------------------------------------
    # Bivariate Analysis
    with tab2:


        st.subheader("Number of Games Released per Year with Trendline")

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
        st.caption("👉 Game production has grown over the years, despite some fluctuations." )
 


        st.divider()

        st.subheader("Global Sales Distribution by User Score (Top 10 Genres)")

    # Get Top 10 genres by total global sales
        top_genres = (
        filtered_df.groupby("genre")["global_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )

        filtered_top10 = filtered_df[filtered_df["genre"].isin(top_genres)]

        fig_violin = px.violin(
        filtered_top10,
        x="genre",              # categorical axis (e.g., genre)
        y="global_sales",       # numeric axis
        color="genre",          # color by genre
        box=True,               # add embedded boxplot
        points="all",           # show all individual points
        hover_data=["name", "user_score"],  # extra info on hover
        labels={
            "genre": "Genre",
            "global_sales": "Global Sales (Millions)"
        },
        color_discrete_sequence=[
            "#2d004d", "#5a189a", "#c77dff",
            "#ff4d4d", "#ff8787",
            "#80ed99", "#38b000",
            "#b7f5d3", "#004b23", "#6a0dad"
        ]
    )

        st.plotly_chart(fig_violin, use_container_width=True)

        st.caption("👉 Sales performance varies across genres, with some genres achieving higher global sales." )


        st.divider()

        st.subheader("Global Sales Trends of Top 3 Platforms")

        # Aggregate global sales by platform and year
        sales_platform_year = (
            filtered_df.groupby(['year_of_release', 'platform'])['global_sales']
            .sum()
            .reset_index()
        )

        # Compute total sales per platform (to find top 3 overall)
        top_platforms = (
            sales_platform_year.groupby('platform')['global_sales']
            .sum()
            .reset_index()
            .sort_values(by='global_sales', ascending=False)
            .head(3)['platform']
        )

        # Filter only top 3 platforms
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
            color_discrete_sequence = ["#2d004d", "#38b000",  "#ff4d4d" ],markers=True,
        )

        st.plotly_chart(fig_platform_line, use_container_width=True)

        st.caption("👉 The top 3 platforms show clear sales peaks across different years, reflecting shifts in console popularity and changes in user demand over time.")
          
    # Multivariate Analysis
       
     
    
    with tab3:
        st.subheader("Global Sales over Years by Top Genres")


        # Get top 3 games by global sales
        top10_games = (
        filtered_df.groupby('genre')['global_sales'].sum().sort_values(ascending=False).head(3).index)

        # Filter dataset
        filtered_df2 = filtered_df[filtered_df['genre'].isin(top10_games)]


        sales_year_genre = filtered_df2.groupby(['year_of_release', 'genre'])['global_sales'].sum().reset_index()
        fig_multi = px.line(sales_year_genre, x='year_of_release', y='global_sales',
                            color='genre', markers=True,  color_discrete_sequence=[

        "#4c1d95",  # purple
        "#b91c1c",  # red
        "#065f46",  # green
        "#6d28d9",  # violet
        "#6ee7b7",  # light green
        "#8b5cf6",  # light purple
        "#10b981",  # green
        "#ef4444"   # red
    ],
                            labels={'year_of_release':'Year of Release', 'genre':'Genre','global_sales':'Global Sales (Millions)' },)
        st.plotly_chart(fig_multi, use_container_width=True)
        st.caption("👉 Global sales by genre show steady year‑over‑year growth followed by a sharp decline.")
      

        st.divider()

        st.subheader("Global Sales by Genre and Age Rating")

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

        # Define rating order
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

        # Assign categorical order
        sales_platform_rating['rating'] = pd.Categorical(
            sales_platform_rating['rating'],
            categories=rating_order,
            ordered=True
        )

        # Get Top 5 genres
        top_genres = (
            sales_platform_rating.groupby('genre')['global_sales']
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .index
        )

        # Filter Top 3
        sales_platform_rating = sales_platform_rating[
            sales_platform_rating['genre'].isin(top_genres)
        ]

        # Plot
        fig_platform_rating = px.bar(
            sales_platform_rating,
            x='genre',
            y='global_sales',
            color='rating',
            barmode='group',
            color_discrete_sequence=[

        "#4c1d95",  # purple
        "#b91c1c",  # red
        "#065f46",  # green
        "#6d28d9",  # violet
        "#6ee7b7",  # light green
        "#8b5cf6",  # light purple
        "#10b981",  # green
        "#ef4444"   # red
    ],
            labels={
                'rating': 'Age Rating',
                'genre': 'Genre',
                'global_sales': 'Global Sales (Millions)'
            }
        )

        st.plotly_chart(fig_platform_rating, use_container_width=True)

        st.caption(
            "👉 Top 5 genres dominate global sales, with 'Everyone' and 'Teen' ratings contributing the most across genres."
        )


        st.divider()
    

        st.subheader("Global Sales Heatmap by Genre, Region, and Age Rating")
        
   

        # Melt the regional sales into long format
        sales_region = filtered_df.melt(
            id_vars=['genre', 'rating'],
            value_vars=['na_sales', 'eu_sales', 'jp_sales', 'other_sales'],
            var_name='region',
            value_name='sales'
        )

        # Rename region values for display
        region_map = {
            'na_sales': 'North America',
            'eu_sales': 'Europe',
            'jp_sales': 'Japan',
            'other_sales': 'Other Regions'
        }

        sales_region['region'] = sales_region['region'].map(region_map)

        # Aggregate sales by genre, rating, and region
        sales_region_grouped = (
            sales_region.groupby(['genre', 'rating', 'region'])['sales']
            .sum()
            .reset_index()
        )

        # Get Top 5 genres by total sales
        top_genres = (
            sales_region_grouped.groupby('genre')['sales']
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .index
        )

        # Filter only Top 5 genres
        sales_region_grouped = sales_region_grouped[
            sales_region_grouped['genre'].isin(top_genres)
        ]

        # Heatmap
        fig_facet = px.density_heatmap(
            sales_region_grouped,
            x='genre',
            y='rating',
            z='sales',
            facet_col='region',
            color_continuous_scale=[
                "#2e1065",
                "#4c1d95",
                "#6d28d9",
                "#9333ea",
                "#c026d3",
                "#db2777",
                "#e11d48"
                    ],
            labels={
                'rating': 'Age Rating',
                'genre': 'Genre',
                'region': 'Region',
                'sales': 'Sales'
            }
        )

        st.plotly_chart(fig_facet, use_container_width=True)

        st.caption(
            "👉 Top genres show different regional preferences, with Action and Sports dominating globally and Role-Playing stronger in Japan."
        )

# =================================================
# Insights & Recommendations PAGE
elif page == "Recommendations":

    st.title("Business Recommendations")
    st.markdown("""
 
### Strategic actions to enhance market performance and maximize global video game sales.

- Focus development on Action & Sports games (since they are the most popular).  
- Focus on family-friendly ratings to reach more players.. 
- Improve game quality to raise user scores
- Target high-performing years trends (release your games during the busiest times of the year when people are buying the most).
- Emulate PS2‑era success with variety + budget‑friendly pricing.

""")



# Footer

st.markdown("""     ---
<div style='text-align: center; font-size: 18px; color: #999;'>

© 2026 Elaf Bahaa Aldein • All Rights Reserved • 
<a href="mailto:elafbhaa0@gmail.com" style="color:#999; text-decoration:none;">Email</a> • 
<a href="https://github.com/elafbhaa" target="_blank" style="color:#6e6e6e; text-decoration:none;">GitHub</a> • 
<a href="https://www.linkedin.com/in/elaf-bahaa-aldein-50b7552aa/" target="_blank" style="color:#0A66C2; text-decoration:none;">LinkedIn</a> •
<a href="https://wa.me/201557549995?text=Hi%20Elaf,%20I%20visited%20your%20Video%20Game%20Dashboard" 
target="_blank" style="color:#25D366; text-decoration:none;">WhatsApp
</a>
</div>
""", unsafe_allow_html=True)
