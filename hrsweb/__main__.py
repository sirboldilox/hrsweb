"""
Entry point script for the app
"""
import logging
from configparser import Error as ConfigError

from hrsweb.app import webapp
from hrsweb.config import SiteConfig

# Defaults
DEFAULT_CONFIG = './local.conf'


def main(config_file=DEFAULT_CONFIG):
    """Main entry point"""

    # Setup logging
    logger = logging.getLogger('webrecords')
    logger.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # Load the config
    try:
        config = SiteConfig.from_file(config_file)
    except ConfigError as error:
        print("Exception in config: %s" % error)
        return 

    webapp.iniconfig = config
    webapp.debug = config.getboolean('flask', 'debug', fallback=False)

    # Start the webserver
    host  = config.get('flask', 'bind', fallback='0.0.0.0')
    port  = config.getint('flask', 'port', fallback=8080)
    webapp.run(host=host, port=port)


def cmd_entry():
    """Entry point for command line script"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Web based frontend to the health record system databaser"
    )
    parser.add_argument('-c', '--config', required=True, help="Config file to load")
    args = parser.parse_args()

    main(args.config)
    

# Make script runnable
if __name__ == '__main__':
    cmd_entry()
