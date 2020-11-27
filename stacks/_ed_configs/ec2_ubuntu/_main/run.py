def run(stackargs):

    # Testingyoyo

    # Do not add cluster and instance
    stackargs["add_cluster"] = False
    stackargs["add_instance"] = False

    # instantiate stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname")
    stack.parse.add_required(key="keyname")
    stack.parse.add_required(key="aws_default_region",default="us-east-1")

    # vpc info
    stack.parse.add_optional(key="vpc_name",default="null")
    stack.parse.add_optional(key="vpc_id",default="null")

    # security groups
    stack.parse.add_optional(key="security_groups",default="null")
    stack.parse.add_optional(key="security_groups_ids",default="null")

    # subnet_id
    stack.parse.add_optional(key="subnet",default="null")
    stack.parse.add_optional(key="subnet_id",default="null")

    # image info
    stack.parse.add_optional(key="image",default="null")
    stack.parse.add_optional(key="image_name",default="null")
    stack.parse.add_optional(key="image_ref",default="null")

    # tags and labels
    stack.parse.add_optional(key="tags",default="null")
    stack.parse.add_optional(key="labels",default="null")

    # Add substacks
    stack.add_substack('elasticdev:::ubuntu::bootstrap_ed')

    # Revisit and replace with ec2_server later
    #stack.add_substack('elasticdev:::aws::ec2_server_builtin',"ec2_server")
    stack.add_substack('elasticdev:::aws::ec2_server',"ec2_server")

    # init the stack namespace
    stack.init_variables()
    stack.init_substacks()

    # Call to create the server
    default_values = {"hostname":stack.hostname}
    default_values["key"] = stack.keyname
    default_values["size"] = "t2.micro"
    default_values["disksize"] = 40
    default_values["timeout"] = 600
    default_values["tags"] = None
    default_values["aws_default_region"] = stack.aws_default_region

    # vpc
    if stack.vpc_name: default_values["vpc_name"] = stack.vpc_name
    if stack.vpc_id: default_values["vpc_id"] = stack.vpc_id

    # subnet
    if stack.subnet: default_values["subnet"] = stack.subnet
    if stack.subnet_id: default_values["subnet_id"] = stack.subnet_id

    # security groups
    if stack.security_groups: default_values["security_groups"] = stack.security_groups
    if stack.security_groups_ids: default_values["security_groups_ids"] = stack.security_groups_ids

    # ami image
    if stack.image: default_values["image"] = stack.image
    if stack.image_name: default_values["image_name"] = stack.image_name
    if stack.image_ref: default_values["image_ref"] = stack.image_ref

    # tags and labels
    if stack.tags: default_values["tags"] = stack.tags
    if stack.labels: default_values["labels"] = stack.labels

    inputargs = {"default_values":default_values}
    inputargs["automation_phase"] = "infrastructure"
    inputargs["human_description"] = "Instruction: Creates a Server on Ec2"
    stack.ec2_server.insert(display=None,**inputargs)

    # Call to bootstrap_ed to ed
    default_values = {"hostname":stack.hostname}
    default_values["keyname"] = stack.keyname
    default_values["ip_key"] = "private_ip"
    default_values["user"] = "ubuntu"
    if stack.tags: default_values["tags"] = stack.tags
    if stack.labels: default_values["labels"] = stack.labels

    inputargs = {"default_values":default_values}
    inputargs["automation_phase"] = "infrastructure"
    inputargs["human_description"] = "Bootstraps host to Jiffy database"
    stack.bootstrap_ed.insert(display=None,**inputargs)

    return stack.get_results()
