# scaling

### VNC API links
* https://juniper.github.io/contrail-vnc/api-doc/html/library_details.html
* VNC API Library tutorial: https://juniper.github.io/contrail-vnc/api-doc/html/tutorial_with_library.html

### sub-interface scaling
* Docker cmd
```sh
docker run --name nuthan_test --entrypoint /bin/bash -v /root/nuthanc-scaling:/root/nuthanc-scaling --network=host -it bng-artifactory.juniper.net/contrail-nightly/contrail-test-test:2011.127
```
* cmd: python scale_v3.py --api_server_ip '10.204.216.103' --keystone_ip '10.204.216.140' --n_vns 1 --n_ports 1  --vnc --cleanup --n_process 1

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