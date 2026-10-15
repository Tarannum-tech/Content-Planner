from pytrends.request import TrendReq

def get_trends(keyword: str, timeframe='today 3-m'):
    pytrends = TrendReq(hl='en-US', tz=330)
    pytrends.build_payload([keyword], timeframe=timeframe, geo='IN')
    data = pytrends.interest_over_time()
    related = pytrends.related_queries()
    return data, related