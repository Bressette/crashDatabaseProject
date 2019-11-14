import pandas
import numpy as np

#function that separates date and time then returns the date
def get_date(s):
    s = s.rsplit("T", maxsplit=1)[0]
    return s

#function that separates date and time then returns the time
def get_time(s):
    s = s.rsplit("T", maxsplit=1)[1]
    s = s.rsplit(".", maxsplit=1)[0]
    return s

#function that declares a dataframe weather drops duplicates and creates new column
#to hold the index of the dataframe and stores it as condID for a primary key column
def create_weather(df):
    df_weather = df[['Weather', 'SurfaceCondition', 'DayNight']]
    df_weather.drop_duplicates(keep='first', inplace=True)
    df_weather.reset_index(inplace=True, drop=True)
    df_weather.index += 1
    df_weather['condID'] = df_weather.index;
    df_weather = df_weather.rename(columns={'Weather': 'weather', 'SurfaceCondition': 'surfaceCond', 'DayNight': 'dayNight'})
    df_weather = df_weather[['condID', 'weather', 'surfaceCond', 'dayNight']]
    return df_weather

#function that declares a dataframe location drops duplicates and creates new column
#to hold the index of the dataframe and stores it as locID for a primary key column
def create_location(df):
    df_location = df[['STREETADDRESS', 'CITYORTOWN', 'RoadCharacteristics']]
    df_location.drop_duplicates(keep='first', inplace=True)
    df_location.reset_index(inplace=True, drop=True)
    df_location.index += 1
    df_location['locID'] = df_location.index;
    return df_location


#function that declares a dataframe driver drops duplicates and creates new column
#to hold the index of the dataframe and stores it as driverID for a primary key column
def create_driver(df):
    df_driver = df[['Impairment', 'InjuryType']]
    df_driver.drop_duplicates(keep='first', inplace=True)
    df_driver.reset_index(inplace=True, drop=True)
    df_driver.index += 1
    df_driver['driverID'] = df_driver.index
    return df_driver


def export_animal(df):
    df['accID'] = df.index
    df_animal = df[['accID', 'Animal']]
    df_animal = df_animal.dropna(axis=0, subset=['Animal'])
    df_export_animal = df_animal[df_animal.Animal != "None/Other"]
    df_export_animal = df_export_animal.rename(columns={'Animal': 'animalType'})
    df_export_animal.to_csv("animal.csv", index=False)
    return df_export_animal

def export_vehicle(df):
    df_vehicle = df[['accID', 'Involving']]
    df_export_vehicle = df_vehicle[df_vehicle.Involving != "None"]
    df_export_vehicle = df_export_vehicle.dropna(subset=['Involving'])
    df_export_vehicle.to_csv("vehicle.csv", index=False)
    return df_export_vehicle


def format_location(mergedCity):
    mergedCity.drop(['CITYORTOWN'], axis=1, inplace=True)
    mergedCity = mergedCity.rename(columns={"STREETADDRESS": "streetAddress", "RoadCharacteristics": "roadChar"})
    mergedCity = mergedCity[["locID", "cityID", "streetAddress", "roadChar"]]
    mergedCity["roadChar"] = mergedCity["roadChar"].replace(to_replace="Other - Explain in Narrative",
                                                                      value="Not Reported")
    mergedCity["roadChar"] = mergedCity["roadChar"].fillna("Not Reported")
    mergedCity["streetAddress"] = mergedCity["streetAddress"].fillna("Not Reported")
    return mergedCity


