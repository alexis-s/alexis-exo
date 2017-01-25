#!/bin/env python

"""
compare the number of events we requested to the number of events completed

arguments: 
  1: P3_*db.txt file from P3MC tasks spreadsheet
  2: *.txt json output from counting script 

"""


import os
import sys
import json
import locale




def compare_results(mc_db_filename, mc_results_filename):


    print "MC DB:", mc_db_filename
    print "MC results:", mc_results_filename

    mc_db_file = file(mc_db_filename)
    mc_db = json.load(mc_db_file)

    mc_results_file = file(mc_results_filename)
    mc_results = json.load(mc_results_file)
    mc_results_names = mc_results.keys()

    
    sims = mc_db["SIMS"]

    print "---> %i tasks completed" % len(mc_results)
    print "\n---> %i tasks requested:" % len(sims)

    print "name | requested | completed | percent complete"

    results_dict = {}

    for task in sims:
        name = task["name"]
        req_events = int(task["events"])
        complete_events = int(mc_results[name])
        mc_results_names.remove(name)

        result = "%s: %i | %i | %.2f" % (name, req_events, complete_events, complete_events/req_events)
        result = "{}: {:,} | {:,} | {:.0%}".format(
            name, 
            req_events, 
            complete_events, 
            1.0*complete_events/req_events
        )
        if 1.0*complete_events/req_events < 0.8: result += " ---> LOW STATS!"
        results_dict[name] = result

    keys = results_dict.keys()
    keys.sort()
    
    for name in keys:
        print results_dict[name]


    print "\n\n--> items remaining in list of completed sims:"
    mc_results_names.sort()
    for name in mc_results_names:
        print "\t", name


if __name__ == "__main__":

    if len(sys.argv) < 3:

        print "usage: [MC DB file like P3_0vBB_db.txt] [json output from counting MC results]"
        sys.exit()

    compare_results(sys.argv[1], sys.argv[2])

