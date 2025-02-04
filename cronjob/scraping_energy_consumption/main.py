import os
import time
import pandas as pd
import argparse

from prometheus_api_client import PrometheusConnect
from pandas import json_normalize

def scrape(num: int = 1000, 
  df_name: str = 'df.csv'
) -> None:
  while not os.path.exists(df_name) or \
    (os.path.exists(df_name) and len(pd.read_csv(df_name)) < num):
    # Prometheus setup    
    prom = PrometheusConnect(
      url='http://prometheus.integration',
      disable_ssl=True
    )
    
    # Execute custom query
    query = 'kepler_container_joules_total{pod_name=~"^uc2.*"}'
    
    result = prom.custom_query(
      query = query
    )
    
    #print(result)
    ### Process to dataframe
    df = json_normalize(result)
    # Filter dynamic
    df = df[df['metric.mode']=='dynamic']
    
    # Split time and value
    df[['time', 'joules']] = df['value'].tolist()
    df = df.drop('value', axis=1)
    print(df)
    
    # Load previous one if exists
    if os.path.exists(df_name):
      df_prev = pd.read_csv(df_name)
      df = pd.concat([df, df_prev], ignore_index=True)
      # Remove duplicate
      df.drop_duplicates(
        subset='metric.pod_name', 
        keep='last',
        inplace=True
      )
    
    # Save
    df.to_csv(df_name, index=False)

    # Sleep
    time.sleep(300)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='Scraping pod energy consumption for n data points'
  )  
  parser.add_argument('-n', '--num', 
    help='number of data points to collect', 
    type=int,
    default=1000)
  args = parser.parse_args()

  scrape(num=args.num)
