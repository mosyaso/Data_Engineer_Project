from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
from configparser import ConfigParser
from pprint import PrettyPrinter

ASHOST='xxxxxxx'
CLIENT='xxx'
SYSNR='xx'
USER='xxxxxxx'
PASSWD='xxxxxx'
conn = Connection(ashost=ASHOST, sysnr=SYSNR, client=CLIENT, user=USER, passwd=PASSWD)

try:
    options = [{ 'TEXT': "FCURR = 'USD'"}]
    pp = PrettyPrinter(indent=4)
    ROWS_AT_A_TIME = 100
    rowskips = 0
    while True:
        print("----Begin of Batch---")
        result = conn.call('RFC_READ_TABLE', \
                            QUERY_TABLE = 'TCURR', \
                            OPTIONS = options, \
                            ROWSKIPS = rowskips, ROWCOUNT = ROWS_AT_A_TIME)
        pp.pprint(result['DATA'])

        rowskips += ROWS_AT_A_TIME
        if len(result['DATA']) < ROWS_AT_A_TIME:
            break
except CommunicationError:
    print("Could not connect to server.")
    raise
except LogonError:
    print("Could not log in. Wrong credentials?")
    raise
except (ABAPApplicationError, ABAPRuntimeError):
    print("An error occurred.")
    raise
