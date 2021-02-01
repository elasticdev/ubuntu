def run(stackargs):

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname")

    # Add host group
    stack.add_hostgroups("elasticdev:::ubuntu::18.04-docker","install_docker")

    # Initialize 
    stack.init_variables()
    stack.init_hostgroups()

    # install docker
    inputargs = {"display":True}
    inputargs["human_description"] = "Install Docker on hostname {}".format(stack.hostname)
    inputargs["automation_phase"] = "infrastructure"
    inputargs["hostname"] = stack.hostname
    inputargs["groups"] = stack.install_docker
    stack.add_groups_to_host(**inputargs)

    return stack.get_results()
