"""
   Verifies the limit function by IP address works correctly
"""
from wcunittest import wcElement

def main(d, WCURL):
   u = d.getWCUnitTest('Verify Access to Function')
   u.setup(lambda d: d.miedb.dbExec('INSERT INTO acceptable_ips SET host_name=%s,ip_address=%s,subnet=%s,timeout=0,security_role_id=0,func=%s',
   																	'192.168.240.0-activeX','15771840','24','activeX'), reason='Limit f=activeX to a local subnet')
   u.setup(lambda d: d.miedb.dbExec('INSERT INTO acceptable_ips SET host_name=%s,ip_address=%s,subnet=%s,timeout=0,security_role_id=0,func=%s',
   																	'10.6.5.0-activeX','329226','24','activeX'), reason='Limit f=activeX to a local subnet')
   u.setup(lambda d: d.navigate('?f=activeX'), reason='View the function\'s "Unspecified control" page appears')
   u.verifyElements(
      # Verify the unspecified control message displays
      wcElement('xpath','//pre',text='ERROR: Unknown Embedded Control ()')
   )
   u.test()
   
   u = d.getWCUnitTest('Verify No Access to Function')
   u.setup(lambda d: d.miedb.dbExec('UPDATE acceptable_ips SET host_name=%s,ip_address=%s,subnet=%s WHERE host_name=%s',
   																	'10.2.2.0-activeX','131594','32','192.168.240.0-activeX'), reason='Limit f=activeX to a different subnet')
   u.setup(lambda d: d.miedb.dbExec('UPDATE acceptable_ips SET host_name=%s,ip_address=%s,subnet=%s WHERE host_name=%s',
   																	'10.2.1.0-activeX','131594','32','10.6.5.0-activeX'), reason='Limit f=activeX to a different subnet')
   u.setup(lambda d: d.navigate('?f=activeX'), reason='Function is not allowed. Get directed to the user default page')
   u.verifyElements(
      # Verify the user is redirected to their Omniscope page
      wcElement('xpath','//div[@class="portlet-header"]/label',text='Administrator Welcome')
   )
   u.test()

   u = d.getWCUnitTest('Verify multiple subnets have access to Function')
   u.setup(lambda d: d.miedb.dbExec('INSERT INTO acceptable_ips SET host_name=%s,ip_address=%s,subnet=%s,timeout=0,security_role_id=0,func=%s',
   																	'192.168.240.0-activeX','15771840','24','activeX'), reason='Limit f=activeX to a local subnet')
   u.setup(lambda d: d.miedb.dbExec('INSERT INTO acceptable_ips SET host_name=%s,ip_address=%s,subnet=%s,timeout=0,security_role_id=0,func=%s',
   																	'10.6.5.0-activeX','329226','24','activeX'), reason='Limit f=activeX to a local subnet')
   u.setup(lambda d: d.navigate('?f=activeX'), reason='View the function\'s "Unspecified control" page appears')
   u.verifyElements(
      # Verify the unspecified control message displays
      wcElement('xpath','//pre',text='ERROR: Unknown Embedded Control ()')
   )
   u.test()
   