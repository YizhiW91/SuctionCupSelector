from scipy.stats import norm
from math import *
import statsmodels.stats.proportion

def get_sample_size(alpha, power, dmin, bm):
    """Sample size calculation for single side test"""
    return ceil(statsmodels.stats.proportion.samplesize_proportions_2indep_onetail(diff=dmin, prop2=bm-dmin, power=power, ratio=1, alpha=alpha, value=0, alternative='smaller'))



def get_two_sample_Z_test(n_ctl, x_ctl, n_exp, x_exp, alpha):
    """Two sided AB test implementing pooled and unpooled standard error based on std ratio"""
    
    
    p_ctl = x_ctl/n_ctl
    p_exp = x_exp/n_exp
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