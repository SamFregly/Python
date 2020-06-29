
import pandas as pd
import os
import csv
import numpy as np
from openpyxl import load_workbook
import datetime
import sys
import timeit
import time
start_time = time.time()

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 50)

nfs_c_names = ['RR2',                       'Advisor Name (RR2)',
                'Primary Account Holder',   'Account #',
                'Primary Email Address',    'SSN/TIN#',
                'SSN/TIN Type',             'Client SSN / TIN',
                'Reg Type',                 'Managed Account Type',
                'Open/Closed Indicator',    'Total Account Value']

nfs_c_order_final = ['Client Number',           'Rep_No',
                    'Advisor Name (RR2)',       'Osj',
                    'Primary Account Holder',   'ACCOUNTNUM_',
                    'Primary Email Address',    'Email Y/N',
                    'Found_Email_Address',      'SSN',
                    'SSN/TIN Type',             'OpenClosed_Indicator',
                    'Total Account Value',      'Client SSN / TIN',
                    'Managed Account Type',     'Reg Type']

jaccomo_c_names = ['ACCOUNTNUM_',           'OWNER_NAME',
                   'FIRSTNAME_',            'SSN','ADDRESS1_',
                   'ADDRESS2_',             'CITY',
                   'STATE',                 'ZIP_',
                   'LASTNAME_',             'DATEOPENED_',
                   'BALANCE_',              'ADVISOR',
                   'REPORTINGCOMPANY_',     'ACCOUNT_TYPE',
                   'SUBTYPE_',              'OWNERSHIP_',
                   'EMPLOYEEEXTERNALID_']

j_c_order_final = [ 'Client Number',            'ACCOUNTNUM_',
                    'OWNER_NAME',               'SSN',
                    'Found_Email_Address',      'OpenClosed_Indicator',
                    'Data_Source',              'BALANCE_',
                    'Osj',                      'DATEOPENED_',
                    'Email?',                   'Rep_No',
                    'FIRSTNAME_',               'ADDRESS1_',
                    'ADDRESS2_',                'CITY',
                    'STATE',                    'ZIP_',
                    'LASTNAME_',                'ADVISOR',
                    'Reporting_Company',        'ACCOUNT_TYPE',
                    'SUBTYPE_','OWNERSHIP_',    'Custodian_SYM',
                    'Custodian', 'In_NFS']

dst_c_names = ['MANAGEMENT COMPANY','INVESTMENT DESCRIPTION',
                'CUSIP','ACCT/CONTRACT#',
                'ROA','ACCOUNT STATUS',
                'ACCOUNT TYPE','ACCOUNT TYPE DESCRIPTION',
                'MATRIX LEVEL','BIN','DEALER','TRUST',
                'TPA','BRANCH','REP/ADVISOR',
                'ACCOUNT VALUE','AS OF','SHARE BALANCE',
                'ISSUED SHARES','UNISSUED SHARES',
                'ESCROW-SHARES','AUTO AGREE 1 TYPE',
                'AUTO AGREE 1 DESC','AUTO AGREE 1 AMOUNT',
                'AUTO AGEE 2 TYPE',
                'AUTO AGREE 2 DESC','AUTO AGREE 2 AMOUNT',
                'TOTAL # AUTO AGREE ON ACCT',
                'DIVIDENDS','SHORT TERM',
                'LONG TERM','REGISTRATION 1',
                'REGISTRATION 2','REGISTRATION 3',
                'REGISTRATION 4','REGISTRATION 5',
                'REGISTRATION 6','REGISTRATION 7',
                'INVESTMENT TYPE','ACCOUNT ESTABLISHMENT DATE' ]

NFS_in_path =  'C:/Temp/Client Counts by Rep.xlsx'
Jaccomo_in_path = 'C:/Temp/Jaccomo All Clients.csv'
DST_extract = 'C:/Temp/dstextract_5.11.20.CSV'


