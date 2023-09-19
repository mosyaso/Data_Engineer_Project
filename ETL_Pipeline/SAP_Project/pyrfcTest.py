# import pyrfc

# if __name__ == '__main__':
#     print('\n\nDone!')

#     sid = {
#             'ASHOST' : 'MBSAPDEV01',
#             'CLIENT' : '800',
#             'SYSNR' : '00',
#             'USER' : 'SCHBASIS',
#             'PASSWD' :'m@l@ko77'
#     }

#     with pyrfc.Connection(**sid) as sapcon:
#         print('\n\nComplete')

#________

# from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
# from configparser import ConfigParser
# from pprint import PrettyPrinter

# ASHOST='MBSAPDEV01'
# CLIENT='800'
# SYSNR='00'
# USER='SCHBASIS'
# PASSWD='m@l@ko77'
# conn = Connection(ashost=ASHOST, sysnr=SYSNR, client=CLIENT, user=USER, passwd=PASSWD)

# try:
#     options = [{'TEXT': "FCURR='USD'"}]
#     pp = PrettyPrinter(indent=4)
#     ROWS_AT_A_TIME = 10
#     rowskips = 0
#     while True:
#         print("----Begin of Batch---")
#         result = conn.call('RFC_READ_TABLE', \
#                             QUERY_TABLE = 'TCURR', \
#                             OPTIONS = options, \
#                             ROWSKIPS = rowskips, ROWCOUNT = ROWS_AT_A_TIME)
#         pp.pprint(result['DATA'])

#         rowskips += ROWS_AT_A_TIME
#         if len(result['DATA']) < ROWS_AT_A_TIME:
#             break
# except CommunicationError:
#     print("Could not connect to server.")
#     raise
# except LogonError:
#     print("Could not log in. Wrong credentials?")
#     raise
# except(ABAPApplicationError,ABAPRuntimeError):
#     print("An error occurred.")
#     raise

#__________________

######Call ABAP Function Module from Python

# from pyrfc import Connection
# conn = Connection(ashost='MBSAPDEV01', sysnr='00', client='800', user='SCHBASIS', passwd='m@l@ko77')

# # ABAP variables are mapped to Python variables
# result = conn.call('STFC_CONNECTION', REQUTEXT=u'Hello SAP!')
# print (result)
# {u'ECHOTEXT': u'Hello SAP!',
#  u'RESPTEXT': u'SAP R/3 Rel. 702   Sysid: ABC   Date: 20121001   Time: 134524   Logon_Data: 100/ME/E'}

# # ABAP structures are mapped to Python dictionaries
# IMPORTSTRUCT = { "RFCFLOAT": 1.23456789, "RFCCHAR1": "A" }

# # ABAP tables are mapped to Python lists, of dictionaries representing ABAP tables' rows
# IMPORTTABLE = []

# result = conn.call("STFC_STRUCTURE", IMPORTSTRUCT=IMPORTSTRUCT, RFCTABLE=IMPORTTABLE)

# print result["ECHOSTRUCT"]
# { "RFCFLOAT": 1.23456789, "RFCCHAR1": "A" ...}

# print result["RFCTABLE"]
# [{ "RFCFLOAT": 1.23456789, "RFCCHAR1": "A" ...}]