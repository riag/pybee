
import sys

if sys.platform.startswith('win32'):
    pass
elif sys.platform.startswith('linux'):
    from pybee.platform import linux
elif sys.platform.startswith('darwin'):
    pass