def sanitize_collision_dir(df):
    df['collisionDir'] = df['collisionDir'].replace(to_replace="No Turns, Thru moves only, Broadside ^<",
                                                    value="No Turns, Thru moves only, Broadside")
    df['collisionDir'] = df['collisionDir'].replace(to_replace="Left Turn and Thru, Angle Broadside -->v--",
                                                    value="Left Turn and Thru, Angle Broadside")
    df['collisionDir'] = df['collisionDir'].replace(to_replace="Left Turn and Thru, Broadside v<--",
                                                    value="Left Turn and Thru, Broadside")
    df['collisionDir'] = df['collisionDir'].replace(to_replace="Left Turn and Thru, Head On ^v--",
                                                    value="Left Turn and Thru, Head On")
    df['collisionDir'] = df['collisionDir'].replace(to_replace="Left Turns, Same Direction, Rear End v--v--",
                                                    value="Left Turns, Same Direction, Rear End")
    df['collisionDir'] = df['collisionDir'].replace(to_replace="Right Turn and Thru, Angle Broadside -->^--",
                                                     value="Right Turn and Thru, Angle Broadside")
    df['collisionDir'] = df['collisionDir'].replace(to_replace="Right Turn and Thru, Head On v^--",
                                                    value="Right Turn and Thru, Head On")
    df['collisionDir'] = df['collisionDir'].replace(to_replace="Right Turn and Thru, Broadside ^<--",
                                                    value="Right Turn and Thru, Broadside")
    df['collisionDir'] = df['collisionDir'].replace(to_replace="Left and Right Turns, Simultaneous Turn Crash --vv--",
                                                    value="Left and Right Turns, Simultaneous Turn Crash")
    df['collisionDir'] = df['collisionDir'].replace(to_replace="Right Turn, Same Direction, Rear End ^--^--",
                                                    value="Right Turn, Same Direction, Rear End")
    return df


def sanitize_weather(df_weather):
    df_weather['surfaceCond'] = df_weather['surfaceCond'].replace(to_replace="Not Reported", value="Unknown")
    df_weather['surfaceCond'] = df_weather['surfaceCond'].replace(to_replace="Other - Explain in Narrative",
                                                                  value="Unknown")
    df_weather['surfaceCond'] = df_weather['surfaceCond'].fillna("Unknown")
    df_weather['dayNight'] = df_weather['dayNight'].fillna("Unknown")
    df_weather.to_csv("Weather CSV.csv", index=False)
    return df_weather


def sanitize_driver(df_driver):
    df_driver['driverImpair'] = df_driver['driverImpair'].fillna("None")
    df_driver['driverDamage'] = df_driver['driverDamage'].fillna("Unknown")
    df_driver.to_csv("driver.csv", index=False)
    return df_driver


def create_city(df_location):
    df_city = df_location[['CITYORTOWN']]
    df_city.drop_duplicates(keep='first', inplace=True)
    df_city.reset_index(inplace=True, drop=True)
    df_city.index += 1
    df_city['cityID'] = df_city.index
    return df_city


def export_city(df_city):
    df_city.rename(columns={'CITYORTOWN': 'cityName'}, inplace=True)
    df_city = df_city[['cityID', 'cityName']]
    df_city.to_csv("city.csv", index=False)
    return df_city


def export_address(mergedAddress, df_location):
    df_export_address = mergedAddress[['streetAddress', 'cityID']]
    df_export_address.drop_duplicates(keep='first', inplace=True)
    df_export_address.reset_index(inplace=True, drop=True)
    df_export_address.index += 1
    df_export_address['addressID'] = df_export_address.index
    df_export_address = df_export_address[['addressID', 'streetAddress', 'cityID']]
    df_export_address.to_csv("address.csv", index=False)
    return df_export_address


def create_address(df_location):
    df_address = df_location[['STREETADDRESS']]
    df_address['addressID'] = df_address.index
    df_address = df_address.rename(columns={'STREETADDRESS': 'streetAddress'})
    return df_address


def export_location(mergedAddress):
    mergedAddress.drop(['locID'], axis=1, inplace=True)
    mergedAddress.drop_duplicates(keep='first', inplace=True)
    mergedAddress.reset_index(inplace=True, drop=True)
    mergedAddress.index += 1
    mergedAddress['locID'] = mergedAddress.index
    mergedAddress = mergedAddress[['locID', 'addressID', 'roadChar']]
    mergedAddress.to_csv("location.csv", index=False)
    return mergedAddress


