import pandas as pd
import plotly as plt
import os
import glob
import plotly.express as px
import numpy as np

import plotly.graph_objects as go
import PostBacStudies.get_data as gd

class PostBac():
    def __init__(self, application = None):
        self.df = gd.load_data()
        print("hello world")
