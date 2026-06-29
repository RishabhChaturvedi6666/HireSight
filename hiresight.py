"""
HireSight - AI Job Market Intelligence Dashboard
Built by Rishabh Chaturvedi
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="HireSight", page_icon="📊", layout="wide")

@st.cache_data
def generate_data():
    np.random.seed(42)
    
    titles = ['Data Analyst', 'Data Scientist', 'ML Engineer', 'AI Engineer', 
              'Business Analyst', 'Data Engineer', 'Deep Learning Engineer', 
              'NLP Engineer', 'Computer Vision Engineer', 'Analytics Manager',
              'BI Developer', 'Data Architect', 'MLOps Engineer', 'Research Scientist']
    
    companies = ['TCS', 'Infosys', 'Wipro', 'Accenture', 'Deloitte',
                 'Amazon', 'Flipkart', 'Google', 'Microsoft', 'IBM',
                 'HCL', 'Tech Mahindra', 'Capgemini', 'Cognizant', 'Genpact',
                 'Fractal Analytics', 'Mu Sigma', 'Tiger Analytics']
    
    locations = ['Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai',
                 'Delhi', 'Gurgaon', 'Noida', 'Kolkata', 'Ahmedabad', 'Remote']
    
    skills_pool = ['Python', 'SQL', 'R', 'Excel', 'Power BI', 'Tableau',
                   'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
                   'NLP', 'Computer Vision', 'Statistics', 'Pandas', 'NumPy',
                   'Scikit-learn', 'Keras', 'AWS', 'Azure', 'GCP',
                   'Docker', 'Kubernetes', 'Git', 'Spark', 'Hadoop',
                   'MongoDB', 'PostgreSQL', 'MySQL', 'ETL', 'Airflow',
                   'Streamlit', 'Plotly', 'Seaborn', 'Matplotlib', 'Jupyter']
    
    experience_levels = ['0-2 years', '2-4 years', '4-6 years', '6-8 years', '8+ years']
    
    jobs = []
    for i in range(200):
        title = np.random.choice(titles)
        company = np.random.choice(companies)
        location = np.random.choice(locations)
        experience = np.random.choice(experience_levels)
        
        base_salary = {'0-2 years': 400000, '2-4 years': 700000, 
                      '4-6 years': 1200000, '6-8 years': 1800000, '8+ years': 2500000}[experience]
        
        num_skills = np.random.randint(3, 8)
        skills = list(np.random.choice(skills_pool, num_skills, replace=False))
        
        premium_skills = ['Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'NLP', 'Computer Vision', 'MLOps']
        premium_count = sum(1 for s in skills if s in premium_skills)
        salary_min = int(base_salary * (1 + premium_count * 0.15))
        salary_max = int(salary_min * 1.4)
        
        work_type = 'Onsite'
        if location == 'Remote':
            work_type = 'Remote'
        elif np.random.random() < 0.3:
            work_type = 'Hybrid'
        
        exp_map = {'0-2 years': 'Entry Level (0-2Y)', '2-4 years': 'Mid Level (2-4Y)',
                   '4-6 years': 'Senior (4-6Y)', '6-8 years': 'Lead (6-8Y)', '8+ years': 'Executive (8Y+)'}
        
        # FIXED: Extract only the number from experience
        exp_text = experience.replace(' years', '').replace('+', '')
        exp_years = int(exp_text.split('-')[0])
        
        jobs.append({
            'title': title,
            'title_standardized': title,
            'company': company,
            'experience': experience,
            'experience_standardized': exp_map[experience],
            'experience_years': exp_years,
            'salary': f"Rs{salary_min//100000}L - Rs{salary_max//100000}L PA",
            'salary_min': salary_min,
            'salary_max': salary_max,
            'salary_avg': (salary_min + salary_max) / 2,
            'location': location,
            'location_standardized': location,
            'work_type': work_type,
            'all_skills': skills,
            'skill_count': len(skills),
        })
    
    return pd.DataFrame(jobs)

st.markdown('<h1 style="text-align:center; color:#1f77b4;">📊 HireSight</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666; font-size:1.2rem;">AI & Data Science Job Market Intelligence Dashboard</p>', unsafe_allow_html=True)

df = generate_data()

st.sidebar.title("🔍 Filters")
exp_options = ['All'] + sorted(df['experience_standardized'].unique().tolist())
selected_exp = st.sidebar.selectbox("Experience Level", exp_options)

loc_options = ['All'] + sorted(df['location_standardized'].unique().tolist())
selected_loc = st.sidebar.selectbox("Location", loc_options)

work_options = ['All'] + sorted(df['work_type'].unique().tolist())
selected_work = st.sidebar.selectbox("Work Type", work_options)

filtered_df = df.copy()
if selected_exp != 'All':
    filtered_df = filtered_df[filtered_df['experience_standardized'] == selected_exp]
if selected_loc != 'All':
    filtered_df = filtered_df[filtered_df['location_standardized'] == selected_loc]
if selected_work != 'All':
    filtered_df = filtered_df[filtered_df['work_type'] == selected_work]

st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("📋 Total Jobs", len(filtered_df))
with c2:
    avg_sal = filtered_df['salary_avg'].mean()
    st.metric("💰 Avg Salary", f"Rs{avg_sal/100000:.1f}L" if pd.notna(avg_sal) else "N/A")
with c3:
    top_skill = filtered_df['all_skills'].explode().value_counts().index[0] if len(filtered_df) > 0 else "N/A"
    st.metric("🔥 Top Skill", top_skill)
with c4:
    top_loc = filtered_df['location_standardized'].value_counts().index[0] if len(filtered_df) > 0 else "N/A"
    st.metric("📍 Top Location", top_loc)

tab1, tab2, tab3, tab4 = st.tabs(["🔥 Skill Demand", "💰 Salary Insights", "📍 Location Analysis", "📈 Experience Trends"])

with tab1:
    st.header("Most In-Demand Skills")
    all_skills = []
    for skills in filtered_df['all_skills']:
        all_skills.extend(skills)
    skill_counts = pd.Series(all_skills).value_counts().head(20)
    skill_df = pd.DataFrame({'Skill': skill_counts.index, 'Job Count': skill_counts.values})
    fig = px.bar(skill_df, x='Job Count', y='Skill', orientation='h', color='Job Count', color_continuous_scale='Viridis')
    fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Salary Distribution")
    sal_data = filtered_df[filtered_df['salary_avg'].notna()]
    if len(sal_data) > 0:
        fig = px.histogram(sal_data, x='salary_avg', nbins=30, color='experience_standardized')
        st.plotly_chart(fig, use_container_width=True)
    
    exp_sal = filtered_df.groupby('experience_standardized')['salary_avg'].mean().reset_index()
    exp_sal = exp_sal[exp_sal['experience_standardized'] != 'Not Specified']
    fig2 = px.bar(exp_sal, x='experience_standardized', y='salary_avg', color='salary_avg', color_continuous_scale='Magma')
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Jobs by Location")
    loc_counts = filtered_df['location_standardized'].value_counts().head(10).reset_index()
    loc_counts.columns = ['Location', 'Job Count']
    fig = px.bar(loc_counts, x='Job Count', y='Location', orientation='h', color='Job Count', color_continuous_scale='Turbo')
    fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    work_type = filtered_df['work_type'].value_counts().reset_index()
    work_type.columns = ['Work Type', 'Count']
    fig2 = px.pie(work_type, values='Count', names='Work Type', color_discrete_sequence=['#ff9999','#66b3ff','#99ff99'])
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.header("Experience vs Salary")
    scatter_data = filtered_df[(filtered_df['experience_years'].notna()) & (filtered_df['salary_avg'].notna())]
    if len(scatter_data) > 0:
        fig = px.scatter(scatter_data, x='experience_years', y='salary_avg', color='title_standardized', size='skill_count')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown('<div style="text-align:center; color:#666;"><b>HireSight</b> | Built by Rishabh Chaturvedi | B.Tech AI & Data Science @ GGSIPU</div>', unsafe_allow_html=True)