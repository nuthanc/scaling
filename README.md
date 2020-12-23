# scaling

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