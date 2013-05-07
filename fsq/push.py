# fsq -- a python library for manipulating and introspecting FSQ queues
# @author: Jeff Rand <jeff.rand@axial.net>
#
# fsq/push.py -- provides remote distsitrubtion function: push
#
#     fsq is all unicode internally, if you pass in strings,
#     they will be explicitly coerced to unicode.
#
# This software is for POSIX compliant systems only.
import jsonrpclib
from . import FSQPushError, constants as _c, FSQWorkItem

def push(remote_addr, port, src_queue, item_id, trg_queue, protocol=u'jsonrpc'):
    remote = u'http://{0}:{1}'.format(remote_addr, port)
    item = FSQWorkItem(src_queue, item_id, host=remote_addr)
    try:
        if protocol == u'jsonrpc':
            try:
                server = jsonrpclib.Server(remote, encoding=_c.FSQ_CHARSET)
                out = server.enqueue(item.id, trg_queue, '', item.item.read())
                item.done()
                return out
            except Exception, e:
                item.fail()
                raise FSQPushError(e)
        raise ValueError('Unknown protocol: {0}'.format(protocol))
    finally:
        item.close()
