##python vn.py --api_server_ip '10.204.216.64' --keystone_ip '10.204.216.150' --n_vns 10 
##python vn.py --api_server_ip '10.204.216.64' --keystone_ip '10.204.216.150' --n_vns 10 --cleanup

from vnc_api.vnc_api import *
import argparse
import random
import socket
import struct
import sys
import time
from netaddr import *
alloc_addr_list = list()

class VNC(object):
    def __init__(self, username, password, tenant, ip, port, auth_host):
        self.vnc = VncApi(api_server_host=ip,
                          api_server_port=port,
                          username=username,
                          password=password,
                          tenant_name=tenant,
                          auth_host=auth_host)
        self.project_fqname = ['default-domain', tenant]
        self.vn_obj = dict()
        self.vm_obj = dict()
        self.port_obj = dict()

    def get_project_id(self):
        return self.vnc.fq_name_to_id('project', self.project_fqname)

    def create_network(self, vn_name, mask=16):
        ''' Create virtual network using VNC api '''
        cidr = get_random_cidr(mask=mask).split('/')[0]
        vn_obj = VirtualNetwork(vn_name, fq_name=self.project_fqname+[vn_name],
                                parent_type='project')
        vn_obj.add_network_ipam(NetworkIpam(),
                                VnSubnetsType([IpamSubnetType(
                                subnet=SubnetType(cidr, mask))]))
        uuid = self.vnc.virtual_network_create(vn_obj)
        self.vn_obj[uuid] = vn_obj
        return uuid

    def delete_network(self, vn_name):
        try:
            self.vnc.virtual_network_delete(fq_name=self.project_fqname+[vn_name])
        except NoIdError as e:
            print e

class ScaleTest(object):
    def __init__ (self, args):
        self.obj = VNC(args.username,
                       args.password,
                       args.tenant,
                       args.api_server_ip,
                       args.api_server_port,
                       args.keystone_ip)
        self._args = args

    def create(self):
        create_cmds = list()
        delete_cmds = list()
        for vn_index in range(self._args.n_vns):
            vn_name = 'scale-test-VN-%s'%vn_index
            vn_id = self.obj.create_network(vn_name=vn_name)
        import pdb;pdb.set_trace()
        with open(self._args.filename+'-create', 'w') as create_fp:
            create_fp.write('\n'.join(create_cmds))
        with open(self._args.filename+'-delete', 'w') as delete_fp:
            delete_fp.write('\n'.join(delete_cmds))

    def cleanup(self):
        for vn_index in range(self._args.n_vns):
            vn_name = 'scale-test-VN-%s'%vn_index
            self.obj.delete_network(vn_name)

def parse_cli(args):
    '''Define and Parse arguments for the script'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--api_server_ip',
                        action='store',
                        default='127.0.0.1',
                        help='API Server IP [127.0.0.1]')
    parser.add_argument('--api_server_port',
                        action='store',
                        default='8082',
                        help='API Server Port [8082]')
    parser.add_argument('--keystone_ip',
                        action='store',
                        default='127.0.0.1',
                        help='Keystone IP [127.0.0.1]')
    parser.add_argument('--username',
                        action='store',
                        default='admin',
                        help='Admin user name [admin]')
    parser.add_argument('--password',
                        action='store',
                        default='contrail123',
                        help="Admin user's password [contrail123]")
    parser.add_argument('--filename',
                        action='store',
                        default='./scale_fake_vms',
                        help="Filename to write the shell commands to execute on vrouter node")
    parser.add_argument('--tenant',
                        action='store',
                        default='admin',
                        help='Admin Tenant name [admin]')
    parser.add_argument('--n_vns',
                        action='store',
                        default='0', type=int,
                        help='No of Vns to create per tenant [0]')
    parser.add_argument('--cleanup',
                        action='store_true',
                        help='Cleanup the created objects [False]')
    pargs = parser.parse_args(args)
    return pargs

def get_random_cidr(mask=16):
    ''' Generate random non-overlapping cidr '''
    global alloc_addr_list
    address = socket.inet_ntop(socket.AF_INET,
                               struct.pack('>I',
                               random.randint(2**24, 2**32 - 2**29 - 1)))
    address = str(IPNetwork(address+'/'+str(mask)).network)
    if address.startswith('169.254') or address.startswith('127') or address in alloc_addr_list:
        cidr = get_random_cidr()
    else:
        alloc_addr_list.append(address)
        cidr = address+'/'+str(mask)
    return cidr

def main():
    pargs = parse_cli(sys.argv[1:])
    obj = ScaleTest(pargs)
    if pargs.cleanup:
        obj.cleanup()
    else:
        obj.create()
if __name__ == '__main__':
    main()
