import pandas as pd
import usaddress
import csv

from pkg_resources import resource_filename
filepath = resource_filename(__name__, 'abbreviations.csv')

with open(filepath) as abb_file:
    abb_reader = csv.reader(abb_file)
    abb_dict = dict(abb_reader)

usaddress_fields = [
                    "AddressNumber",
                    "AddressNumberPrefix",
                    "AddressNumberSuffix",
                    "BuildingName",
                    "CornerOf",
                    "IntersectionSeparator",
                    "LandmarkName",
                    "NotAddress",
                    "OccupancyType",
                    "OccupancyIdentifier",
                    "PlaceName",
                    "Recipient",
                    "StateName",
                    "StreetName",
                    "StreetNamePreDirectional",
                    "StreetNamePreModifier",
                    "StreetNamePreType",
                    "StreetNamePostDirectional",
                    "StreetNamePostModifier",
                    "StreetNamePostType",
                    "SubaddressIdentifier",
                    "SubaddressType",
                    "USPSBoxGroupID",
                    "USPSBoxGroupType",
                    "USPSBoxID",
                    "USPSBoxType",
                    "ZipCode"
                    ]

def usaddress_field_creation(x,i):
    try:
        return x[0][i]
    except:
        None

def trim(x):
    x = str(x)
    x = x.split()
    x = ' '.join(x)
    if len(x) == 0:
        return None
    else:
        return x

def taggit(x):
    try:
        return usaddress.tag(x)
    except:
        None


                
        
