"""
5 Day / 1 Minute, including today's data:

https://api.tdameritrade.com/v1/marketdata/XYZ/pricehistory?periodType=day&period=5&frequencyType=minute&frequency=1&endDate=1464825600000


5 Day / 1 Minute, excluding today's data:

https://api.tdameritrade.com/v1/marketdata/XYZ/pricehistory?periodType=day&period=5&frequencyType=minute&frequency=1


6 Months / 1 Day, including today's data:

https://api.tdameritrade.com/v1/marketdata/XYZ/pricehistory?periodType=month&frequencyType=daily&endDate=1464825600000

Note that periodType=month is specified because the default periodType is day which is not compatible with the frequencyType daily


Daily from May 25th, 2016 to today:

https://api.tdameritrade.com/v1/marketdata/XYZ/pricehistory?periodType=month&frequencyType=daily&startDate=1464148800000&endDate=1464825600000


WORKING OPTION CHAIN FOR SPY EXAMPLE
https://api.tdameritrade.com/v1/marketdata/chains?apikey=SknGuPiaoAlgo&symbol=SPY&contractType=PUT&strikeCount=5&strategy=SINGLE&range=ITM&optionType=S

WORKING REQUEST FOR TSLA YTD TO CURRENT DATE
https://api.tdameritrade.com/v1/marketdata/TSLA/pricehistory?apikey=SknGuPiaoAlgo&periodType=ytd&period=1&frequencyType=daily&endDate=1585115769000

"""


"""
BEARER CODE
https://localhost:8080/?code=%2BNjCoGcRpOsQJcGKrSmFFzhuqms0LevdosObjUcnBMOjkIANWSpo1%2BfgG5glVVJBw%2By9tER7wb5bJgUtG1cTEwsHTod%2FYYIyaTXa%2BxBTB597ShWL4wbTVPfVLKb6bS%2FxVXlkyQZ6%2FbpZN%2BaoS%2BwYsCxo3up%2Bl%2B4Hd4Px15UhCk%2BqCp1%2BV%2B8vKNj9oXeT9Br7YrtHEJKvgL00HIA5wBypkRKrAncuFBZ%2BpzZGegwxR08JzQqyWGHwuKv%2FXSHcuW%2FS9pK2L4kUdYVL4fGMqyEwYk%2BpcXrkKEX1sRdn3Si6wf6MUIGN1ychqeyFwpRuU4uoNM7%2FY2%2FRCOFXVloMdsSiE7xAqy59hEz0FpuZce1F87K51HEUWOD3lNsY6XgBVi0V14A6PEtxYk1fc8TOL3%2BCxWf33n5zP%2FTORKeLggTLtnYwti9Q94ALpZBzYDG100MQuG4LYrgoVi%2FJHHvlYltS5FyVeM4hrrtnsj6geD0EV1uNhLjfYkkVt%2FJWO%2FVmwpFjs9Tm%2BwxKIaxL6Qqnbmx5YGEt7Q6e4kGavTY%2FaYOs7xMqPDxx67ps8rbbHnvE7ACplgT42e0eZmU1VYFwfNaSdlgOiPuFavMGR7XqIiL5%2FDP4t%2BYQLxtrVRYbWFSPIoelbm0O26Z0aIkZg2CXrvOGyB3gVXvcdHmQYk0XPB40BqofHOvinL6jR9YusFIAr%2B%2Fbpmh7FmwZeUlrQJ0iGVhzQtXT0ZqJNEeYGUSfdO2yspC1BELY7RECMFsHGc6EyWd2scSFKzaQyw3g6rGKZ8K9%2Bke7wd3cz0n7bXd0V5QSAMH8MbEvmEa%2B1UfPFPYhi6tYuRYBcbf1wc9wKjw57dpED6W2md2fHQSA%2BRaogbntmxurm00GcLjNyNz20IwwlesYUimVjUwLvKg%3D212FD3x19z9sWBHDJACbC00B75E
"""
