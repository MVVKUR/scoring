import streamlit as st
import folium
from groq import Groq
from streamlit_folium import folium_static
import random  # For demo purposes
import requests
import json




# Set page configuration
st.set_page_config(
    page_title="Restaurant Location Analysis",
    page_icon="🍽️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #34495e;
        margin-top: 1rem;
    }
    .analysis-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .meta-info {
        font-size: 1.1rem;
        color: #7f8c8d;
        margin-bottom: 1rem;
    }
    .factor-header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #16a085;
        margin-top: 1.5rem;
    }
    .factor-point {
        margin-left: 1rem;
    }
    .output-section {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2980b9;
        margin-top: 1.5rem;
    }
    .score-display {
        font-size: 1.5rem;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        display: inline-block;
        margin: 0.5rem 0;
        background-color: #3498db;
        color: white;
    }
    .strength-point {
        color: #27ae60;
        margin-left: 1rem;
    }
    .challenge-point {
        color: #e74c3c;
        margin-left: 1rem;
    }
    .recommendation-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #3498db;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown('<div class="main-header">Restaurant Location Analysis</div>', unsafe_allow_html=True)
st.markdown("AI-powered analysis of restaurant location potential based on key market factors.")

# Create two columns for input form and map
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown('<div class="sub-header">Restaurant Information</div>', unsafe_allow_html=True)
    
    # Simplified input fields
    restaurant_name = st.text_input("Restaurant Name", placeholder="Pempek Abing")
    location_address = st.text_input("Full Address", placeholder="Jl. Prof Dr Satrio No. 16C, Kuningan, Jakarta")
    query = restaurant_name + location_address
    # Add a note about the AI analysis
    st.info("Our AI will analyze all relevant factors including rental costs, foot traffic, income levels, commercial density, transport access, and competitors.")

with col2:
    # Display a map (in a real app, this would use the address to show the actual location)
    st.markdown('<div class="sub-header">Location Map</div>', unsafe_allow_html=True)
    
    # For demo, centered on Jakarta
    m = folium.Map(location=[-6.2088, 106.8456], zoom_start=12)
    
    if location_address:
        # In a real app, you would geocode the address to get coordinates
        # For demo, we'll use random coordinates around Jakarta
        lat = -6.2088 + random.uniform(-0.02, 0.02)
        lng = 106.8456 + random.uniform(-0.02, 0.02)
        
        # Add marker for the restaurant location
        folium.Marker(
            [lat, lng],
            popup=f"{restaurant_name}<br>{location_address}",
            tooltip="Restaurant Location",
            icon=folium.Icon(color="red", icon="cutlery", prefix="fa")
        ).add_to(m)
        
        # Add a circle to represent the analysis area
        folium.Circle(
            radius=500,
            location=[lat, lng],
            color="blue",
            fill=True,
            fill_opacity=0.2
        ).add_to(m)
    
    folium_static(m)

prompt = """**Restaurant Location Analysis**

*Input:*  
- **Location:** [Enter the restaurant's address]  
- **City/District:** [Enter the specific city and district]  

*Analysis Factors:*  
1. **Rental Cost**  
   - Evaluate the average commercial property rental rates in this district.  
   - Compare rental costs to neighboring districts to assess affordability.  

2. **Foot Traffic**  
   - Analyze the pedestrian and vehicle traffic patterns in the area.  
   - Identify peak business hours and potential customer volume.  

3. **Income Levels & Purchasing Power**  
   - Assess the average income levels of residents in this district.  
   - Determine the spending behavior and restaurant affordability in the area.  

4. **Office & Commercial Density**  
   - Evaluate the presence of office buildings, business centers, and commercial establishments nearby.  
   - Assess the potential for lunch/dinner rush from office workers.  

5. **Public Transport & Accessibility**  
   - Identify the availability of public transportation (MRT, LRT, buses, etc.).  
   - Analyze road access and parking availability for customers.  

6. **Competitor Density & Market Viability**  
   - Determine the number of similar restaurants in a defined radius.  
   - Evaluate competitors’ performance based on reviews, ratings, and popularity.  
   - Identify any market gaps or unique opportunities in this location.  

*Output:*  
- **Location Score:** [Provide a numerical score based on the above factors]  
- **Strengths:** [Summarize key advantages of the location]  
- **Challenges:** [Highlight potential risks or drawbacks]  
- **Recommendation:** [Suggest whether the location is high-potential, moderate, or risky for investment] 
"""

client = Groq(api_key="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")
def fixed_nonrag(prompt,query):
    completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "assistant",
            "content": f' {prompt} also Give the data source or the time you get the data'  
        },
        {
            "role": "user",
            "content": query
        },
    ],
    temperature=0.7,
    max_completion_tokens=4096,
    top_p=0.95,
    stream=False,
    stop=None,
)   
    content_list = [choice.message.content for choice in completion.choices]
    return content_list