def count_clients(df, rep = 'Rep_No', ssn = 'SSN'):
    df = df.sort_values(by = [rep,ssn])
    df = df.reset_index(drop = True)          # reset index so the client numbering will work
    df['Client Number'] = np.nan               #initialize column to null
    df.loc[0,'Client Number'] = 1              #set first value to 1

    for i in range(1,len(df)):                 # loop through and increment based on client number from specific valu
        if df.ix[i,rep] == df.ix[i-1,rep] and df.ix[i,ssn] != df.ix[i-1,ssn]:    
            df.ix[i,'Client Number'] = df.ix[i-1,'Client Number']+1
        elif df.ix[i,rep] == df.ix[i-1,rep] and df.ix[i,ssn] == df.ix[i-1,ssn]:    
            df.ix[i,'Client Number'] = df.ix[i-1,'Client Number']    
        else: 
            df.ix[i,'Client Number'] = 1
    return df


def get_dst_df(data_extract):
    
    df1 = pd.read_csv(data_extract, header = 0, na_values=['','NA'], dtype = {'ACCT/CONTRACT#':str})
    df1 = df1.loc[:, ['ACCT/CONTRACT#', 'ACCOUNT STATUS','ACCOUNT VALUE']]
    df1.rename({'ACCT/CONTRACT#' : 'ACCOUNTNUM_',
                'ACCOUNT STATUS' : 'OpenClosed_Indicator',
                'RR2':'Rep_No'},axis = 'columns',inplace = True)
    df1 = df1[df1['ACCOUNT VALUE'] > 0.0]
    df1 = df1.loc[:, ['ACCOUNTNUM_', 'OpenClosed_Indicator']]
    return df1

def get_nfs_df(account_file):
    xls = pd.ExcelFile(account_file)
    df1 = xls.parse('Raw', index_col=None, na_values=['NA'],converters={'RR2':str, 'SSN/TIN#':str,'Client SSN / TIN':str})
    df1['SSN/TIN#'] = (df1['SSN/TIN#']     # the "integer" column
               # the integer column
             .astype(str)  # cast integers to string
             .str.zfill(9) # zero-padding
             .pipe(lambda s: s.str[:3] + '-' + s.str[3:5] + '-' + s.str[5:]))
    df1.rename({'SSN/TIN#':'SSN',
                'Open/Closed Indicator':'OpenClosed_Indicator',
                'Account #' : 'ACCOUNTNUM_',
                'RR2':'Rep_No'},axis = 'columns',inplace = True)
    df1['Client SSN / TIN'] = (df1['Client SSN / TIN']     # the "integer" column
               # the integer column
             .astype(str)  # cast integers to string
             .str.zfill(9)) # zero-padding
             #.pipe(lambda s: s.str[:3] + '-' + s.str[3:5] + '-' + s.str[5:]))
    df1 = df1.drop_duplicates(keep = 'first')
    df2 = df1.sort_values(['Primary Email Address','SSN'],ascending = False)[['SSN','Primary Email Address']].drop_duplicates(keep ='first').copy()
            # sorts them, pulls out SSN and Email columns, drops any row duplicates and copies it into df2
    df2.rename({'Primary Email Address':'Found_Email_Address'},axis = 'columns',inplace = True)
    
    df1['Email Y/N'] =  pd.notna(df1['Primary Email Address'])
    df1 = df1.sort_values(['SSN','ACCOUNTNUM_'])               #sort on social and account
    df1 = pd.merge(df1,df2, on = 'SSN', how ='left')           # merge in emails from other accounts based on primary social
    #################                                           Basic cleaning of files is complete gets a new name
    print(df1.columns)
    print(osj_sheet.columns)
    df3 = pd.merge(df1,osj_sheet, on = 'Rep_No' , how = 'left')        # Merge in OSJ Data
   
    #df3.rename({'RR2':'Rep_No'},axis = 'columns',inplace = True)
    df3 = df3.drop_duplicates(['ACCOUNTNUM_','SSN'])       # remove account duplicates that occur due to other merges
   
    df3 = count_clients(df3)                        # to add in client counts
    df3 = df3[nfs_c_order_final]                    #reorder columns

    df3.fillna(value="Unconfirmed")
    NFS_open = df3[df3['OpenClosed_Indicator']== 'Open']
    NFS_open = NFS_open[NFS_open.Osj != 'House']
    NFS_open = NFS_open[NFS_open['Advisor Name (RR2)'] != 'Unknown']                
    NFS_open_p = NFS_open[NFS_open['Total Account Value'] >  0]
    NFS_open_n = df3[df3['Total Account Value'] <  0]            
    NFS_0 = df3[df3['Total Account Value'] == 0]

    NFS_house = df3[df3.Osj == 'House']
    NFS_unknown = df3[df3['Advisor Name (RR2)'] == 'Unknown']

    NFS_closed = df3[df3[ 'OpenClosed_Indicator']== 'Closed']
    NFS_closed = NFS_closed[NFS_closed['Total Account Value'] >=  0]
    NFS_closed = NFS_closed[NFS_closed['Advisor Name (RR2)'] !=  'Unknown']

    all_clean = df3
    return [all_clean,NFS_open_p,NFS_open_n,NFS_house,NFS_unknown,NFS_closed]



