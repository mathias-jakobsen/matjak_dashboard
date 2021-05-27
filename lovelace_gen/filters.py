#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

import json


#-----------------------------------------------------------#
#       Jinja Filters
#-----------------------------------------------------------#

def fromjson(value):
    return json.loads(value)


#-----------------------------------------------------------#
#       Constants
#-----------------------------------------------------------#

JINJA_FILTERS = {
    "fromjson": fromjson
}