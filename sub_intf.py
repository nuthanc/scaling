import sys
import ipaddr
from vnc_api.vnc_api import *
from netaddr import IPNetwork
import socket
import struct
import random
from netaddr import *

alloc_addr_list = list()

parent_vmi_1_uuid = 'ba726734-ee9b-42b8-9169-a89aa81b2b51'
parent_vmi_2_uuid = '05d10116-1a7e-42b6-9237-04f970bb4205'
#shc_uuid = 'f581f508-e6a3-4134-b526-0cca0b6801f8'
ipam_fq_name = ['default-domain', 'default-project', 'default-network-ipam']
tenant_name = ['default-domain', 'admin']

client = VncApi(username='admin', password='c0ntrail123', tenant_name='admin',
                api_server_host='10.204.216.2', api_server_port=8082, auth_host='10.204.216.2')

cidr = "80.0.1.0/24"


def get_randmon_cidr(mask=16):
    ''' Generate random non-overlapping cidr '''
    global alloc_addr_list
    address = socket.inet_ntop(socket.AF_INET,
                               struct.pack('>I',
                                           random.randint(2**24, 2**32 - 2**29 - 1)))
    address = str(IPNetwork(address+'/'+str(mask)).network)
    if address.startswith('169.254') or address in alloc_addr_list:
        cidr = get_randmon_cidr()
    else:
        alloc_addr_list.append(address)
        cidr = address+'/'+str(mask)
    return cidr


class CIDR:

    def __init__(self, cidr):
        self.index = 0
        self.cidr = cidr
        self.ip_network = IPNetwork(self.cidr)
        self.ip_addr = ipaddr.IPAddress(IPNetwork(self.cidr)[0])
        self.cidr_net, self.cidr_mask = cidr.split("/")

    def get_next_cidr(self):
        ip_network_next = self.ip_network.next()[0]
        ip_addr_next = ipaddr.IPAddress(ip_network_next)
        cidr = ip_addr_next._explode_shorthand_ip_string()
        cidr = cidr + "/" + self.cidr_mask
        self.ip_network = IPNetwork(cidr)
        return cidr


cidr_obj = CIDR(cidr)

proj_obj = client.project_read(fq_name=tenant_name)
ipam_obj = client.network_ipam_read(fq_name=ipam_fq_name)


def create_vn(vlan):
    vn_name = "VN.hc.st" + str(vlan)
    #cidr = get_randmon_cidr(mask=28).split('/')[0]
    ipv4_cidr = cidr_obj.get_next_cidr()
    ipv4_network, ipv4_prefix = ipv4_cidr.split("/")
    ipam_sn_lst = []
    ipam_sn = IpamSubnetType(subnet=SubnetType(
        ipv4_network, int(ipv4_prefix)), addr_from_start=True)
    ipam_sn.set_subnet_name(vn_name+"_ipv4_subnet")
    ipam_sn_lst.append(ipam_sn)
    vn_obj = VirtualNetwork(vn_name, parent_obj=proj_obj)
    vn_obj.add_network_ipam(ipam_obj, VnSubnetsType(ipam_sn_lst))
    net_id = client.virtual_network_create(vn_obj)
    return vn_obj


#hc_obj = client.service_health_check_read(id=shc_uuid)
for vlan in range(850, 1275):
    vn = create_vn(vlan)
    p_vmi_1 = client.virtual_machine_interface_read(id=parent_vmi_1_uuid)
    p_vmi_2 = client.virtual_machine_interface_read(id=parent_vmi_2_uuid)
    for p_vmi in [p_vmi_1, p_vmi_2]:
        if p_vmi == p_vmi_1:
            vmi_fq_name = ['default-domain', 'admin',
                           'test-bfd-hc-vmi.st%d' % vlan]
        else:
            vmi_fq_name = ['default-domain', 'admin',
                           'test-bfd-2-hc-vmi.st%d' % vlan]
        vmi_obj = VirtualMachineInterface(
            fq_name=vmi_fq_name, parent_type='project')
        vmi_prop = VirtualMachineInterfacePropertiesType()
        vmi_prop.set_sub_interface_vlan_tag(vlan)
        vmi_obj.set_virtual_machine_interface_properties(vmi_prop)
        vmi_obj.add_virtual_machine_interface(p_vmi)
        vmi_obj.add_virtual_network(vn)
#        vmi_obj.add_service_health_check(hc_obj)
        vmi_obj.set_virtual_machine_interface_mac_addresses(
            p_vmi.virtual_machine_interface_mac_addresses)
        client.virtual_machine_interface_create(vmi_obj)
        iip_obj = InstanceIp(name=p_vmi.name+'-iip-%s' % vlan)
        iip_obj.add_virtual_machine_interface(vmi_obj)
        iip_obj.add_virtual_network(vn)
        client.instance_ip_create(iip_obj)
