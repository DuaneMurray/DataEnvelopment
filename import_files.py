#########################################################################################
# IMPORT DIRECTORY OF CSV FILES INTO MYSQL DB
#   MOVE PROCESSED FILES TO ARCHIVE DIR
#   INSERT CONCATED DATAFRAME INTO DB
#
# SOURCE: https://www.analystfactory.com/how-to-import-csv-files-into-mysql-with-python
#########################################################################################

import os
import mysql.connector
import shutil
from sqlalchemy import create_engine
import pandas as pd
from glob import glob

#import db_config as cfg

# USER, PW, AND DB ARE BEING IMPORTED FROM dbconfig.py FILE
#db_data = ("mysql+mysqlconnector://{user}:{pw}@localhost/{db}"
#           .format(user = cfg.mysql["user"],
#                   pw = cfg.mysql["passwd"],
#                   db = cfg.mysql["db"]))

# USER, PW, AND DB ARE BEING IMPORTED FROM dbconfig.py FILE
db_data = ("mysql+mysqlconnector://{user}:{pw}@localhost/{db}"
           .format(user = "vsc",
                   pw = "blaster123",
                   db = "stockdata"))          

# USING 'CREATE_ENGINE' FROM SQLALCHEMY TO MAKE THE DB CONNECTION
engine = create_engine(db_data).connect()

# FiLEPATHS OF WHERE THE SOURCE FILES ARE AND WHERE TO MOVE THEM AFTER PROCESSING
# USE ONE SOURCE DIRECTORY AT A TIME
# current_dir = os.getcwd()

########################################################
# COMPANY DETAIL DATA FILES:
source = 'Data\\Stock-Details\\'
dest = 'Data\\Stock-Details\\Archive\\'


########################################################
# FUNDMENTAL DATA FILES:
#source = 'Technology\\Fundamentals\\'
#dest = 'Technology\\Fundamentals\\Archive\\'
#
#source = 'Energy\\Fundamentals\\'
#dest = 'Energy\\Fundamentals\\Archive\\'
#
#source = 'Financial\\Fundamentals\\'
#dest = 'Financial\\Fundamentals\\Archive\\'
#
#source = 'Healthcare\\Fundamentals\\'
#dest = 'Healthcare\\Fundamentals\\Archive\\'
#
#source = 'Industrials\\Fundamentals\\'
#dest = 'Industrials\\Fundamentals\\Archive\\'
#
#source = 'Materials\\Fundamentals\\'
#dest = 'Materials\\Fundamentals\\Archive\\'
#
#source = 'RealEstate\\Fundamentals\\'
#dest = 'RealEstate\\Fundamentals\\Archive\\'
#
#source = 'Telecom\\Fundamentals\\'
#dest = 'Telecom\\Fundamentals\\Archive\\'
#
#source = 'Utilities\\Fundamentals\\'
#dest = 'Utilities\\Fundamentals\\Archive\\'
#
#source = 'ConsumerDiscretionary\\Fundamentals\\'
#dest = 'ConsumerDiscretionary\\Fundamentals\\Archive\\'
#
#source = 'ConsumerStaples\\Fundamentals\\'
#dest = 'ConsumerStaples\\Fundamentals\\Archive\\'
#########################################################

#########################################################
# PRICE QUOTE DATA FILES:
#source = 'Technology\\PriceHistory\\'
#dest = 'Technology\\PriceHistory\\Archive\\'
#
#source = 'Energy\\PriceHistory\\'
#dest = 'Energy\\PriceHistory\\Archive\\'
#
#source = 'Financial\\PriceHistory\\'
#dest = 'Financial\\PriceHistory\\Archive\\'
#
#source = 'Healthcare\\PriceHistory\\'
#dest = 'Healthcare\\PriceHistory\\Archive\\'
#
#source = 'Industrials\\PriceHistory\\'
#dest = 'Industrials\\PriceHistory\\Archive\\'
#
#source = 'Materials\\PriceHistory\\'
#dest = 'Materials\\PriceHistory\\Archive\\'
#
#source = 'RealEstate\\PriceHistory\\'
#dest = 'RealEstate\\PriceHistory\\Archive\\'
#
#source = 'Telecom\\PriceHistory\\'
#dest = 'Telecom\\PriceHistory\\Archive\\'
#
#source = 'Utilities\\PriceHistory\\'
#dest = 'Utilities\\PriceHistory\\Archive\\'
#
#source = 'ConsumerDiscretionary\\PriceHistory\\'
#dest = 'ConsumerDiscretionary\\PriceHistory\\Archive\\'
#
#source = 'ConsumerStaples\\PriceHistory\\'
#dest = 'ConsumerStaples\\PriceHistory\\Archive\\'
#########################################################


# USE THE GLOB MODULE TO CREATE A LIST OF FILES IN THE SOURCE PATH
import_files = sorted(glob(source + "*.csv"))

# GET THE COUNT OF FILES IN THE import_files LIST
filecount = len(import_files)

# IF THERE ARE NO CSV FILES IN THE SOURCE DIR PRINT MESSAGE
if filecount < 1:
    print("No files found in: " + source)

# IF THERE ARE FILES IN THE SOURCE CREATE THE DATAFRAME
else:
    df = pd.concat((pd.read_csv(file).assign(filename=file)
                    for file in import_files), ignore_index=True)
    
    # MOVE THE FILES FROM THE SOURCE PATH TO THE DEST PATH
    for file in import_files:
        shutil.move(file, dest)

    # PRINT THE DATAFRAME TO THE CONSOLE
    print(df)


# INSERT THE DATAFRAME INTO THE TABLE
# name = 'database_table_name'
#
# IF VERY LARGE DATA SET, USE CHUNKSIZE:
# Chunksize number is: 
#       chunksize = (2100 / your number of columns)
# https://stackoverflow.com/questions/50645445/python-pandas-to-sql-maximum-2100-parameters

#####################################################################
# FINANCIALS INSERT
#
#df.to_sql(name='financials', con=engine, chunksize=430, if_exists='replace') # REPLANCE ENTIRE TABLE WITH NEW ONE
df.to_sql(name='company_details', con=engine, chunksize=5000, if_exists='append') # ADD DATA TO EXISTING TABLE
#df.to_sql(name='financials', con=engine, chunksize=430, if_exists='append') # ADD DATA TO EXISTING TABLE
#df.to_sql(name='financials', con=engine, chunksize=430, if_exists='append') # ADD DATA TO EXISTING TABLE
#
#####################################################################

################################################################################
# PRICE QUOTE INSERT
#
#df.to_sql(name='price_quotes', con=engine, chunksize=430, if_exists='replace') # REPLANCE ENTIRE TABLE WITH NEW ONE
#df.to_sql(name='price_quotes', con=engine, chunksize=430, if_exists='append') # ADD DATA TO EXISTING TABLE
#
################################################################################


# NOTIFY SUCCESS
print("File import complete.")