if st.button("Analyze Location", type="primary"):
    if not restaurant_name or not location_address:
        st.error("Please provide both restaurant name and location.")
    else:
        with st.spinner("AI is analyzing location data..."):
            import time
            time.sleep(2)
            
            analysis = fixed_nonrag(prompt, query)
            for content in analysis:
                st.markdown(content)
            
        #     st.markdown(f'<div class="analysis-title">{analysis["title"]}</div>', unsafe_allow_html=True)
        #     st.markdown(f'<div class="meta-info">**Data Source:** {analysis["data_source"]}</div>', unsafe_allow_html=True)
        #     st.markdown(f'**Location:** {analysis["location"]}')
        #     st.markdown(f'**City/District:** {analysis["city_district"]}')
            
        #     st.markdown('**Analysis Factors:**')
            
        #     # Rental Cost
        #     st.markdown('<div class="factor-header">1. Rental Cost:</div>', unsafe_allow_html=True)
        #     for point in analysis["analysis_factors"]["rental_cost"]["points"]:
        #         st.markdown(f'<div class="factor-point">* {point}</div>', unsafe_allow_html=True)
            
        #     # Foot Traffic
        #     st.markdown('<div class="factor-header">2. Foot Traffic:</div>', unsafe_allow_html=True)
        #     for point in analysis["analysis_factors"]["foot_traffic"]["points"]:
        #         st.markdown(f'<div class="factor-point">* {point}</div>', unsafe_allow_html=True)
            
        #     # Income Levels
        #     st.markdown('<div class="factor-header">3. Income Levels & Purchasing Power:</div>', unsafe_allow_html=True)
        #     for point in analysis["analysis_factors"]["income_levels"]["points"]:
        #         st.markdown(f'<div class="factor-point">* {point}</div>', unsafe_allow_html=True)
            
        #     # Office Density
        #     st.markdown('<div class="factor-header">4. Office & Commercial Density:</div>', unsafe_allow_html=True)
        #     for point in analysis["analysis_factors"]["office_density"]["points"]:
        #         st.markdown(f'<div class="factor-point">* {point}</div>', unsafe_allow_html=True)
            
        #     # Public Transport
        #     st.markdown('<div class="factor-header">5. Public Transport & Accessibility:</div>', unsafe_allow_html=True)
        #     for point in analysis["analysis_factors"]["public_transport"]["points"]:
        #         st.markdown(f'<div class="factor-point">* {point}</div>', unsafe_allow_html=True)
            
        #     # Competitor Density
        #     st.markdown('<div class="factor-header">6. Competitor Density & Market Viability:</div>', unsafe_allow_html=True)
        #     for point in analysis["analysis_factors"]["competitor_density"]["points"]:
        #         st.markdown(f'<div class="factor-point">* {point}</div>', unsafe_allow_html=True)
            
        #     # Output
        #     st.markdown('<div class="output-section">Output:</div>', unsafe_allow_html=True)
            
        #     # Location Score
        #     st.markdown(f'<div class="score-display">Location Score: {analysis["location_score"]}</div>', unsafe_allow_html=True)
            
        #     # Strengths
        #     st.markdown('**Strengths:**')
        #     for strength in analysis["strengths"]:
        #         st.markdown(f'<div class="strength-point">+ {strength}</div>', unsafe_allow_html=True)
            
        #     # Challenges
        #     st.markdown('**Challenges:**')
        #     for challenge in analysis["challenges"]:
        #         st.markdown(f'<div class="challenge-point">- {challenge}</div>', unsafe_allow_html=True)
            
        #     # Recommendation
        #     st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        #     st.markdown('**Recommendation:**')
        #     st.markdown(analysis["recommendation"])
        #     st.markdown('</div>', unsafe_allow_html=True)
            
            # Option to download the analysis as PDF (in a real app)
            st.download_button(
                label="Download Analysis as PDF",
                data="Sample PDF content",  # In a real app, this would generate a PDF
                file_name=f"{restaurant_name}_location_analysis.pdf",
                mime="application/pdf",
            )

# Information section at the bottom
with st.expander("About the Analysis Framework"):
    st.markdown("""
    Our AI-powered restaurant location analysis evaluates the following key factors:
    
    1. **Rental Cost**
       - Commercial property rental rates in the district
       - Comparative analysis with neighboring areas
       
    2. **Foot Traffic**
       - Pedestrian and vehicle traffic patterns
       - Peak business hours identification
       
    3. **Income Levels & Purchasing Power**
       - Average income demographics
       - Local spending behavior analysis
       
    4. **Office & Commercial Density**
       - Proximity to office buildings and business centers
       - Potential for lunch/dinner rush from office workers
       
    5. **Public Transport & Accessibility**
       - Public transportation availability
       - Road access and parking assessment
       
    6. **Competitor Density & Market Viability**
       - Similar restaurants in the defined radius
       - Competitor performance analysis
       - Market gap identification
    
    The AI combines these factors to generate an overall location score, key strengths and challenges, and tailored recommendations for your specific restaurant concept.
    """)