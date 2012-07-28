#DaTtSs emitter

import math

from dattss import DaTtSs

dts_test = DaTtSs('TEST_AUTH', debug=True).process('test')
dts_test.agg('cache', '132g!')
dts_test.agg('cache', '122g!')
dts_test.agg('test', '1c')
dts_test.agg('test', '2c')
dts_test.agg('test', '-4c')

dts_admin = DaTtSs('TEST_AUTH', debug=True).process('admin')
dts_admin.agg('toto', '1c!')


