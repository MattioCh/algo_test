import pandas as pd
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities
from pathlib import Path

# Set the start and end dates of the bars, should also align with the Trading Calendar
start_session = pd.Timestamp('2000-10-5', tz='utc')
end_session = pd.Timestamp('2021-1-4', tz='utc')


register(
    'daily-bundle',   # What to call the new bundle
    csvdir_equities(
        ['daily'],  # Are these daily or minute bars
        '/Users/matthewchuang/Documents/GitHub/algo_test/datas/20200105',  # Directory where the formatted bar data is
    ),
    calendar_name='NYSE', # US equities default
    start_session=start_session,
    end_session=end_session
)


start_session = pd.Timestamp('2020-11-6', tz='utc')
end_session = pd.Timestamp('2021-1-5', tz='utc')

register(
    'minute-bundle',   # What to call the new bundle
    csvdir_equities(
        ['minute'],  # Are these daily or minute bars
        '/Users/matthewchuang/Documents/GitHub/algo_test/datas/20210106/',  # Directory where the formatted bar data is
    ),
    calendar_name='NYSE', # US equities default
    start_session=start_session,
    end_session=end_session
)




"""
Some commandline reference code on ingesting and cleaning up data bundles
zipline bundles
zipline clean -b custom-csvdir-bundle --keep-last 1
zipline clean -b custom-csvdir-bundle --after 2020-10-1
zipline ingest -b test-csvdir
"""

# ssh -i "algot.pem" ubuntu@ec2-18-167-41-96.ap-east-1.compute.amazonaws.com
# zipline run -f main.py -o test7.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark --capital-base 10000