def get_osj_df(account_file):
    xls = pd.ExcelFile(account_file)
    df = xls.parse('OSJ Mapping', index_col=None, na_values=['NA'],converters={'Rep No':str})
    return df
    

def get_jaccomo_dfs(client_file):
    df1 = pd.read_csv(client_file, header = 0, na_values=['NA'], dtype = {'SSN':str})
    df1['DATEOPENED_'] =  pd.to_datetime(df1['DATEOPENED_'], format='%Y-%m-%d %H:%M:%S')
    df1.rename({'REPORTINGCOMPANY_':'Reporting_Company',
                'EMPLOYEEEXTERNALID_':'Rep_No'},axis = 'columns',inplace = True)

    df1['SSN'] = (df1['SSN']     # the "integer" column
               # the integer column
            .astype(str)        # cast integers to string
            .str.zfill(9) # zero-padding
            .pipe(lambda s: s.str[:3] + '-' + s.str[3:5] + '-' + s.str[5:]))

    df1.loc[(df1.Reporting_Company == 'NFSC'),'Reporting_Company'] = 'NFSC^NFSC^NFSC'
     # fix blank data source
          
            
    df1[['Data_Source','Custodian_SYM','Custodian']] = df1.Reporting_Company.astype(str).str.split('^',expand = True)
    # populate data source-Custodian-custodian symbol fields from Reporting_Company Field
          # fille in blank data source fields
    df1 = df1.sort_values(by = ['Rep_No','OWNER_NAME'])
    df1 = df1.reset_index(drop = True)
    df1 = pd.merge(df1,osj_sheet, on = 'Rep_No' , how = 'left')  # mapped in  and OSJ
          # fill in blank OSJ field
    df1 = df1.drop_duplicates(['ACCOUNTNUM_','SSN','BALANCE_'])  # dropped duplicates

    NFS_ssn = NFS_all.loc[:, ['SSN', 'Found_Email_Address']]   # Get SSN and Emails from NFS
    NFS_ssn = NFS_ssn.drop_duplicates(['SSN'])
    NFS_ssn['In_NFS'] = True

    
    df1 = pd.merge(df1,NFS_ssn, on = 'SSN' , how = 'left') # left join on 'SSN' column
    df1 = df1.drop_duplicates(['ACCOUNTNUM_','SSN','BALANCE_'])     #remove duplicates from merge things

    NFS_acct = NFS_all.loc[:, ['ACCOUNTNUM_','OpenClosed_Indicator']]        # prep to merge in open/closed ind

    NFS_acct['ACCOUNTNUM_'] = NFS_acct['ACCOUNTNUM_'].str.replace('-','') # remove '-' so they match
    NFS_acct = NFS_acct.append(DST_status)
    NFS_acct['OpenClosed_Indicator'] = NFS_acct['OpenClosed_Indicator'].str.replace('OPEN','Open')
    
    df1 = pd.merge(df1,NFS_acct, on = 'ACCOUNTNUM_' , how = 'left') # merge on account number  This only affects to NFS accounts in jaccomo
    
    df1['Email?'] = df1['Found_Email_Address'].notnull()
    place_holder = df1.filter(['Data_Source','Osj','BALANCE_','OpenClosed_Indicator','DATEOPENED_','In_NFS','Custodian'], axis = 1)
    for i in range(1,len(place_holder)):# loop through mark non NFSC accounts as closed
        if place_holder.ix[i,'Data_Source'] not in['DST','DAZL','NFSC']:
             place_holder.ix[i,'Data_Source'] = 'DST'
        if place_holder.ix[i,'Osj'] == 'nan':
            place_holder.ix[i,'Osj'] = 'Unconfirmed' 
    
        date_before = datetime.datetime(2018, 1, 1)             # anything with 0 balance opened more than 3 years ago is closed
        if place_holder.ix[i,'Custodian'] != 'NFSC' and str(place_holder.ix[i,'OpenClosed_Indicator']) =='nan' :
            #print(place_holder.ix[i,'OpenClosed_Indicator'])
            if (place_holder.ix[i,'BALANCE_'] == 0 and
                place_holder.ix[i,'DATEOPENED_'] < date_before):    
                    place_holder.ix[i,'OpenClosed_Indicator'] = 'Closed'
            elif place_holder.ix[i,'BALANCE_'] > 0:
                    place_holder.ix[i,'OpenClosed_Indicator'] = 'Open'
            elif place_holder.ix[i,'BALANCE_'] < 0:
                    place_holder.ix[i,'OpenClosed_Indicator'] = 'Negative'
            else:
                    place_holder.ix[i,'OpenClosed_Indicator'] = 'Unconfirmed'
        elif (place_holder.ix[i,'Custodian'] == 'NFSC' and
              place_holder.ix[i,'DATEOPENED_'] > datetime.datetime(2020, 1, 1)):
                place_holder.ix[i,'OpenClosed_Indicator'] = 'Open'
        else:
            place_holder.ix[i,'OpenClosed_Indicator'] = 'Unconfirmed'
                
        if place_holder.ix[i,'In_NFS'] != True:                      # populate blanks
            place_holder.ix[i,'In_NFS'] = False
            
        if place_holder.ix[i,'Osj'] == 'NaN':
            place_holder.ix[i,'Osj'] = 'Unconfirmed' 
        #if '@' not in str(df1.ix[i,'Found Email Address']):
        #    df1.ix[i,'Email?'] = False
    print(df1.columns)
    df1[['Data_Source','Osj','BALANCE_','OpenClosed_Indicator','DATEOPENED_','In_NFS']] = place_holder[['Data_Source','Osj','BALANCE_','OpenClosed_Indicator','DATEOPENED_','In_NFS']]        
    df1 = df1.sort_values(by = ['Rep_No','OWNER_NAME'])     
    df1 = df1.drop_duplicates(['ACCOUNTNUM_','SSN','BALANCE_'])
    #print('DF1.columns:::  ', df1.columns)
    
    
    J_house = df1[df1['Osj'] == 'House']
    #print(J_house)
    DAZL = df1[df1['Data_Source'] != 'NFSC']
    DAZL = DAZL[DAZL['Osj'] != 'House']
    DAZL_open = DAZL[DAZL['OpenClosed_Indicator'] == 'Open']
    
    DST  = df1[df1['Data_Source'] == 'DST']
    DST = DST[DST['Osj'] != 'House']
    DST_open  = DST[DST['OpenClosed_Indicator'] == 'Open']
    
    NFSC = df1[df1['Data_Source'] == 'NFSC']
    NFSC = NFSC[NFSC['Osj'] != 'House']
    NFSC_open = NFSC[NFSC['OpenClosed_Indicator'] == 'Open']

    DAZL_closed = DAZL[DAZL['OpenClosed_Indicator'] == 'Closed']
    DST_closed  = DST[DST['OpenClosed_Indicator'] == 'Closed']
    NFSC_closed = NFSC[NFSC['OpenClosed_Indicator'] == 'Closed']
    
    DST_DZL_myb = df1[df1['Data_Source'] != 'NFSC']
    DST_DZL_myb = DST_DZL_myb[DST_DZL_myb['OpenClosed_Indicator'] == '?Open?']
    
    
    #print(DST.columns)
    return [df1 , DAZL_open , DST_open, NFSC_open , DAZL_closed , DST_closed , NFSC_closed , DST_DZL_myb, J_house]

