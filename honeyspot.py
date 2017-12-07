#!/usr/bin/env python

"""
/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <i@c0d.ist> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return. - Rahul
 * ----------------------------------------------------------------------------
 */
 """
#TODO: Add scoring method
#TODO: Add error handling
#TODO: Add module selection based upon protocol (http, ssh)

import sys
import os
import glob
import argparse
import imp
from ConfigParser import ConfigParser

__author__ = "c0dist@Garage4Hackers"

def print_banner():
    msg = """
         _   _                        _____             _   
        | | | |                      /  ___|           | |  
        | |_| | ___  _ __   ___ _   _\ `--. _ __   ___ | |_ 
        |  _  |/ _ \| '_ \ / _ \ | | |`--. \ '_ \ / _ \| __|
        | | | | (_) | | | |  __/ |_| /\__/ / |_) | (_) | |_ 
        \_| |_/\___/|_| |_|\___|\__, \____/| .__/ \___/ \__|
                                 __/ |     | |              
                                |___/      |_|              

        Spotting Honeypots for fun and (no) profit!
        author: %s
    """ % __author__
    print msg


class HoneySpot:
    def __init__(self, host=None, port=0):
        self.configs = self.parse_config()

        # Setting Modules directory
        modules_dir = self.configs.get("global", "modules_dir")
        if not os.path.isabs(modules_dir):
            modules_dir = os.path.abspath(modules_dir)
        self.modules_dir = modules_dir

    	self.modules = self.modules_list()
    	self.host = host
        self.port = port
    
    def modules_list(self):
        plugin_files = glob.glob(self.modules_dir + "/*.py")
        return [plugin.split("/")[-1] for plugin in plugin_files]

    def parse_config(self):
        conf = ConfigParser()
        conf.read("honeyspot.conf")
        return conf

    def run_module(self, module):
        """ 
        This trick is taken from CapTipper - https://github.com/omriher/CapTipper/blob/master/CTPlugin.py
        """
        module_file = self.modules_dir + "/" + module + ".py"
        full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), module_file)
        print "[+] Running the module - %s" % full_path
        (path, name) = os.path.split(full_path)
        (name, ext) = os.path.splitext(name)

        (p_file, filename, data) = imp.find_module(name, [path])
        try:
            mod = imp.load_module(name, p_file, filename, data)
        except ImportError:
            print "[-] Failed to import module. Exiting!"
            sys.exit(1)
        mod.run(self.host, self.port)


def main():
    if args.list_modules:
        spotter = HoneySpot()
        print "[+] Modules directory: {}".format(spotter.modules_dir)
        print "[+] Modules Available for use in `modules` Folder:"
        for module in spotter.modules:
            print "\t[*]", module.replace(".py", "")
        return 0

    if args.host:
        if not args.module:
            print "[-] No module defined to run against the target. Exiting"
            return 1
        spotter = HoneySpot(args.host, args.port)
        module = args.module
        spotter.run_module(module)

    
if __name__ == '__main__':
    print_banner()
    parser = argparse.ArgumentParser(description='Uncovers Honeypots.')
    parser.add_argument('-t', '--host', 
                        help='Target/Host where service is running.')
    parser.add_argument('-p', '--port', 
                        help='Port where service is running. If port is not given, default one will be used.',
                        type=int,
                        default=0)
    parser.add_argument('-m', '--module', 
                        help='Module to run against the target (without .py). \
                        List available modules using \'-ls\' option.')
    parser.add_argument('-ls', '--list-modules', 
                        help='Lists available modules.',
                        action="store_true",
                        default=False)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    sys.exit(main())