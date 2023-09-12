import streamlit as st
from math import *
import pandas as pd
from scipy.stats import norm

# Text
st.markdown(
    """
    # AB Test Result Analyzer
    This is the tool for performing the AB test given the following parameters:
    
    * Number of data points in control group
    * Success picking rate in control group
    * Number of data points in experiment group
    * Success picking rate in experiment group
    * Alpha - The significance level
    
    ## Assumption
    
    1. Null Hypothesis (H0): There is no significant difference of picking success rate between control group and experiment group.
    2. Alternative Hypothesis (H1): The control group has higher success rate than the experiment group. The difference is at least MDE.
    
    ## Result
    The analyzer will output the p value. Comparing the p value to the alpha provided above, there are two possible results, significant or insignificant.
    * Significant: If the p value is less than alpha, then we can reject the null hypothesis in favor of the alternative hypothesis.
    * Insignificant: We reject the alternative hypothesis in favor of the null hypothesis.
    
    """
)

# input blanks
n_ctl = st.number_input("Number of samples in control group", value=0, step=1)
p_ctl = st.number_input("Picking success rate of control group", value=0.5, step=0.01)
n_exp = st.number_input("Number of samples in experiment group", value=0, step=1)
p_exp = st.number_input("Picking success rate of experiment group", value=0.5, step=0.01)
alpha = st.number_input("Alpha", value=0.05, step=0.01, help="Significance level")

# methods
def get_two_sample_Z_test(n_ctl, p_ctl, n_exp, p_exp, alpha):
    """Two sided AB test implementing pooled and unpooled standard error based on std ratio"""

    x_ctl = p_ctl * n_ctl
    x_exp = p_exp * n_exp
    
    d = p_ctl - p_exp
    
    print(f'control mean: {p_ctl}')
    print(f'experiment mean: {p_exp}')
    
    std_ctl = sqrt(p_ctl * (1-p_ctl))
    std_exp = sqrt(p_exp * (1-p_exp))
    
    p_pool = (x_ctl+x_exp)/(n_ctl+n_exp)
    se_pool =  sqrt(p_pool*(1-p_pool)*(1/n_ctl + 1/n_exp))
    
    # calculate confidence interval
    Z_alpha = norm.ppf(1-alpha)
    lower = d - se_pool*Z_alpha
    upper = d + se_pool*Z_alpha
    
    print(f"The confidence interval for the difference is [{lower:.4f}, {d:.4f}, {upper:.4f}]")
    
    # calculate p value
    Z = d/se_pool
    if Z <= 0:
        Z = -Z
    p = 1 - norm.cdf(Z)
    p *=2
    
    print(f"statistics: {Z}")
    print(f"The p value: {p}")
    
    return Z, p, lower, upper, d

# callback
def confirm():
    try:
        _, p, _, _, _ = get_two_sample_Z_test(n_ctl, p_ctl, n_exp, p_exp, alpha)
        st.session_state['p'] = p
    except Exception as e:
        st.warning("Couldn't perform the analysis. Please make sure that the input parameters are correct.")
    
# Button
st.button("Run Calculation", help="Click to get the p value", on_click=confirm)

# Output
if 'p' in st.session_state:
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown(
        """
        ## Output
        """
        )
        st.metric(label="P Value", value='{:.2}'.format(st.session_state['p']))
