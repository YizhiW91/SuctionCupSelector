from scipy.stats import norm
from math import *

def get_two_sample_size_twosided(alpha, power, dmin, bm):
    """Sample size calculation"""
    Zalpha = norm.ppf(1-alpha/2)
    Zbeta = norm.ppf(1 - power)
    bexp = dmin + bm
    
    sd1 = sqrt(2*bm*(1-bm))
    sd2 = sqrt(bm*(1-bm) + bexp*(1-bexp))
    
    return ceil((Zalpha*sd1 - Zbeta * sd2)/dmin)**2
    


def get_two_sample_Z_test_twosided(n_ctl, x_ctl, n_exp, x_exp, alpha):
    """Two sided AB test implementing pooled and unpooled standard error based on std ratio"""
    
    
    p_ctl = x_ctl/n_ctl
    p_exp = x_exp/n_exp
    d = p_ctl - p_exp
    
    print(f'control mean: {p_ctl}')
    print(f'experiment mean: {p_exp}')
    
    std_ctl = sqrt(p_ctl * (1-p_ctl))
    std_exp = sqrt(p_exp * (1-p_exp))
    
    p_pool = (x_ctl+x_exp)/(n_ctl+n_exp)
    se_pool =  sqrt(p_pool*(1/n_ctl + 1/n_exp))
    
    # calculate confidence interval
    Z_alpha_div_2 = norm.ppf(1-alpha/2)
    lower = d - se_pool*Z_alpha_div_2
    upper = d + se_pool*Z_alpha_div_2
    
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