########################################################################################################
########################################################################################################

global osj_sheet
global NFS_out
global Jaccomo_client_file
global DST_status


DST_status = get_dst_df(DST_extract)
osj_sheet = get_osj_df(NFS_in_path)



NFS_out = get_nfs_df(NFS_in_path)
print(NFS_out[0].columns)
NFS_out[:] = [count_clients(x) for x in NFS_out] 

NFS_all = NFS_out[0]
NFS_open_p = NFS_out[1]
NFS_open_n = NFS_out[2] 
NFS_house  = NFS_out[3]
NFS_unknown  = NFS_out[4]
NFS_closed  = NFS_out[5]

path = r'C:/Temp/Open AccountsV3.5.xlsx'
path2 = r'C:/Temp/Closed and Other AccountsV3.5.xlsx'

Jac_out = get_jaccomo_dfs(Jaccomo_in_path)
Jac_out[:] = [count_clients(x) for x in Jac_out]            # add in client number by rep
Jac_out[:] = [x[j_c_order_final] for x in Jac_out]

Jaccomo_client_file = Jac_out[0]
Jaccomo_DAZL_open = Jac_out[1]
Jaccomo_DST_open = Jac_out[2]
Jaccomo_NFSC_open = Jac_out[3]
Jaccomo_DAZL_closed = Jac_out[4]
Jaccomo_DST_closed = Jac_out[5]
Jaccomo_NFSC_closed = Jac_out[6]
Jaccomo_NFSC_maybeopen = Jac_out[7]
Jaccomo_house = Jac_out[8]




