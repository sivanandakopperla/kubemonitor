from prometheus_client import Counter, Histogram


monitor_server_started = Counter('monitor_server_started', 'number of walks started')
monitor_server_completed = Counter('monitor_server_completed', 'number of walks completed')
invalid_monitor_server = Counter('invalid_monitor_server', 'number of walks attempted to be started, but invalid')

monitor_server_distance = Histogram('monitor_server_distance', 'distribution of distance walked',
                          buckets=[0, 50, 200, 400, 800, 1600, 3200])