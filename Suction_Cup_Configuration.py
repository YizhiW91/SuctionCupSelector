import streamlit as st
from SuctionCupRules import *
import pandas as pd

# Text
st.markdown(
    """
    # Suction Cup Initializer
    This is the tool for item suction cup configuration. Please input the dimensions of a item, the page will provide the compatible suction cups and grasp type based on the preset rules.
    """
)

# input blanks
length = st.number_input("Item Length", value=0.0, step=0.01)
width = st.number_input("Item Width", value=0.0, step=0.01)
height = st.number_input("Item Height", value=0.0, step=0.01)
weight = st.number_input("Item Weight", value=0.0, step=0.01)

# create the rule list
# Removed the rules for medium suction cup as we don't use it currently.
rules = [MiniCupRule, MiniCupPreferred1SORule, MiniCupPreferred2, 
         SmallCupRule, SmallCupPreferredCase3SO, SmallCupPreferredCase2, SmallCupPreferredCase1,
         BagCupRule, BagCupPreferred2, BagCupPreferred1,
         LargeCupRule, BigCupPreferredCase1, BigCupPreferredCase2SO, BigCupPreferredCase3]



def confirm():
    dim_array = sorted([length, width, height])
    dim1, dim2, dim3 = dim_array[0], dim_array[1], dim_array[2]
    item = Item(1, 1, dim1, dim2, dim3, weight, "no description")    
    for rule in rules:
        if rule().isEligible(item):
            item.addSuctionCupConfig(rule().getConfig())
    
    
    
    if len(item.getSuctionCupConfig()) == 0:
        st.warning("No compatible suction cup found, please inspect the item manually")
    else:
        data = [(x[0].name, x[1].name) for x in item.getSuctionCupConfig()]
        st.session_state['output'] = pd.DataFrame(data, columns=['SuctionCup', 'GraspType'])
    
# Button
st.button("Run Configuration", help="Click to get the output of recommended item configuration", on_click=confirm)

# Output
if 'output' in st.session_state:
    st.markdown(
    """
    ## Output
    """
    )
    st.dataframe(st.session_state['output'])
