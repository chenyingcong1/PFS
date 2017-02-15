# import nmap
# nm = nmap.PortScannerYield()
# for i in nm.scan('113.105.76.129/25', '80'):
#     print(i)
import nmap

nm = nmap.PortScannerYield()
# print(nm.scan('113.105.76.194/25','80'))
for i in nm.scan(hosts='113.105.76.182/25', arguments='-sn'):
    print(i)
# print(i[0],':',i[1]['nmap']['scanstats']['uphosts'])

# ('113.105.76.182',
#  {'nmap':
#       {'command_line': 'nmap -oX - -p 80 -sV 113.105.76.182',
#        'scaninfo':{'tcp':{'method': 'syn', 'services': '80'}},
#        'scanstats':{'downhosts': '0', 'elapsed': '12.44', 'timestr': 'Wed Feb 15 14:30:32 2017', 'totalhosts': '1', 'uphosts': '1'}
#        },
#   'scan':{'113.105.76.182':
#               {'tcp':
#                    {80:
#                         {'product': 'Apache httpd', 'cpe': 'cpe:/a:apache:http_server:2.2.21', 'reason': 'syn-ack', 'state': 'open', 'conf': '10', 'extrainfo': '(Unix) DAV/2', 'version': '2.2.21', 'name': 'http'}
#                     },
#                'vendor':{},
#                'addresses':{'ipv4': '113.105.76.182'},
#                'hostnames':[{'type': '', 'name': ''}],
#                'status':{'reason': 'echo-reply', 'state': 'up'}
#            }
#       }
#   }
#  )
#
# ('113.105.76.194',
#  {'scan': {},
#   'nmap': {'scaninfo': {'tcp': {'method': 'syn', 'services': '80'}},
#            'scanstats': {'uphosts': '0', 'elapsed': '9.15', 'totalhosts': '1', 'timestr': 'Wed Feb 15 14:32:59 2017', 'downhosts': '1'},
#            'command_line': 'nmap -oX - -p 80 -sV 113.105.76.194'}
#   }
#  )
