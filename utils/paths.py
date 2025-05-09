##################################################################################################
#                                          PATHS MODULE                                          #
#                                                                                                #
# Provides utility functions shared across the NeuroGoalkeeper project.                          #
# Currently includes helpers for locating project-relative resource files.                       #
#                                                                                                #
# Key Features:                                                                                  #
# - Stable resolution of file paths relative to project root                                     #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os

##################################################################################################
#                                   RESOURCE PATH RESOLVER                                       #
#                                                                                                #
# Returns the absolute path to a resource file relative to the project root.                     #
# This allows safe and consistent access to resources regardless of where the script is run.     #
#                                                                                                #
# :param relative_path: str → relative path like "datasets/data.csv"                             #
# :return: str → absolute path to be used in file operations                                     #
##################################################################################################

def resource_path(relative_path):
    base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)
