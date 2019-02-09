#!/usr/bin/env python
"""
PyMetric is a network simulation and visualisation tool. It
allows the user to trace paths through his network, given a
set of nodes and links with metrics (costs).

It allows the simulation of metric changes, router failures and
link outages, and provides various information relating to the
changes in topology and routing.

PyMetric can also show various statistics on the topology, such
as equal-cost paths, links with assymetric costs, longest paths
and lots more. It can even suggest some metric changes to help
the user with traffic engineering.

It still has some assumptions that are IS-IS specific, but they
are minor and will go away at some point. PyMetric should perform
its job regardless of the routing protocol used (as long as it
is a LSP)

"""
__version__   = "1.0-pre (git/master)"
__author__    = """Morten Knutsen (morten.knutsen@uninett.no)"""
__copyright__ = """Copyright (C) 2009-2010
Morten Knutsen <morten.knutsen@uninett.no>
"""
import matplotlib
import scripting
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="PyMetric Network Simulator")
    parser.add_argument('topofile',
                       help='Specify topology file to load')
    parser.add_argument('--script','-s', help='script file to load')
    parser.add_argument('--output','-o', help='png output file')
    args = parser.parse_args()

    infile = args.topofile

    if not args.script and not args.output:
        # Load interactive shell
        matplotlib.use("TkAgg")
        matplotlib.interactive(True)
        exec('from command import MetricShell')
        cli = MetricShell(filename=infile)
        cli.version = __version__
        cli.cmdloop()
    elif args.script and args.output:
        sys.stderr.write("ERROR: --script and --output can't be used together")
        sys.exit(1)
    else:
        # Load script
        matplotlib.use("cairo")
        matplotlib.interactive(False)
        exec('from command import MetricShell')
        old_stdout = sys.stdout
        sys.stdout = open("/dev/null", "w")
        cli = MetricShell(filename=infile)
        cli.version = __version__

        if args.output:
            cli.onecmd("png %s" % args.output)
            sys.exit(0)

        if args.script:
            se = scripting.ScriptEngine(cli)
            sys.exit(se.run(args.script))