def create_accident(df, df_location, df_weather, df_driver):
    # create dataframe to store data for accident
    df_accident = df[['DirOfCollision', 'ACCIDENTDATE', 'ReportingAgency']]

    # set accDate to the date portion of the ACCIDENTDATE field through applying the get_date function
    df_accident["accDate"] = df_accident["ACCIDENTDATE"].apply(get_date)

    # set accTime to the time portion of the ACCIDENTDATE field through applying the get_time function
    df_accident["accTime"] = df_accident["ACCIDENTDATE"].apply(get_time)
    # remove the useless end of the time field using rstrip
    df_accident["accTime"] = df_accident["accTime"].map(lambda x: x.rstrip('.'));

    # drops the now useless datetime field
    df_accident.drop(['ACCIDENTDATE'], axis=1, inplace=True)

    # create new dataframe to hold only the fields that need to be in the accident table
    df_accident = df_accident[['DirOfCollision', 'accDate', 'accTime', 'ReportingAgency']]
    df_accident.rename(columns={'ReportingAgency': 'agency', 'DirOfCollision': 'collisionDir'}, inplace=True)

    # merge df and df_location so that the master table has the location primary key
    mergedLocation = pandas.merge(df, df_location, how='left', left_on=['RoadCharacteristics'],
                                  right_on=['roadChar'])

    # merge df and df_weather so that the master table has the weather primary key
    mergedWeather = pandas.merge(df, df_weather, how='left', left_on=['Weather', 'SurfaceCondition', 'DayNight'],
                                 right_on=['weather', 'surfaceCond', 'dayNight'])

    # merge df and df_driver so that the master table has the location primary key
    mergedDriver = pandas.merge(df, df_driver, how='left', left_on=['Impairment', 'InjuryType'],
                                right_on=['driverImpair', 'driverDamage'])

    # create fields in accident to hold foreign key values from merged dataframes
    df_accident['driverID'] = mergedDriver['driverID']
    df_accident['condID'] = mergedWeather[['condID']]
    df_accident['locID'] = mergedLocation[['locID']]
    return df_accident


def export_accident(df_accident):
    df_export_accident = df_accident[['locID', 'condID', 'driverID', 'collisionDir', 'accDate', 'accTime',
                                      'agency']]
    df_export_accident.index += 1
    df_export_accident['accID'] = df_export_accident.index
    df_export_accident = df_export_accident[
        ['accID', 'locID', 'condID', 'driverID', 'collisionDir', 'accDate', 'accTime',
         'agency']]
    df_export_accident['collisionDir'] = df_export_accident['collisionDir'].replace(
        to_replace="Other - Explain in Narrative", value="Unknown")
    df_export_accident['collisionDir'] = df_export_accident['collisionDir'].fillna("Unknown")
    df_export_accident = sanitize_collision_dir(df_export_accident)
    df_export_accident.to_csv("accident.csv", index=False)
    return df_export_accident


#df is the base data frame that the data is stored as
df = pandas.read_csv("All Data.csv")

#stores dataframes for weather, location, driver dataframes
df_weather = create_weather(df)
df_location = create_location(df)
df_driver = create_driver(df)
df_animal = export_animal(df)
df_vehicle = export_vehicle(df)


df_city = create_city(df_location)
df_address = create_address(df_location)

mergedCity = pandas.merge(df_location, df_city, how='left', left_on=['CITYORTOWN'], right_on=['CITYORTOWN'])
mergedCity = format_location(mergedCity)

mergedAddress = pandas.merge(mergedCity, df_address, how='left', left_on=['streetAddress'],
                                 right_on=['streetAddress'])

df_address = export_address(mergedAddress, df_location)
df_location = export_location(mergedAddress)
df_city = export_city(df_city)


df_driver = df_driver.rename(columns={'Impairment': 'driverImpair', 'InjuryType': 'driverDamage'})
df_driver = df_driver[['driverID', 'driverImpair', 'driverDamage']]

df_accident = create_accident(df, df_location, df_weather, df_driver)
df_accident = export_accident(df_accident)



df_weather = sanitize_weather(df_weather)
df_driver = sanitize_driver(df_driver)








