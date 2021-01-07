## this is to assure your CSV is not an empty one, that would screw up the ingestion process
## It can remove the file that was a weird shape

import os
import sys
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
dist = []

## replace the path before run
path = "/Users/matthewchuang/Documents/GitHub/algo_test/datas/20210106/minute"

for file in Path(path).iterdir():
    if file.is_file():
        df = pd.read_csv(file)
        if df.shape[0] < 2000:
            os.remove(file)
        else:
            dist.append(df.shape[0])

plt.hist(dist)