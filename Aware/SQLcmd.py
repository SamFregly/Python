import os
import re
import sys
from PyEmail import send_log
import psycopg2
import datetime
from cryptography.fernet import Fernet
estat = False

import logging
now2 = datetime.datetime.now()
day = int(now2.today().strftime('%Y%m%d'))-1
today = now2.today().strftime('%Y-%m-%d')
estat = True


def get_key():
    
    with open('C:/Users/vfgadmin/AppData/Local/Programs/Python/Python36-32/secret_key.bin', 'rb') as file_object:
        for line in file_object:
            key = line

    cipher_suite = Fernet(key)
    
    with open('C:/Users/vfgadmin/AppData/Local/Programs/Python/Python36-32/cryptobin.bin', 'rb') as file_object:
        for line in file_object:
            encryptedpwd = line

    uncipher_text = (cipher_suite.decrypt(encryptedpwd))
    normal = bytes(uncipher_text).decode("utf-8")
    return normal
get_key()



def SQL_process(input_csv, staging_table,prod_tbl,t1):  # this is the flow of processing a table(main[] post csv processing)
    error_msg = []  # store success of each step in SQL commands
    # 1. Bulk Insert
    # 2. necessary transformations # have no idea what to do here just yet as of 11/6, built for scaling
    # 3. copy from staging to final
    # 4. delete (not drop) staging table]
    # ONLY FOR NFS FILES
    staging_name = staging_table
    #############################################
    #############################################
    #############################################
    final_name = prod_tbl #######################
    #############################################
    #############################################
    #############################################
    delete = SQL_make_qry(staging_table, command_type="DELETE")
    D = SQL_run_cmd(delete,file = input_csv,cmd_type ='Delete')
    insert = SQL_make_qry(staging_table, csv_path=input_csv, command_type='BULK',values = t1)  # 1. B
    A = SQL_run_cmd(insert, file = input_csv,cmd_type = 'Bulk')
    print('A.insert')
    transform = SQL_make_qry(staging_table,command_type = 'TRANSFORM')
    B = SQL_run_cmd(transform,file = input_csv,cmd_type ='Transform')
    print('B.TRANSFORM')
    everything = SQL_make_qry(staging_table,tablename2=final_name, command_type = 'DEFAULT')
    C = SQL_run_cmd(everything,file = input_csv,cmd_type ='DEFAULT')
    print('leaving sql_proc')
    logging.info(':::{0}::: SQL commands successfull on {1} for file {2}'.format(staging_table,today,input_csv))
    return (A,B,C)

#########################################################
#########################################################
def SQL_make_qry(tablename1, tablename2='NULL', csv_path='NULL', command_type='BULK',values = '',
                 msg='NULL'):  # sets up bulk upload command to SQL table table1 = staging table2 = final 
    print('in sql_command {0}'.format(command_type))
    # tablename1 is used for the staging table in cases where tablename2 is not null .
    # this is usually called from SQL_process. This does exist as its own function just in case.
    if command_type == 'BULK':
        command = "COPY "+tablename1 + values+ " FROM '" + csv_path +"' DELIMITER ',' CSV ;"
        print(command)
        return command
    elif command_type == 'TRANSFORM':
        if True
            return
        else:
            return
        print(command)
        return command
    elif command_type == 'MOVE':
        command = "INSERT INTO {0} select * FROM {1};".format(tablename2,tablename1)
        print(command)
        return command
    elif command_type == 'DELETE':
        command = "DELETE FROM {0};".format(tablename1)
        print(command)
        return command
    elif command_type == 'ALTER':
        return command
    elif command_type == 'RE-ALTER':
        return command
    elif command_type == 'DEFAULT':
        return command
    else:
        return 'FAILURE'
    
###########################################################
def SQL_run_cmd(command, file = None ,cmd_type='DEFAULT'):  # creates SQL connection and uploads CSV file
    # tbl2 can act as a secondary string for transform commands or as the second table for multi table commands
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M")
    success = 'start pf sql_run_cmd {0}:::'.format(date)
    password = get_key()
    try:
        cnxn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password={0}".format(password))
        cur = cnxn.cursor()
        
        success += cmd_type + ' connection:::'
    except Exception as ex:
        print(ex)
        logging.debug('{0}, {1},{2} CONNECTION ERROR CHECK STATUS OF SERVER \n'.format(now,ex,file))
        send_log(email,log_file,'NFS Connection Broke ',estat)
    c = str(command)
    cur.execute(c)
    success += cmd_type +' execute:::'
    try:
        cnxn.commit()
    except pyodbc.Error as ex:
        logging.debug('{0}, {1},{2} COMMITING ERROR CHECK THINGS \n'.format(now,ex,a))
        send_log(email,log_file,'Commit Failure',estat)
        cnxn.close()
    success += cmd_type+' commit:::'
    try:
        cnxn.close()
        success += cmd_type+ ' Connection Closed:::'
    except exception as inst:
         logging.debug('{0}, unable to close sql connection??? \n {1} {2}'.format(now,inst,file))
         send_log(email,log_file,'Connection Close Failure',estat)
         return success
    print('command {0} ran succesfully'.format(cmd_type))
    cnxn.close()
    return success


def SQL_select(command, limit = '100'):
    cmd = command + ' limit ' + limit 
    cnxn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='}{P';l?><'")
    cur = cnxn.cursor()
    cur.execute(cmd)
    data = cur.fetchall()
    cnxn.close()
    return data

