#!/usr/bin/env python3

# Copyright 2017 Brocade Communications Systems, Inc.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may also obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""

:mod:`switchiproutedelete` - PyFOS util for deleting a switch IP route.
********************************************************************************
The :mod:`switchiproutedelete` provides IP route delete functionality.

This module is a standalone script that can be used to delete an extension
IP route.

* inputs:
    * -L=<login>: Login ID. If not provided, interactive
        prompt will request one.
    * -P=<password>: Password. If not provided, interactive
        prompt will request one.
    * -i=<IP address>: IP address
    * -n=<name>: slot/port name of the GE port.
    * -d=<dp-id>: DP instance.
    * -s=<ip-address>: source IP address.
    * -g=<ip-gateway>: IP gateway address.
    
* outputs:
    * Python dictionary content with RESTCONF response data.


.. function:: switchiproutedelete.delete_extension_iproute(session, name,\
dp, ip, prefix, gateway = None)
    
    *Delete extension IP route* 

        Example usage of the method::
        
                ret = switchiproutedelete.delete_extension_iproute(session,\
                name, dp, ip, prefix, gateway)
                print (ret)
                
        Details::
        
            IProute = {
                            "name": name,
                            "dp-id": dp,
                            "ip-address": ip
                            "ip-prefix-length": prefix
                            "ip-gateway": gateway
                      }
            result = switchiproutecreate._delete_extension_iproute(session, IProute)

        * inputs:
            :param session: session returned by login.
            :param name: GE port name expressed as slot/port.
            :param dp-id: DP Instance.
            :param ip: Extension IP-Address.
            :param prefix: Prefix length for the IP Address.
            :param gateway: IP address gateway.


        * outputs:    
            :rtype: dictionary of return status matching rest response

        *use cases*

        1. Delete an new extension IP route     
"""
import pyfos.pyfos_auth as pyfos_auth
import pyfos.pyfos_util as pyfos_util
from pyfos.pyfos_extension_iproute import extension_iproute
import getpass
import getopt
import sys
import pyfos.utils.brcd_util as brcd_util

isHttps = "0"


def parse_iproute(user_command, inputs,  value_dict):
	try:
		opts, args = getopt.getopt(user_command,"i:n:d:s:g:p:f:",
                ["switch=","name=","dp-id=","ip-address=", "ip-gateway=",
                 "mtu-size=", "ip-prefix-length=","fid=", ])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	status = 1
	for opt, arg in opts:
		if opt in ("-i", "--switch"):
			inputs.update({'switch': arg})
			status = 0
		elif opt in ("-f", "--vfid="):
			inputs.update({'fid': arg})
		if opt in ("-n", "--name"):
			value_dict.update({'name': arg})
		elif opt in ("-d", "--dp-id="):
			value_dict.update({'dp-id': arg})	
		elif opt in ("-s", "--ip-address="):
			value_dict.update({'ip-address': arg})
		elif opt in ("-g", "--ip-gateway="):
			value_dict.update({'ip-gateway': arg})
		elif opt in ("-m", "--mtu-size="):
			value_dict.update({'mtu-size': arg})
		elif opt in ("-p", "--ip-prefix-length="):
			value_dict.update({'ip-prefix-length': arg})
	if status == 0:
		login = input("Login:")
		password = getpass.getpass()
		inputs.update({'login': login})
		inputs.update({'password': password})
	return status


def _delete_extension_iproute(session, value_dict):
	iprouteobject = extension_iproute(value_dict)
	result = iprouteobject.delete(session)
	return result

def delete_extension_iproute(session, name, dp, ip, prefix, gateway = None):
        value_dict = {'name': name, 'dp-id':dp, 'ip-address': ip,
                      'ip-prefix-length':prefix , 'ip-gateway': gateway}
        result = _delete_extension_iproute(value_dict)
        return result
  

def usage():
	print ("usage:")
	print ('switchipiproutedelete.py -i <ipaddr> -n <name> -d <dp-id> ' +\
               '-s <ip-address> -p <ip-prefix-length> -g<ip-gateway>]')



def main(argv):
        
	#myinput=str("-i 10.17.3.70  -n 4/17 -d 0 -s 154.10.10.0 " +\
        #            "-g 134.10.10.25 -p 24 ")
	#argv = myinput.split()
	value_dict = dict()
	inputs = dict()
	ret = parse_iproute(argv, inputs, value_dict)
	if ret != 0:
		usage()
		sys.exit()

	session = pyfos_auth.login(inputs["login"], inputs["password"],
                                   inputs["switch"], isHttps)
	if pyfos_auth.is_failed_login(session):
		print ("login failed because",
			session.get(pyfos_auth.CREDENTIAL_KEY)[pyfos_auth.LOGIN_ERROR_KEY])
		usage()
		sys.exit()

	brcd_util.exit_register(session)

	vfid = None
	if 'vfid' in inputs:
		vfid = inputs['vfid']
		
	if vfid is not None:
		pyfos_auth.vfid_set(session, vfid)

	if "name" not in value_dict:
		pyfos_auth.logout(session)
		usage()
		sys.exit()

	if "ip-address" not in value_dict:
		pyfos_auth.logout(session)
		usage()
		sys.exit()

	if "ip-prefix-length" not in value_dict:
		pyfos_auth.logout(session)
		usage()
		sys.exit()

	if "dp-id" not in value_dict:
		pyfos_auth.logout(session)
		usage()
		sys.exit()        
	result = _delete_extension_iproute(session, value_dict)
	pyfos_util.response_print(result)
	pyfos_auth.logout(session)
    

if __name__ == "__main__": main(sys.argv[1:])
