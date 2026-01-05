# This test does nothing but reset the system.
# Use this to explicity reset within a group
import wctestlist

def main(d, WCURLS, systemType=None):
    # new_system_type is the systemType we giv in udata, or
    # d.wcutils.systemType, or None
    systemType = systemType or d.getUserData('systemType')
    if not d.wcutils.clean or getattr(d.wcutils, 'systemType', systemType) != systemType:
        # We only reset if the system is dirty.  This prevents multiple
        # consecutive resets
        d.wcutils.resetSystem(systemType=systemType)
    else:
        d.initComment("System was already clean, no action taken")
