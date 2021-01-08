# Sub-interfaceScaling

### Sub-interface
* 1 Phy port -> Multiple logic units
* eth0 -> eth0.1, eth0.2
* 10G port -> 1G 10 sub-interfaces
* VLAN Id -> for identifying

### Important
* Use only one process with ForkedPdb

### Docker cmd and script cmd
```sh
docker run --name nuthan_test --entrypoint /bin/bash -v /root/nuthanc-scaling:/root/nuthanc-scaling --network=host -it bng-artifactory.juniper.net/contrail-nightly/contrail-test-test:2011.127

python scale_v3.py --api_server_ip '10.204.216.103' --keystone_ip '10.204.216.140' --n_vns 1 --n_ports 1  --vnc --cleanup --n_process 1
```
python scale_v3.py --api_server_ip '10.204.216.103' --keystone_ip '10.204.216.140' --n_vns 1 --n_subintfs 4094 --vnc --cleanup --n_process 1

python scale_v3.py --api_server_ip '10.204.216.103' --keystone_ip '10.204.216.140' --n_vns 1 --n_subintfs 4094 --vnc --cleanup --n_process 1 --project admin

For m16:

python scale_v3.py --api_server_ip '10.204.216.105' --keystone_ip '10.204.216.159' --n_vns 1 --n_subintfs 4094 --vnc --cleanup --n_process 1 --project admin

### VNC API links
* https://juniper.github.io/contrail-vnc/api-doc/html/library_details.html
* VNC API Library tutorial: https://juniper.github.io/contrail-vnc/api-doc/html/tutorial_with_library.html

### sub-interface scaling
* Two sub interfaces under same primary port can't have same Vlan tag
* VLAN has to be between 1 to 4094
* 4094 is the actual limit per port
* I think **251** is the limit(From scale.log)
  * 1 is Port's ip(252)
  * 1 is Service Address ip(253)
  * 1 is Gateway's ip(254)
  * 1 is Broadcast ip(255)
  * This is in /24 network

### Insights from Aswani
* Scale per VN and per cluster
* Need to increase timeout in parse_cli(to 1,80,000 more or less) 
* Increase the subnet mask in create_VN(If mask size is 16, then no of subinterfaces to 2^16 - 3)
* Give project as admin(--project admin) so that the processes create objects in the mentioned project

### Scale numbers from Aswani
```txt
Virtual Network(30 processes)

300 vns = 15 sec
3k  vns = 16 mins
21k vns = 9.5hrs
Every vn taking 19 sec after 21k
After 10k vns every 1k added extra 3 min latency

Ports(50 processes)

1000 ports = 16 sec
10k  ports = 13 min
20k  ports = 16 min
Total created 250k ports = ~5hrs

floating_ips(50 processes)

1500 fips = 140sec
15k  fips = 23min
36k  fips = 80 min
Total created 52k fips = ~100min

security group (50 processes)

1500 porrs = 23 sec
15k  ports = 310sec
38k  ports = 18 min

security group_rules rules(100 processes)

3000 rules = 90 sec
10 k rules = 6.5 min
100k rules = 31 min
200k rules = 65 min

policy(50 processes)

1000 policies = 19sec
5k   policies = 4min
25k  policies = 23min
50k  policies = 49min

policy rules(50 processes)

3k  policy_rules = 4sec
30k policy_rules = 59sec
100K policy_rules per_tenant = 5min
```