with pd.ExcelWriter(path, mode='w') as writer:
    Jaccomo_client_file.to_excel(writer, sheet_name='J_ALL', index=False)
    #Jaccomo_DAZL_open.to_excel(writer, sheet_name='Direct_open', index=False)
    #Jaccomo_DST_open.to_excel(writer, sheet_name='DST_open', index=False)
    #Jaccomo_NFSC_open.to_excel(writer, sheet_name='J_NFSC_open', index=False)
    Jaccomo_house.to_excel(writer, sheet_name='J_House_all', index=False)


    NFS_all.to_excel(writer, sheet_name='NFS_all', index=False) 
   # NFS_open_p.to_excel(writer, sheet_name='NFS_open_p', index=False) 
  #  NFS_open_n.to_excel(writer, sheet_name='NFS_open_n', index=False)
    NFS_house.to_excel(writer, sheet_name='NFS_house', index=False)  



     
#with pd.ExcelWriter(path2, mode='w') as writer2:
   # NFS_closed.to_excel(writer2, sheet_name='NFS_closed', index=False)  
   # Jaccomo_DAZL_closed.to_excel(writer2, sheet_name='Direct_closed', index=False) 
   # Jaccomo_DST_closed.to_excel(writer2, sheet_name='DST_closed', index=False) 
   # Jaccomo_NFSC_closed.to_excel(writer2, sheet_name='J_NFS_closed', index=False) 
   # Jaccomo_NFSC_maybeopen.to_excel(writer2, sheet_name='NFS_maybeopen', index=False)
   # NFS_unknown.to_excel(writer, sheet_name='NFS_unknown', index=False)




print("--- %s seconds ---" % (time.time() - start_time))




















