# pandas-usaddress
The usaddress library made easy with Pandas.

Also supports standardizing addresses to meet USPS standards.

# Installation

pip install pandas-usaddress

# Usage

### Basic Parsing

    import pandas as pd
    import pandas_usaddress

    #load dataframe
    df = pd.read_csv('test_file.csv')

    #initiate usaddress
    df = pandas_usaddress.tag(df, ['address_field'])

    #send output to csv
    df.to_csv('parsed_output.csv')
    
    
    #------------------------------additional details------------------------------

    #Output and fields will be identical to usaddress

### Parsing with Address Standardization

    import pandas as pd
    import pandas_usaddress

    #load dataframe
    df = pd.read_csv('test_file.csv')

    #initiate usaddress
    df = pandas_usaddress.tag(df, ['address_field'], granularity='medium', standardize=True)

    #send output to csv
    df.to_csv('parsed_output.csv')
    
    
    #------------------------------additional details------------------------------

    #The standard output for usaddress has a lot of fields. The granularity parameter
    #allows you to condense the results you get back for different types of analysis.
    #see parameter documentation below for all granularity options.
    
    #Addresses are often unstandardized. The same address can come as 123 1st ST, or
    #123 First Street, etc. This can cause issues with analysis such as aggregation,
    #or record matching. The standardize parameter attempts to standardize the address
    #to US Postal Service (USPS) standards.
    
### Parsing with Address Standardization

    import pandas as pd
    import pandas_usaddress

    #load dataframe
    df = pd.read_csv('test_file.csv')

    #initiate usaddress
    df = pandas_usaddress.tag(df, ['street1', 'street2', 'city', 'state'], granularity='single', standardize=True)

    #send output to csv
    df.to_csv('parsed_output.csv')
    
    
    #------------------------------additional details------------------------------
    
    #You can also use pandas-usaddress to concatenate and parse multiple address lines. 
    #This can be helpful when you are working with two datasets that have different 
    #field names and you want the field names to be standardized using a specific level of
    #granularity. It's pretty common for instance that in one dataset will concatenate 
    #address line 1 and 2, and another will not.
    
    #You will help the parser do it's job if you try to concatenate fields in approximately
    #same order that you would write them on an envelope.
    
    #In this instance, we are taking multiple address fields and converting them into a
    #single address line. That's fine to do!
    

