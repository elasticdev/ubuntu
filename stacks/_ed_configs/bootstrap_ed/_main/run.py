def run(stackargs):

    stackargs["add_cluster"] = False
    stackargs["add_instance"] = False

    # instantiate stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname")
    stack.parse.add_required(key="key")

    # Initialize Variables in stack
    stack.init_variables()

    # Add host to the ed engine
    cmd = "host add"
    order_type = "add-host::api"
    role = "host/add"

    default_values = {"tags":None}
    default_values["hostname"] = stack.hostname

    human_description = "Adding/Recording host = {}".format(stack.hostname)
    long_description = "Adds host = {} to Jiffy".format(stack.hostname)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             long_description=long_description,
                             display=None,
                             default_values=default_values)

    # Bootstrap host to the ed engine
    cmd = "host bootstrap"
    order_type = "bootstrap-host::api"
    role = "host/bootstrap"

    default_values = {"ip_key":"private_ip", "user":"ubuntu"}
    default_values["hostname"] = stack.hostname
    default_values["keyname"] = stack.key
    human_description = "Bootstrapping host = {}".format(stack.hostname)
    long_description = "Bootstraps host = {} to Jiffy".format(stack.hostname)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             long_description=long_description,
                             display=None,
                             default_values=default_values)

    return stack.get_results()
