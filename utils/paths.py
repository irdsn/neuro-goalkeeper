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
#                                        IMPLEMENTATION                                          #
##################################################################################################

def resource_path(relative_path):
    """
    Resolve the absolute path to a resource file based on the project root.

    This function ensures compatibility when running the application from different locations
    by returning a consistent and safe absolute path to internal resources.

    Args:
        relative_path (str): Relative path to the file (e.g., "datasets/data.csv").

    Returns:
        str: Absolute file path pointing to the requested resource.
    """

    base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)
