# Scaling

### Docker cmd for scale
```sh
docker run --name scale_test --entrypoint /bin/bash --env-file /root/my_scaling/tools/env_file -v /root/contrail_test_input.yaml:/contrail-test/contrail_test_input.yaml -v /root/my_scaling:/root/my_scaling -v /etc/contrail:/etc/contrail -v /root/.ssh:/root/.ssh --network=host -it bng-artifactory.juniper.net/contrail-nightly/contrail-test-test:2011.102
```

### Subinterface Scaling
* Main file: scale_v3.py
* Cmd: python scale_v3.py --api_server_ip '192.168.7.29' --keystone_ip '192.168.7.13' --admin_username 'admin' --admin_password 'password' --admin_project 'admin' --n_vns 1 --n_ports 1  --vnc --cleanup --n_process 1