import nginx

# read manifeast and have a for loop for apps for creating new conf files
c = nginx.Conf()
s = nginx.Server()
s.add(
    nginx.Key('listen', '5000'),
    nginx.Key('server_name', '_'),
    nginx.Location(' /',
         nginx.Key('proxy_pass', 'http://app_name:5000;'),
         nginx.Key('send_timeout;', '3600;'),
         nginx.Key('proxy_read_timeout', '3600;'),
         nginx.Key('proxy_send_timeout', '3600;'),
         nginx.Key('proxy_connect_timeout', '3600;')
    )
)
c.add(s)
nginx.dumpf(c, './test.conf')
