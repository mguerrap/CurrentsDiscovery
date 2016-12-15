import datetime as dt

# List of Full Moons during 2014
Full_2014 = ["20140115", "20140214", "20140316", "20140415", "20140514",
             "20140612", "20140712", "20140810", "20140908", "20141008",
             "20141106", "20141206"]

# List of New Moons during 2014
New_2014 = ["20140101", "20140130", "20140301", "20140330", "20140428",
            "20140528", "20140627", "20140726", "20140825", "20140923",
            "20141023", "20141122", "20141221"]

# List of First Quarter Moons during 2014
First_2014 = ["20140107", "20140206", "20140308", "20140407", "20140506",
              "20140605", "20140705", "20140803", "20140902", "20141001",
              "20141030", "20141129", "20141228"]

# List of Third Quarter Moons during 2014
Third_2014 = ["20140123", "20140222", "20140323", "20140422", "20140521",
              "20140619", "20140718", "20140817", "20140915", "20141015",
              "20141114", "20141214"]


def mcddatetime(Moon):
    """Makes Moon Cycle date into datetime format for plotting"""
    dates = [(dt.datetime.strptime(date, '%Y%m%d').date() +
              pd.DateOffset(hours=0)) for date in Moon]
    modified_data = pd.to_datetime(dates)
    return modified_data