```sh
[root@nodem14 nuthanc-scaling] python scale_v3.py --api_server_ip '10.204.216.103' --keystone_ip '10.204.216.140' --n_vns 1 --n_subintfs 252 --vnc --cleanup --n_process 1
Process Process-1:1:
Traceback (most recent call last):
  File "/usr/lib64/python2.7/multiprocessing/process.py", line 258, in _bootstrap
    self.run()
  File "/usr/lib64/python2.7/multiprocessing/process.py", line 114, in run
    self._target(*self._args, **self._kwargs)
  File "scale_v3.py", line 403, in start_create
    self.obj.create_port(vn_name, sub_intf_name, parent_vmi=parent_vmi, vlan=vlan)
  File "scale_v3.py", line 861, in create_port
    self.vnc.instance_ip_create(iip_obj)
  File "/usr/lib/python2.7/site-packages/vnc_api/vnc_api.py", line 58, in wrapper
    return func(self, *args, **kwargs)
  File "/usr/lib/python2.7/site-packages/vnc_api/vnc_api.py", line 652, in _object_create
    OP_POST, obj_cls.create_uri, data=json_body)
  File "/usr/lib/python2.7/site-packages/vnc_api/vnc_api.py", line 1094, in _request_server
    retry_after_authn=retry_after_authn, retry_count=retry_count)
  File "/usr/lib/python2.7/site-packages/vnc_api/vnc_api.py", line 1170, in _request
    raise BadRequest(status, content)
BadRequest: Virtual-Network(['default-domain', 'NutScaleaF8c', 'NutScaleaF8c-VN0f0cb']) has exhausted subnet([])
> /root/nuthanc-scaling/scale_v3.py(1159)main()
-> obj.cleanup()
```

### ENV in kolla toolbox
```sh
OS_PROJECT_DOMAIN_ID=default
OS_PROJECT_ID=bcbea1bc6efe49f1bf2c76239c6b1d51
OS_REGION_NAME=RegionOne
OS_USER_DOMAIN_NAME=Default
OS_PROJECT_NAME=admin
OS_IDENTITY_API_VERSION=3
OS_PASSWORD=c0ntrail123
OS_AUTH_URL=http://10.204.216.140:5000
OS_USERNAME=admin
OS_INTERFACE=public
```

### Code in tf-test
* https://github.com/nuthanc/tf-test/blob/d1ce5dbc8b37cd9405c7ee1f1139a82547dd5495/common/intf_mirroring/verify.py#L251
* https://github.com/nuthanc/tf-test/blob/d1ce5dbc8b37cd9405c7ee1f1139a82547dd5495/fixtures/port_fixture.py#L115

### Flow
* create -> start_create 

### Sub-interface Parameters given in UI
* Network
* Name 
* VLAN: This is required

