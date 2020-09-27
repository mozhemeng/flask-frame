from appname.controllers.v1 import bp_list as v1_bp_list


controller_mapping = {
    'v1': v1_bp_list
}


__all__ = controller_mapping
