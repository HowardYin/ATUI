import ConfigParser
import logging
import os
import sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

local_path = os.path.abspath(os.path.dirname(__file__))

local_conf_path = os.path.join(os.path.dirname(local_path), 'local.conf')

if not os.path.exists(local_conf_path):
    raise Exception('no local.conf found , ATUI/local.conf is need !')
else:
    logging.debug('using %s as local conf' % local_conf_path)

cf = ConfigParser.ConfigParser()
# read config
cf.read(local_conf_path)
# return all section
# erp_url = cf.get("urls", "erp_url")
os.environ.update(dict(cf.items("urls")))
os.environ.update(dict(cf.items("drivers")))

# logging.debug(pformat(os.environ.get('erp_url')))

loc_atui = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if loc_atui not in sys.path:
    sys.path.append(loc_atui)

loc_drivers = os.environ.get('driver_folder')
if not os.path.isdir(loc_drivers):
    raise Exception('driver_folder %s invalid' % loc_drivers)
else:
    logging.debug('driver_folder %s is valid' % loc_drivers)
    # sys.path.append(loc_drivers)