### Sub-interface info from pdb
* I had set vlan tag to 123 and name to sub1
* Sub-interface to port
```python
(Pdb) pprint.pprint(vars(self.vnc.virtual_machine_interface_read(fq_name=[u'default-domain', u'ProjectcFf5', u'sub1'])))
{'_display_name': u'sub1',
 '_ecmp_hashing_include_fields': hashing_configured = False, source_ip = True, destination_ip = True, ip_protocol = True, source_port = True, destination_port = True,
 '_id_perms': permissions = owner = admin, owner_access = 7, group = reader, group_access = 7, other_access = 7, uuid = uuid_mslong = 11294628849236263867, uuid_lslong = 11217915269180553128, enable = True, created = 2020-12-28T07:50:33.852823, last_modified = 2020-12-28T07:50:33.876075, description = None, user_visible = True, creator = None,
 '_igmp_enable': False,
 '_pending_field_list_updates': {},
 '_pending_field_map_updates': {},
 '_pending_field_updates': set(),
 '_pending_ref_updates': set(),
 '_perms2': owner = 9d313b43eb1d4aec85ff670f5b71f790, owner_access = 7, global_access = 0, share = [],
 '_port_security_enabled': True,
 '_server_conn': <vnc_api.vnc_api.VncApi object at 0x7f64150b48d0>,
 '_type': 'virtual-machine-interface',
 '_uuid': u'9cbe9518-cc9b-43bb-9bae-0a8093eff7a8',
 '_virtual_machine_interface_allowed_address_pairs': allowed_address_pair = [],
 '_virtual_machine_interface_bindings': key_value_pair = [key = vnic_type, value = normal],
 '_virtual_machine_interface_device_owner': u'',
 '_virtual_machine_interface_dhcp_option_list': dhcp_option = [],
 '_virtual_machine_interface_disable_policy': False,
 '_virtual_machine_interface_mac_addresses': mac_address = [u'02:9c:be:95:18:cc'],
 '_virtual_machine_interface_properties': service_interface_type = None, interface_mirror = None, local_preference = None, sub_interface_vlan_tag = 123, max_flows = 0,
 '_vlan_tag_based_bridge_domain': False,
 'fq_name': [u'default-domain', u'ProjectcFf5', u'sub1'],
 'name': u'sub1',
 'parent_type': u'project',
 'parent_uuid': u'9d313b43-eb1d-4aec-85ff-670f5b71f790',
 'routing_instance_refs': [{u'attr': direction = both, vlan_tag = None, src_mac = None, dst_mac = None, mpls_label = None, service_chain_address = None, ipv6_service_chain_address = None, protocol = None,
                            u'href': u'http://10.204.216.103:8082/routing-instance/4159986d-ba8e-40a7-9b3f-c5906384895e',
                            u'to': [u'default-domain',
                                    u'ProjectcFf5',
                                    u'ProjectcFf5-VN0424d',
                                    u'ProjectcFf5-VN0424d'],
                            u'uuid': u'4159986d-ba8e-40a7-9b3f-c5906384895e'}],
 'virtual_machine_interface_refs': [{u'attr': None,
                                     u'href': u'http://10.204.216.103:8082/virtual-machine-interface/cbb65082-5710-4e36-8d3f-49c6aa8fc387',
                                     u'to': [u'default-domain',
                                             u'ProjectcFf5',
                                             u'ProjectcFf5-VN0424d-Port0'],
                                     u'uuid': u'cbb65082-5710-4e36-8d3f-49c6aa8fc387'}],
 'virtual_network_refs': [{u'attr': None,
                           u'href': u'http://10.204.216.103:8082/virtual-network/e1b3e27d-9fd1-4d2e-8848-8cad3a4051b6',
                           u'to': [u'default-domain',
                                   u'ProjectcFf5',
                                   u'ProjectcFf5-VN0424d'],
                           u'uuid': u'e1b3e27d-9fd1-4d2e-8848-8cad3a4051b6'}]}
```
* dir of port object
```python
(Pdb) dir(port_obj)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__long__', '__module__', '__native__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_igmp_enable', '_original_virtual_network_refs', '_pending_field_list_updates', '_pending_field_map_updates', '_pending_field_updates', '_pending_ref_updates', '_port_security_enabled', '_serialize_field_to_json', '_server_conn', '_type', '_uuid', '_virtual_machine_interface_disable_policy', '_vlan_tag_based_bridge_domain', 'add_annotations', 'add_bgp_router', 'add_bridge_domain', 'add_interface_route_table', 'add_physical_interface', 'add_port_profile', 'add_port_tuple', 'add_qos_config', 'add_routing_instance', 'add_security_group', 'add_security_logging_object', 'add_service_endpoint', 'add_service_health_check', 'add_tag', 'add_virtual_machine', 'add_virtual_machine_interface', 'add_virtual_machine_interface_bindings', 'add_virtual_machine_interface_fat_flow_protocols', 'add_virtual_network', 'annotations', 'backref_field_types', 'backref_fields', 'children_field_metas', 'children_field_types', 'children_fields', 'clear_pending_updates', 'create_uri', 'del_annotations', 'del_bgp_router', 'del_bridge_domain', 'del_interface_route_table', 'del_physical_interface', 'del_port_profile', 'del_port_tuple', 'del_qos_config', 'del_routing_instance', 'del_security_group', 'del_security_logging_object', 'del_service_endpoint', 'del_service_health_check', 'del_tag', 'del_virtual_machine', 'del_virtual_machine_interface', 'del_virtual_machine_interface_bindings', 'del_virtual_machine_interface_fat_flow_protocols', 'del_virtual_network', 'display_name', 'dump', 'ecmp_hashing_include_fields', 'fq_name', 'from_dict', 'get_alias_ip_back_refs', 'get_annotations', 'get_bgp_as_a_service_back_refs', 'get_bgp_router_refs', 'get_bridge_domain_refs', 'get_customer_attachment_back_refs', 'get_display_name', 'get_ecmp_hashing_include_fields', 'get_floating_ip_back_refs', 'get_fq_name', 'get_fq_name_str', 'get_id_perms', 'get_igmp_enable', 'get_instance_ip_back_refs', 'get_interface_route_table_refs', 'get_link_aggregation_group_back_refs', 'get_loadbalancer_back_refs', 'get_loadbalancer_pool_back_refs', 'get_logical_interface_back_refs', 'get_logical_router_back_refs', 'get_parent_fq_name', 'get_parent_fq_name_str', 'get_pending_updates', 'get_perms2', 'get_physical_interface_refs', 'get_port_profile_refs', 'get_port_security_enabled', 'get_port_tuple_refs', 'get_qos_config_refs', 'get_ref_updates', 'get_routing_instance_refs', 'get_security_group_refs', 'get_security_logging_object_refs', 'get_service_endpoint_refs', 'get_service_health_check_refs', 'get_subnet_back_refs', 'get_tag_refs', 'get_type', 'get_uuid', 'get_virtual_ip_back_refs', 'get_virtual_machine_interface_allowed_address_pairs', 'get_virtual_machine_interface_back_refs', 'get_virtual_machine_interface_bindings', 'get_virtual_machine_interface_device_owner', 'get_virtual_machine_interface_dhcp_option_list', 'get_virtual_machine_interface_disable_policy', 'get_virtual_machine_interface_fat_flow_protocols', 'get_virtual_machine_interface_host_routes', 'get_virtual_machine_interface_mac_addresses', 'get_virtual_machine_interface_properties', 'get_virtual_machine_interface_refs', 'get_virtual_machine_refs', 'get_virtual_network_refs', 'get_virtual_port_group_back_refs', 'get_vlan_tag_based_bridge_domain', 'get_vrf_assign_table', 'id_perms', 'igmp_enable', 'name', 'next', 'object_type', 'parent_name', 'parent_type', 'parent_types', 'parent_uuid', 'perms2', 'port_security_enabled', 'prop_field_metas', 'prop_field_types', 'prop_fields', 'prop_list_field_has_wrappers', 'prop_list_fields', 'prop_map_field_has_wrappers', 'prop_map_field_key_names', 'prop_map_fields', 'ref_field_metas', 'ref_field_types', 'ref_fields', 'resource_type', 'resource_uri_base', 'serialize_to_json', 'set_annotations', 'set_bgp_router', 'set_bgp_router_list', 'set_bridge_domain', 'set_bridge_domain_list', 'set_display_name', 'set_ecmp_hashing_include_fields', 'set_id_perms', 'set_igmp_enable', 'set_interface_route_table', 'set_interface_route_table_list', 'set_perms2', 'set_physical_interface', 'set_physical_interface_list', 'set_port_profile', 'set_port_profile_list', 'set_port_security_enabled', 'set_port_tuple', 'set_port_tuple_list', 'set_qos_config', 'set_qos_config_list', 'set_routing_instance', 'set_routing_instance_list', 'set_security_group', 'set_security_group_list', 'set_security_logging_object', 'set_security_logging_object_list', 'set_server_conn', 'set_service_endpoint', 'set_service_endpoint_list', 'set_service_health_check', 'set_service_health_check_list', 'set_tag', 'set_tag_list', 'set_uuid', 'set_virtual_machine', 'set_virtual_machine_interface', 'set_virtual_machine_interface_allowed_address_pairs', 'set_virtual_machine_interface_bindings', 'set_virtual_machine_interface_device_owner', 'set_virtual_machine_interface_dhcp_option_list', 'set_virtual_machine_interface_disable_policy', 'set_virtual_machine_interface_fat_flow_protocols', 'set_virtual_machine_interface_host_routes', 'set_virtual_machine_interface_list', 'set_virtual_machine_interface_mac_addresses', 'set_virtual_machine_interface_properties', 'set_virtual_machine_list', 'set_virtual_network', 'set_virtual_network_list', 'set_vlan_tag_based_bridge_domain', 'set_vrf_assign_table', 'uuid', 'virtual_machine_interface_allowed_address_pairs', 'virtual_machine_interface_bindings', 'virtual_machine_interface_device_owner', 'virtual_machine_interface_dhcp_option_list', 'virtual_machine_interface_disable_policy', 'virtual_machine_interface_fat_flow_protocols', 'virtual_machine_interface_host_routes', 'virtual_machine_interface_mac_addresses', 'virtual_machine_interface_properties', 'virtual_network_refs', 'vlan_tag_based_bridge_domain', 'vrf_assign_table']
```

