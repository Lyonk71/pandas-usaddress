import pandas as pd
import numpy as np
import usaddress
import csv

# reference abbreviations for street names
from pkg_resources import resource_filename
filepath = resource_filename(__name__, 'abbreviations.csv')

with open(filepath) as abb_file:
    abb_reader = csv.reader(abb_file)
    abb_dict = dict(abb_reader)
    
# reference numbered_street file
    from pkg_resources import resource_filename
filepath = resource_filename(__name__, 'numbered_streets.csv')

with open(filepath) as num_file:
    num_reader = csv.reader(num_file)
    num_dict = dict(num_reader)
    
# reference street_numbers file
    from pkg_resources import resource_filename
filepath = resource_filename(__name__, 'street_numbers.csv')

with open(filepath) as str_file:
    str_reader = csv.reader(str_file)
    str_dict = dict(str_reader)

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
        
def lowercase(x):
    try:
        return x.lower()
    except:
        pass
                      
        
def tag(dfa, address_columns, granularity='full', standardize=False):
    df = dfa.copy()
    df['odictaddress'] = ""
    for i in address_columns:
        df[i].fillna('', inplace=True)        
    df['odictaddress'] = df['odictaddress'].str.cat(df[address_columns].astype(str), sep=" ", na_rep='')
    df['odictaddress'] = df['odictaddress'].str.replace('[^\w\s\-]','')
    df['odictaddress'] = df['odictaddress'].apply(lambda x: trim(x))
    df['odictaddress'] = df['odictaddress'].apply(lambda x: lowercase(x))
    df['odictaddress'] = df['odictaddress'].apply(lambda x: taggit(x))

    
    for i in usaddress_fields:
        df[i] = df['odictaddress'].apply(lambda x: usaddress_field_creation(x,i))
        
    
        
    df = df.drop(columns='odictaddress')              
        
    if standardize==False:
        pass
    
    # standardize parameter
    elif standardize==True:
        df["StreetNamePreDirectional"] = df["StreetNamePreDirectional"].apply(lambda x: abb_dict.get(x, x))
        df["StreetNamePreType"] = df["StreetNamePreType"].apply(lambda x: abb_dict.get(x, x))
        df["StreetNamePostDirectional"] = df["StreetNamePostDirectional"].apply(lambda x: abb_dict.get(x, x))
        df["StreetNamePostType"] = df["StreetNamePostType"].apply(lambda x: abb_dict.get(x, x))        
        df["StreetName"] = df["StreetName"].apply(lambda x: num_dict.get(x, x))
        df["AddressNumber"] = df["AddressNumber"].apply(lambda x: str_dict.get(x, x))
        
        
    
    else:
        raise ValueError('standardize parameter must be either True or False')     


    
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
        df['StreetTag'] = df['StreetTag'].str.cat(df[[#"AddressNumber",
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
                         #"AddressNumber",
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
        
    df = df.replace({'None': np.nan, 'none': np.nan, 'nan': np.nan, 'NaN': np.nan, None: np.nan, '': np.nan}).copy()

        
    return df