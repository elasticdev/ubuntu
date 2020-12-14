**Description**

  - This stack wrappers around Ec2 creation of Ubuntu instance
  - Optionally, we can also bootstrap the Ubuntu instance to ElasticDev

**Required**

| argument      | description                            | var type | default      |
| ------------- | -------------------------------------- | -------- | ------------ |
| hostname   | name of the host                 | string   | None         |
| keyname      | the keyname required to ssh into instance      | string   | None         |
| aws_default_region      | the AWS/EC2 default regioin      | string   | us-east-1         |

**Optional**

| argument           | description                            | var type |  default      |
| ------------- | -------------------------------------- | -------- | ------------ |
| config_network | config network is either public or private       | string   | master       |
| register_to_ed        | register the instance to ElasticDev           | boolean    | True       |

**Sample entry:**

```
infrastructure:
   ec2_instance:
       stack_name: elasticdev:::ec2_ubuntu
       arguments:
          hostname: test-instance
          size: t3.micro
          keyname: mongodb_ssh
          security_groups: web,bastion
          subnet: public
          disksize: 25
          ip_key: public_ip
          volume_size: 100
          volume_mount: /var/lib/mongodb
          volume_fstype: xfs
          mongodb_username: admin123
          mongodb_password: admin123
       credentials:
           - reference: aws_2
             orchestration: true
```
yoyo
