import re


def write_config(section, option, data, config_obj, config_file):
    """ Write/Update the configuration file

    Write or update the configuration file according to the section or
    option provided.

    Args:
        section (str): Name of the section
        option (str): Name of the option
        data (str): data related to the option to store
        config_obj (str): instance of the configuration object)
        config_file (str): instance of the configuration file where to save
                            the data

    Returns:
        None

    Todo:
        Need to cast the object to string before saving the data.
    """
    if config_obj.has_section(section):
        config_obj.set(section, option, str(data))
    else:
        config_obj.add_section(section)
        config_obj.set(section, option, str(data))

    config_obj.write(config_file)


def read_config(section, option, config_obj):
    """ Look for a given option in a config file.

    If exists, return the value in a config file according to the section
    and option.

    Args:
        section (str):  section related to the option looked for.
        option (str):   option related to the value looked for.
        config_obj (obj):   configparser object.

    Returns:
        value given for a specific tuple section/option.

    Todo:
        - Be able to cast the data into the right type.
    """
    if config_obj.has_option(section, option):
        return config_obj.get(section, option)
    else:
        raise StandardError(
                "Impossible to find %s.%s in the configuration file"
                % (section, option))


def conf_param_extract(parameter):
    data = re.split('\.', parameter)
    section = data[0]
    option = data[1]
    return section, option