### Read port configuration containing sub-interfaces
* sub-interfaces mentioned in virtual_network_refs property
```python
(Pdb) pprint.pprint(vars(self.vnc.virtual_machine_interface_read(id='cbb65082-5710-4e36-8d3f-49c6aa8fc387')))
{'_display_name': u'ProjectcFf5-VN0424d-Port0',
 '_id_perms': permissions = owner = admin, owner_access = 7, group = reader, group_access = 7, other_access = 7, uuid = uuid_mslong = 14679008556197367350, uuid_lslong = 10177934800494510983, enable = True, created = 2020-12-28T07:39:13.343144, last_modified = 2020-12-28T07:58:42.633946, description = None, user_visible = True, creator = None,
 '_igmp_enable': False,
 '_pending_field_list_updates': {},
 '_pending_field_map_updates': {},
 '_pending_field_updates': set(),
 '_pending_ref_updates': set(),
 '_perms2': owner = 9d313b43eb1d4aec85ff670f5b71f790, owner_access = 7, global_access = 0, share = [],
 '_port_security_enabled': True,
 '_server_conn': <vnc_api.vnc_api.VncApi object at 0x7fd7c15868d0>,
 '_type': 'virtual-machine-interface',
 '_uuid': u'cbb65082-5710-4e36-8d3f-49c6aa8fc387',
 '_virtual_machine_interface_disable_policy': False,
 '_virtual_machine_interface_mac_addresses': mac_address = [u'02:cb:b6:50:82:57'],
 '_vlan_tag_based_bridge_domain': False,
 'fq_name': [u'default-domain', u'ProjectcFf5', u'ProjectcFf5-VN0424d-Port0'],
 'name': u'ProjectcFf5-VN0424d-Port0',
 'parent_type': u'project',
 'parent_uuid': u'9d313b43-eb1d-4aec-85ff-670f5b71f790',
 'routing_instance_refs': [{u'attr': direction = both, vlan_tag = None, src_mac = None, dst_mac = None, mpls_label = None, service_chain_address = None, ipv6_service_chain_address = None, protocol = None,
                            u'href': u'http://10.204.216.103:8082/routing-instance/4159986d-ba8e-40a7-9b3f-c5906384895e',
                            u'to': [u'default-domain',
                                    u'ProjectcFf5',
                                    u'ProjectcFf5-VN0424d',
                                    u'ProjectcFf5-VN0424d'],
                            u'uuid': u'4159986d-ba8e-40a7-9b3f-c5906384895e'}],
 'virtual_machine_interface_refs': [{u'attr': None,
                                     u'href': u'http://10.204.216.103:8082/virtual-machine-interface/0d31597f-8e10-454d-a92e-c40627219c80',
                                     u'to': [u'default-domain',
                                             u'ProjectcFf5',
                                             u'sub2'],
                                     u'uuid': u'0d31597f-8e10-454d-a92e-c40627219c80'},
                                    {u'attr': None,
                                     u'href': u'http://10.204.216.103:8082/virtual-machine-interface/9cbe9518-cc9b-43bb-9bae-0a8093eff7a8',
                                     u'to': [u'default-domain',
                                             u'ProjectcFf5',
                                             u'sub1'],
                                     u'uuid': u'9cbe9518-cc9b-43bb-9bae-0a8093eff7a8'}],
 'virtual_network_refs': [{u'attr': None,
                           u'href': u'http://10.204.216.103:8082/virtual-network/e1b3e27d-9fd1-4d2e-8848-8cad3a4051b6',
                           u'to': [u'default-domain',
                                   u'ProjectcFf5',
                                   u'ProjectcFf5-VN0424d'],
                           u'uuid': u'e1b3e27d-9fd1-4d2e-8848-8cad3a4051b6'}]}
```
