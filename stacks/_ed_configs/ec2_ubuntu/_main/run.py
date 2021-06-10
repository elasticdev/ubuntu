def _insert_volume_params(stack,values=None):

    if not values: values = {}

    # minimal to create the disk 
    # is volume_size and volume_name
    if not stack.volume_size: return values
    if not stack.volume_name: return values

    values["volume_size"] = stack.volume_size
    values["volume_name"] = stack.volume_name

    # minimal to create the disk
    # to optionally format and mount volume
    if not stack.volume_fstype: return values
    if not stack.volume_mountpoint: return values
    values["volume_fstype"] = stack.volume_fstype
    values["volume_mountpoint"] = stack.volume_mountpoint

    return values

def run(stackargs):

    import random

    # Do not add cluster and instance
    stackargs["add_cluster"] = False
    stackargs["add_instance"] = False

    # instantiate stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname")
    stack.parse.add_required(key="keyname")
    stack.parse.add_required(key="aws_default_region",default="us-east-1")

    stack.parse.add_optional(key="config_network",choices=["public","private"],default="public")

    stack.parse.add_optional(key="register_to_ed",default=True,null_allowed=True)

    # vpc info
    # hellohello
    stack.parse.add_optional(key="vpc_name",default="null")
    stack.parse.add_optional(key="vpc_id",default="null")

    # security groups
    # hellohello
    stack.parse.add_optional(key="sg_id",default="null")
    stack.parse.add_optional(key="security_group_ids",default="null")
    stack.parse.add_optional(key="security_groups",default="null")

    # subnet_id
    # hellohello
    stack.parse.add_optional(key="subnet",default="null")
    stack.parse.add_optional(key="subnet_id",default="null")
    stack.parse.add_optional(key="subnet_ids",default="null")  # expect CSV

    # image info
    stack.parse.add_optional(key="image",default="null")
    stack.parse.add_optional(key="image_name",default="null")
    stack.parse.add_optional(key="image_ref",default="null")
    stack.parse.add_optional(key="image_filter",default="null")
    stack.parse.add_optional(key="image_owner",default="null")

    stack.parse.add_optional(key="size",default="t3.micro")
    stack.parse.add_optional(key="disksize",default="20")
    stack.parse.add_optional(key="ip_key",default="public_ip")

    # extra disk
    stack.parse.add_optional(key="volume_name",default="null")
    stack.parse.add_optional(key="volume_size",default="null")
    stack.parse.add_optional(key="volume_mountpoint",default="null")
    stack.parse.add_optional(key="volume_fstype",default="null")

    # tags and labels
    stack.parse.add_optional(key="tags",default="null")
    stack.parse.add_optional(key="labels",default="null")

    # Add substacks
    stack.add_substack('elasticdev:::bootstrap_ed')
    stack.add_substack('elasticdev:::ec2_server')

    # init the stack namespace
    stack.init_variables()
    stack.init_substacks()

    ##################################################
    # determine specific variables
    ##################################################

    # subnet
    if not stack.subnet_id and stack.subnet_ids: 
        _subnet_ids = stack.subnet_ids.strip().split(",")
        _subnet_id = random.choice(_subnet_ids)
        stack.set_variable("subnet_id",_subnet_id)

    # security groups
    if not stack.security_group_ids and stack.sg_id: 
        stack.set_variable("security_group_ids",[ stack.sg_id ])

    ##################################################
    # Main
    ##################################################

    # Call to create the server
    default_values = {"hostname":stack.hostname}
    default_values["key"] = stack.keyname
    default_values["size"] = stack.size
    default_values["disksize"] = stack.disksize
    default_values["timeout"] = 600
    default_values["aws_default_region"] = stack.aws_default_region
    default_values["config_network"] = stack.config_network
    if stack.tags: default_values["tags"] = stack.tags

    # vpc
    if stack.vpc_id: 
        default_values["vpc_id"] = stack.vpc_id
    elif stack.vpc_name: 
        default_values["vpc_name"] = stack.vpc_name

    # subnet
    if stack.subnet_id: 
        default_values["subnet_id"] = stack.subnet_id
    elif stack.subnet: 
        default_values["subnet"] = stack.subnet

    # security groups
    if stack.security_group_ids: 
        default_values["security_group_ids"] = stack.security_group_ids
    elif stack.security_groups: 
        default_values["security_groups"] = stack.security_groups

    # ami image
    if stack.image: default_values["image"] = stack.image
    if stack.image_name: default_values["image_name"] = stack.image_name
    if stack.image_ref: default_values["image_ref"] = stack.image_ref
    if stack.image_filter: default_values["image_filter"] = stack.image_filter
    if stack.image_owner: default_values["image_owner"] = stack.image_owner

    # tags and labels
    if stack.tags: default_values["tags"] = stack.tags
    if stack.labels: default_values["labels"] = stack.labels

    # see if extra disk is required
    _insert_volume_params(stack,default_values)

    # hellohello
    stack.logger.debug(default_values)

    inputargs = {"default_values":default_values}
    inputargs["automation_phase"] = "infrastructure"
    inputargs["human_description"] = "Instruction: Creates a Server on Ec2"
    stack.ec2_server.insert(display=None,**inputargs)

    if stack.register_to_ed:

        # Call to bootstrap_ed to ed
        default_values = {"hostname":stack.hostname}
        default_values["keyname"] = stack.keyname
        default_values["ip_key"] = stack.ip_key
        default_values["user"] = "ubuntu"
        if stack.tags: default_values["tags"] = stack.tags
        if stack.labels: default_values["labels"] = stack.labels

        inputargs = {"default_values":default_values}
        inputargs["automation_phase"] = "infrastructure"
        inputargs["human_description"] = "Bootstraps host to Jiffy database"
        stack.bootstrap_ed.insert(display=None,**inputargs)

    return stack.get_results()
