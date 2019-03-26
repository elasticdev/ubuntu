def run(stackargs):

    # Do not add cluster and instance
    stackargs["add_cluster"] = False
    stackargs["add_instance"] = False

    # instantiate stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname")
    stack.parse.add_required(key="key")
    stack.parse.add_required(key="region",default="us-east-1")
    stack.parse.add_required(key="image",default="null")
    stack.parse.add_required(key="image_name",default="null")
    stack.parse.add_required(key="image_ref",default="github_13456777:::public::ubuntu.16.04-chef_solo")

    # Add substacks
    stack.add_substack('elasticdev:::ubuntu::bootstrap_ed')
    stack.add_substack('elasticdev:::aws::ec2_server')

    # init the stack namespace
    stack.init_variables()
    stack.init_substacks()

    # Call to create the server
    default_values = {}
    default_values["hostname"] = stack.hostname
    default_values["key"] = stack.key
    default_values["region"] = stack.region

    default_values["size"] = "t2.micro"
    default_values["disksize"] = 40
    default_values["timeout"] = 600
    default_values["timeout"] = 600
    default_values["security_group"] = "default"
    default_values["placement"] = None
    default_values["vpc"] = None
    default_values["vpc_label"] = 'vpc'
    default_values["sg"] = None
    default_values["sg_label"] = None
    default_values["tags"] = None
    default_values["comment"] = None
    default_values["image_ref"] = stackargs.image_ref
    if stackargs.image: default_values["image"] = stackargs.image
    if stackargs.image_name: default_values["image_name"] = stackargs.image_name

    inputargs = {"default_values":default_values}
    inputargs["automation_phase"] = "infrastructure"
    inputargs["human_description"] = "Instruction: Creates a Server on Ec2"
    stack.ec2_server.insert(display=None,**inputargs)

    # Call to bootstrap_ed to ed
    default_values = {}
    default_values["hostname"] = stack.hostname
    default_values["key"] = stack.key
    default_values["ip_key"] = "private_ip"
    default_values["user"] = "ubuntu"
    default_values["tags"] = None

    inputargs = {"default_values":default_values}
    inputargs["automation_phase"] = "infrastructure"
    inputargs["human_description"] = "Bootstraps host to Jiffy database"
    stack.bootstrap_ed.insert(display=None,**inputargs)

    return stack.get_results()

