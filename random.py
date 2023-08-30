import pandas as pd
import numpy as np


line_colors = {
    'U7': '#33B5FF',   # Light Blue
    'S and U Bahn': '#FFC300',  # Yellow
    'U6': '#DA33FF',   # Light Purple
    'S7': '#FF335D',   # Light Red
    'S25': '#00FF00',  # Green
    'U9': '#FF5733',   # Orange
    'S2': '#00CC00',   # Green2
    'U3': '#33FF33',   # Green3
    'S8': '#6B4423',   # Poop green
    'U8': '#00008B',   # Dark Blue
    'S3': '#0000FF',   # Blue
    'S5': '#FFD700',   # Dark Yellow
    'U5': '#A52A2A',   # Dark Brown
    'S1': '#FF33AD',   # Light Pink
    'U2': '#FF6961',   # Light Red
    'S75': '#FF00FF',  # Magenta
    'U1': '#FFFF00',   # Yellow 2
    'S46': '#FFA500',  # Orange2
    'S47': '#CD853F',  # Light Brown
    'U4': '#FFD700',    # yellow 3
    "": '#008080'# Bright Green (same as U2)
}


def random():
    new_map.to_csv('/Users/alexhergert/code/Xander78261/ticket-control-bvg/data-newmap.csv')
    new_map.fillna("", inplace=True)
    new_map.loc[new_map["Location"].str.contains(""), "Location"] = new_map["lines"]
    new_map.loc[new_map["lines"].str.contains(","), "Location"] = "S and U Bahn"
    new_map["color"] = new_map["Location"].map(line_colors)
    return new_map
