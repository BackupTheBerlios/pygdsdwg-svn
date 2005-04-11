# A demo plugin for Google Desktop Search
#
# This addin simply adds nothing.
#
# To register the addin, simply execute:
#   gdsPlugin.py
# This will install the COM server.
#
# To unregister completely:
#   gdsPlugin.py --unregister
#
# To debug, execute:
#   gdsPlugin.py --debug
#
# Then open Pythonwin, and select "Tools->Trace Collector Debugging Tool"
# Restart GDS, and you should see some output generated.
#

from win32com.server.exception import COMException
from win32com.client import gencache
import winerror
import pythoncom
import sys

# Specifics for GDS
GDS_ICON = "no icon"
GDS_FEXT = "hmf, herchu"

# Support for COM objects we use.
# Use these commands in Python code to auto generate .py support
gds = gencache.EnsureModule('{3D056FE7-EA8E-481A-B18F-0B02EBF6B3C1}', 0, 1, 0)

# The following class IS our COM Server.
# Please DO NO reuse the same GUID. 
TITLE = "PySimpleAnytext"
MYGUID = '{01C58A3B-18DB-4A5E-8F3E-3154C48DF4DE}'
DESCRIPTION = "A very simple text indexer in Python."

class GdsPlugin:
    _public_methods_ = [ 'HandleFile' ]
    _reg_clsid_ = MYGUID
    _reg_desc_ =  DESCRIPTION
    _reg_progid_ = TITLE
    _reg_policy_spec_ = "EventHandlerPolicy"

    def HandleFile(self, full_path_to_file, event_factory):
        print "HandleFile: ", full_path_to_file
        return 0

# Register the plugin within GDS
def RegisterPlugin(klass):
    reg = gds.GoogleDesktopSearchRegister()
    componentDesc = ["Title", TITLE, "Description", DESCRIPTION, "Icon", GDS_ICON];
    registration = reg.RegisterComponent(klass._reg_clsid_, componentDesc)
    ret = registration.RegisterExtension(GDS_FEXT)
    print "Plugin Registered."

# Unregister the plugin within GDS
def UnregisterPlugin(klass):
    reg = gds.GoogleDesktopSearchRegister()
    ret = reg.UnregisterComponent(klass._reg_clsid_)
    print "Plugin Unregistered."

# Use the command line for registration purposes
if __name__ == '__main__':
    # 1st, (un)register the COM server
    import win32com.server.register
    win32com.server.register.UseCommandLine(GdsPlugin)
    # ... later (un)register it within GDS.
    if "--unregister" in sys.argv:
        UnregisterPlugin(GdsPlugin)
    else:
        RegisterPlugin(GdsPlugin)

