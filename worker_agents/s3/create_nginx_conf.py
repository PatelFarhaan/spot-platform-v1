import os
import nginx


main_application_port = int(os.getenv("CLIENT_APP_PORT"))
c = nginx.Conf()
s = nginx.Server()
s.add(
    nginx.Key('listen', '80'),
    nginx.Key('server_name', '_'),
    nginx.Location(' /',
                   nginx.Key('send_timeout', 3600),
                   nginx.Key('proxy_send_timeout', 3600),
                   nginx.Key('proxy_read_timeout', 3600),
                   nginx.Key('proxy_connect_timeout', 3600),
                   nginx.Key('proxy_pass', f'http://main_application:{main_application_port}')
                   )
    )
c.add(s)
nginx.dumpf(c, './nginx/conf.d/application.conf')