def tag(dfa, address_columns, granularity='medium'):
    df = dfa.copy()
    df['address'] = ""
    for i in address_columns:
        df[i].fillna('', inplace=True)        
    df['address'] = df['address'].str.cat(df[address_columns].astype(str), sep=" ", na_rep='')
    df['address'] = df['address'].str.replace('[^\w\s]','')
    df['address'] = df['address'].apply(lambda x: trim(x))
    df['address'] = df['address'].apply(lambda x: x.upper())
    df['address'] = df['address'].apply(lambda x: taggit(x))
    
    for i in usaddress_fields:
        df[i] = df['address'].apply(lambda x: usaddress_field_creation(x,i))
        
    df["StreetNamePreDirectional"] = df["StreetNamePreDirectional"].apply(lambda x: abb_dict.get(x, x))
    df["StreetNamePreType"] = df["StreetNamePreType"].apply(lambda x: abb_dict.get(x, x))
    df["StreetNamePostDirectional"] = df["StreetNamePostDirectional"].apply(lambda x: abb_dict.get(x, x))
    df["StreetNamePostType"] = df["StreetNamePostType"].apply(lambda x: abb_dict.get(x, x))
            


    
    if granularity=='full':
        pass
    
    elif granularity=='high':
        df.drop(columns=["AddressNumberPrefix",
                         "AddressNumberSuffix",
                         "CornerOf",
                         "IntersectionSeparator",
                         "LandmarkName",
                         "NotAddress",
                         "USPSBoxGroupID",
                         "USPSBoxGroupType",],inplace=True)
        
    elif granularity=='medium':
        df['StreetNamePrefix'] = ''
        df['StreetNamePrefix'] = df['StreetNamePrefix'].str.cat(df[['StreetNamePreModifier', 'StreetNamePreType']], sep=" ", na_rep='')
        df['StreetNamePrefix'] = df['StreetNamePrefix'].apply(lambda x: trim(x))
        
        df['StreetNameSuffix'] = ''
        df['StreetNameSuffix'] = df['StreetNameSuffix'].str.cat(df[['StreetNamePostType', 'StreetNamePostModifier']], sep=" ", na_rep='')
        df['StreetNameSuffix'] = df['StreetNameSuffix'].apply(lambda x: trim(x))
        
        df['USPSBox'] = ''
        df['USPSBox'] = df['USPSBox'].str.cat(df[['USPSBoxType', 'USPSBoxID']], sep=" ", na_rep='')
        df['USPSBox'] = df['USPSBox'].apply(lambda x: trim(x))
        
        df['OccupancySuite'] = ''
        df['OccupancySuite'] = df['OccupancySuite'].str.cat(df[['OccupancyType', 'OccupancyIdentifier']], sep=" ", na_rep='')
        df['OccupancySuite'] = df['OccupancySuite'].apply(lambda x: trim(x))
        
        df.drop(columns=["Recipient",
                         "BuildingName",
                         "SubaddressType",
                         "SubaddressIdentifier",                             
                         "AddressNumberPrefix",
                         "AddressNumberSuffix",
                         "CornerOf",
                         "IntersectionSeparator",
                         "LandmarkName",
                         "NotAddress",
                         "USPSBoxGroupID",
                         "USPSBoxGroupType",
                         "StreetNamePreModifier",
                         "StreetNamePreType",
                         "StreetNamePostType",
                         "StreetNamePostModifier",
                         "USPSBoxType",
                         "USPSBoxID",
                         "OccupancyType",
                         "OccupancyIdentifier"],inplace=True)
        
    elif granularity=='low':
        df['StreetTag'] = ""
        df['StreetTag'] = df['StreetTag'].str.cat(df[["AddressNumber",
                                                      "StreetNamePreDirectional",
                                                      "StreetNamePreModifier",
                                                      "StreetNamePreType",
                                                      "StreetName",
                                                      "StreetNamePostType",
                                                      "StreetNamePostModifier",
                                                      "StreetNamePostDirectional",
                                                      "USPSBoxType",
                                                      "USPSBoxID",
                                                      "OccupancyType",
                                                      "OccupancyIdentifier"]], sep=" ", na_rep='')
        df['StreetTag'] = df['StreetTag'].apply(lambda x: trim(x))
        
        
        df.drop(columns=["Recipient",
                         "BuildingName",
                         "SubaddressType",
                         "SubaddressIdentifier",                             
                         "AddressNumberPrefix",
                         "AddressNumberSuffix",
                         "CornerOf",
                         "IntersectionSeparator",
                         "LandmarkName",
                         "NotAddress",
                         "USPSBoxGroupID",
                         "USPSBoxGroupType",
                         "StreetNamePreModifier",
                         "StreetNamePreType",
                         "StreetNamePostType",
                         "StreetNamePostModifier",
                         "USPSBoxType",
                         "USPSBoxID",
                         "OccupancyType",
                         "OccupancyIdentifier",
                         "AddressNumber",
                         "StreetNamePreDirectional",
                         "StreetName",
                         "StreetNamePostDirectional"],inplace=True)
    
    
    
    elif granularity=='single':
        df['SingleLine'] = ""
        df['SingleLine'] = df['SingleLine'].str.cat(df[["AddressNumber",
                                                      "StreetNamePreDirectional",
                                                      "StreetNamePreModifier",
                                                      "StreetNamePreType",
                                                      "StreetName",
                                                      "StreetNamePostType",
                                                      "StreetNamePostModifier",
                                                      "StreetNamePostDirectional",
                                                      "USPSBoxType",
                                                      "USPSBoxID",
                                                      "OccupancyType",
                                                      "OccupancyIdentifier",
                                                      "PlaceName",
                                                      "StateName",
                                                      "ZipCode"]], sep=" ", na_rep='')
        df['SingleLine'] = df['SingleLine'].apply(lambda x: trim(x))
        
        
        df.drop(columns=["Recipient",
                         "BuildingName",
                         "SubaddressType",
                         "SubaddressIdentifier",                             
                         "AddressNumberPrefix",
                         "AddressNumberSuffix",
                         "CornerOf",
                         "IntersectionSeparator",
                         "LandmarkName",
                         "NotAddress",
                         "USPSBoxGroupID",
                         "USPSBoxGroupType",
                         "StreetNamePreModifier",
                         "StreetNamePreType",
                         "StreetNamePostType",
                         "StreetNamePostModifier",
                         "USPSBoxType",
                         "USPSBoxID",
                         "OccupancyType",
                         "OccupancyIdentifier",
                         "AddressNumber",
                         "StreetNamePreDirectional",
                         "StreetName",
                         "StreetNamePostDirectional",
                         "PlaceName",
                         "StateName",
                         "ZipCode"],inplace=True)
        
        
        
    return df