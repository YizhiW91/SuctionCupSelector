import streamlit as st
import pandas as pd
from math import *
import statsmodels.stats.proportion

# Text
st.markdown(
    """
    # Item Configuration AB Test Sample Size Calculator
    This is the tool for calculating how many data points is needed for each variation in the AB test. Please input the baseline, power, alpha and the relative minimal detectable effect(MDE), the page will return the sample size needed.
    
    The alternative hypothsis of the Item Configuration AB Test assumes that control group has higher success rate than the experiment group, hence the test is one-side test.
    """
)

# input blanks
baseline = st.number_input("Baseline", value=0.5, step=0.01, help="The control group proportion which should be greater than the experiment group proportion")
alpha = st.number_input("Alpha", value=0.05, step=0.01, help="Significance level")
power = st.number_input("Power", value=0.80, step=0.01, help="Power of the test")
MDE = st.number_input("Relative MDE Ratio", value=0.15, step=0.01, help="Relative minimal detectable effect. Alternative hypothesis assumes that experiment group proportion is less than baseline - MDE_Ratio*baseline")

# methods
def get_sample_size(alpha, power, dmin, bm):
    """Sample size calculation for single side test"""
    return ceil(statsmodels.stats.proportion.samplesize_proportions_2indep_onetail(diff=dmin, prop2=bm-dmin, power=power, ratio=1, alpha=alpha, value=0, alternative='smaller'))

# callback
def confirm():
    try:
        n = get_sample_size(alpha, power, baseline*MDE, baseline)
        st.session_state['sample_size'] = n
    except Exception as e:
        st.warning("Couldn't perform the calculation. Please make sure that the input parameters are correct.")
        st.session_state['sample_size'] = "NA"
        
# Button
st.button("Run Calculation", help="Click to get the needed sample size per variant", on_click=confirm)

# Output
if 'sample_size' in st.session_state:
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown(
        """
        ## Output
        """
        )
        st.metric(label="Sample Size", value=st.session_state['sample_size'], help=f"Need {st.session_state['sample_size']} sample per variant")
