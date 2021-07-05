#!/usr/bin/env python3

import requests
import re
import datetime
import os


def main():
   swim_pool_in_page = requests.get("https://www.kravihora-brno.cz/kryta-plavecka-hala", verify=False).content.decode('utf-8')
   swim_pool_out_page = requests.get("https://www.kravihora-brno.cz/venkovni-bazeny", verify=False).content.decode('utf-8')

   occupancy_re = re.compile(r".*Obsazenost: <strong>(\d*|Err)<\/strong><\/p>.*")
   air_temp_in_re = re.compile(r".*Teplota vzduch hala: <strong>(\d*\.{0,1}\d*)\s*°C<\/strong><\/p>.*")
   air_temp_out_re = re.compile(r".*Teplota vzduchu: <strong>(\d*\.{0,1}\d*)\s*°C<\/strong><\/p>.*")

   watter_temp_in_re = re.compile(r".*Teplota vnitřní bazén: <strong>(\d*\.{0,1}\d*)\s*°C<\/strong><\/p>.*")
   watter_temp_out_re = re.compile(r".*Teplota vody.*: <strong>(\d*\.{0,1}\d*)\s*°C<\/strong><\/p>.*")


   occupancy_in_match = occupancy_re.search(swim_pool_in_page)
   occupancy_out_match =  occupancy_re.search(swim_pool_out_page)

   occupancy_in = 0
   if occupancy_in_match.group(1) != 'Err':
       occupancy_in = occupancy_in_match.group(1)

   occupancy_out = 0
   if occupancy_out_match.group(1) != 'Err':
       occupancy_out = occupancy_out_match.group(1)

   air_temp_in = air_temp_in_re.search(swim_pool_in_page).group(1)
   air_temp_out = air_temp_out_re.search(swim_pool_out_page).group(1)
   watter_temp_in = watter_temp_in_re.search(swim_pool_in_page).group(1)
   watter_temp_out = watter_temp_out_re.search(swim_pool_out_page).group(1)

   timestamp = datetime.datetime.now() 
   os.system("echo {0},{1},{2},{3},{4},{5},{6} >> /home/franta_hrdina/scripts/pool_stats/pool_stats.txt"
       .format(timestamp, occupancy_in, air_temp_in, watter_temp_in, 
       occupancy_out, air_temp_out, watter_temp_out))

if __name__ == '__main__':
    main()

