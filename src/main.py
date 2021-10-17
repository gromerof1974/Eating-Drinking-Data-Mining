import scraper
import configparser
from distutils import util

def main():
    config = configparser.ConfigParser()
    config.read('scraper.properties')
    run_mode = config.get('Run', 'run_mode');
    
    if (run_mode == 'test'):
        run_test_mode(config)
    else:
        run_interactive_mode()       


''' 
-------------------------------------------------------------------------------------------------------
Run the scraper by reading the input arguments from scraper.properties
-------------------------------------------------------------------------------------------------------
'''
def run_test_mode(config):
    debug_enabled = bool(util.strtobool(config.get('Test', 'debug_enabled')))
    scroll_down = bool(util.strtobool(config.get('Test', 'scroll_down')))
    city = config.get('Test', 'city');
    scraper.scrape(city, debug_enabled, scroll_down)

   
''' 
-------------------------------------------------------------------------------------------------------
Run the scraper by reading the input arguments from the standard input
-------------------------------------------------------------------------------------------------------
'''    
def run_interactive_mode():
    city = input("Type the name of a city: ").strip()
    str_debug_enabled = input("Enable debug trace for verbose mode? [y/n]: ")
    str_scroll_down = input("Enable auto scrolling for getting all restaurants? [y/n]: ")
    print('\n')

    debug_enabled = False
    scroll_down = False
    if (str_debug_enabled.lower().strip() == 'y'):
        debug_enabled = True
    if (str_scroll_down.lower().strip() == 'y'):
        scroll_down = True
        
    scraper.scrape(city, debug_enabled, scroll_down)
   
main()        
 
    
