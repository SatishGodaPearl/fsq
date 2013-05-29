#!/usr/bin/env python
# fsq-push(1) -- a program for pushing queue items to remote queues
#
# @author: Jeff Rand <jeff.rand@axial.net>
# @depends: fsq(1), fsq(7), python (>=2.7)
#
# This software is for POSIX compliant systems only.
import getopt
import sys
import fsq
import os

_PROG = "fsq-push"
_VERBOSE = False
_CHARSET = fsq.const('FSQ_CHARSET')

def chirp(msg):
    if _VERBOSE:
        shout(msg)

def shout(msg, f=sys.stderr):
    '''Log to file (usually stderr), with progname: <log>'''
    print >> f, "{0}: {1}".format(_PROG, msg)
    f.flush()

def usage(asked_for=0):
    '''Exit with a usage string, used for bad argument or with -h'''
    exit =  fsq.const('FSQ_SUCCESS') if asked_for else\
                fsq.const('FSQ_FAIL_PERM')
    f = sys.stdout if asked_for else sys.stderr
    shout('{0} [opts] src_queue trg_queue host item_id [item_id [...]]'.format(
          os.path.basename(_PROG)), f)
    if asked_for:
        shout('{0} [-p|--protocol=jsonrpc] [-L|--no-lock]'\
              '<proto>://<host>:<port>/url'.format(os.path.basename(_PROG)), f)
        shout('{0} [-p|--protocol=jsonrpc] [-L|--no-lock]'\
              'unix://var/sock/foo.sock'.format(os.path.basename(_PROG)), f)
        shout('        trg_queue host_queue item [item [...]]', f)
    return exit

def main(argv):
    global _PROG, _VERBOSE
    protocol = 'jsonrpc'
    lock = True

    _PROG = argv[0]
    try:
        opts, args = getopt.getopt(argv[1:], 'vhLp:', ( '--verbose', '--help',
                                                        '--no-lock',
                                                        '--protocol=', ))
        for flag, opt in opts:
            if flag in ( '-v', '--verbose', ):
                _VERBOSE = True
            if flag in ( '-p', '--protocol', ):
                protocol = opt
            if flag in ( '-L', '--no-lock', ):
                lock = False
            elif flag in ( '-h', '--help', ):
                return usage(1)

        if 4 > len(args):
            return usage()

        for item_id in args[3:]:
            chirp('pushing item {0} to remote {1} from host queue {2}'\
                  ' to queue {3}'.format(item_id, args[0], args[2], args[1],))
            item = fsq.FSQWorkItem(args[1], item_id , host=args[2], lock=lock)
            fsq.push(item, args[0], args[1], protocol=protocol)

    except ( fsq.FSQEnvError, fsq.FSQCoerceError, ):
        shout('invalid argument for flag: {0}'.format(flag))
        return fsq.const('FSQ_FAIL_PERM')
    except fsq.FSQInstallError, e:
        shout(e.strerror)
        return fsq.const('FSQ_FAIL_TMP')
    except getopt.GetoptError, e:
        shout('invalid flag: -{0}{1}'.format('-' if 1 < len(e.opt) else '',
              e.opt))
        return fsq.const('FSQ_FAIL_TMP')

if __name__ == '__main__':
    main(sys.argv)