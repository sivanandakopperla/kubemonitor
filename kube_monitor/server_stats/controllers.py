from server_stats.serializers import ServerStatsSerializer
from server_stats.models import ServerStats
from server_stats import metrics
import json
import pdb
import paramiko
from kafka import KafkaConsumer, KafkaProducer
import logging

logging.basicConfig(filename="server_stats.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

json_file = os.path.abspath(os.path.join('.'))+'/server_details.json'
with open(json_file, 'r') as fi:
    server_hosts = json.load(fi)


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        logger.info('Kafka - Message published successfully')
    except Exception as ex:
        logger.error('Kafka - Exception in publishing message')

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=[server_hosts[kafka_host]+':'+str(server_hosts[kafka_port])],
                                  api_version=(0, 10))
        logger.info('Kafka Creating producer obj and connected successfully')
    except Exception as ex:
        logger.error('Exception while connecting Kafka')
    finally:
        return _producer


def connect_kafka_consumer(topic_name):
    consumer = KafkaConsumer(topic_name, auto_offset_reset='earliest',
                             bootstrap_servers=[server_hosts[kafka_host]+':'+str(server_hosts[kafka_port])],
                             api_version=(0, 10), consumer_timeout_ms=1000)
    for msg in consumer:
        logging.info("Kafka message: ")
        logging.info(json.loads(msg.value))
    consumer.close()


def isHostValid(ip_add):
    host_dict = server_hosts['server_credentials']
    logger.info("Total host_dict {}".format(host_dict))
    for ip in host_dict:
        if ip["host"] == ip_add:
            logger.info("specific host_dict {}".format(ip))
            return True
    else:
        return False


def update_stats(request, ip_add=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host_dict = server_hosts['server_credentials']
    logger.info("Total host_dict {}".format(host_dict))
    if ip_add:
        for ip in host_dict:
            if ip["host"] == ip_add:
                host_dict = [ip]
                logger.info("specific host_dict {}".format(ip))
                break
    for host_detail in host_dict:
        ssh.connect(hostname=host_detail['host'], username=host_detail['username'],
                    password=host_detail['password'])
        logging.info(" {} connected successfully".format(host_detail['host']))
        cmd_list = ['df -hT /home', 'free -tm', 'uptime']
        stats = ServerStats()
        stats.server = host_detail['host']
        for cmd in cmd_list:
            try:
                if cmd == 'df -hT /home':
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    cmd_out = stdout.readlines(100)[1]
                    cmd_out = cmd_out.split()
                    file_system = cmd_out[0]
                    total_size = cmd_out[2]
                    used_space = cmd_out[3]
                    free_space = cmd_out[4]
                    use_percentage = cmd_out[5]
                    disk = {'file_system': file_system,
                            'total_size': total_size,
                            'used_space': used_space,
                            'free_space': free_space,
                            'use_percentage': use_percentage}
                    stats.disk_info = disk
                    logging.info("disk: ",disk)
                elif cmd == 'free -tm':
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    cmd_out2 = stdout.readlines(100)[1]
                    cmd_out2 = cmd_out2.split()
                    total_memory = cmd_out2[1]
                    used_memory = cmd_out2[2]
                    free_memory = cmd_out2[3]
                    shared_memory = cmd_out2[4]
                    cache_memory = cmd_out2[5]
                    available_memory = cmd_out2[6]
                    memory = {'total_memory': total_memory+'M',
                              'used_memory': used_memory+'M',
                              'free_memory': free_memory+'M',
                              'shared_memory': shared_memory+'M',
                              'cache_memory': cache_memory+'M',
                              'available_memory': available_memory+'M'}
                    stats.memory_info = memory
                    logging.info("memory: ", memory)
                elif cmd == 'uptime':
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    cmd_out3 = stdout.readlines(10)
                    up_time = cmd_out3[0].split(",")[0].strip()
                    stats.up_time = up_time
                    logging.info("uptime: ",up_time)
            except:
                logging.error("Error while fetching stats")
        stats.save()

        ssh.close()
        logging.info("Closing Paramiko")
    data = "Update success!"
    logging.info(data)
    return data


class ServerStatsController:
    def update_stats(self, request):
        metrics.monitor_server_started.inc()
        logging.info("metrics captured started")
        data = update_stats(request)
        result = {"status": "200_OK", "data": data}
        logging.info(result)
        producer = connect_kafka_producer()
        publish_message(producer, 'server_stats', 'stats', data)
        return json.dumps(result)

    def update_stats_specific(self, request, pk):
        metrics.monitor_server_started.inc()
        ip_add = pk.replace("_", ".")
        if isHostValid(ip_add):
            data = update_stats(request, ip_add)
            producer = connect_kafka_producer()
            publish_message(producer, 'server_stats', 'stats', data)
            result = {"status": "200_OK", "data": data}
            logging.info(result)
            return json.dumps(result)
        else:
            data = "Please provide your valid host"
            result = {"status": "404_NotFound", "data": data}
            logging.info(result)
            return json.dumps(result)

    def get_stats_info_list(self, request):
        if request.user.is_superuser:
            try:
                obj = ServerStats.objects.all()
                serializer_user = ServerStatsSerializer(obj, many=True)
                data = json.dumps(serializer_user.data)
                result = {"status": "200_OK", "data": data}
                logging.info(result)
                connect_kafka_consumer('server_stats')
                return json.dumps(result)
            except Exception as error:
                logging.error(error)
        else:
            data = "You dont have credentials to see all data"
            result = {"status": "403_Forbidden", "data": data}
            logging.info(result)
            return json.dumps(result)

    def get_stats_info(self, request, pk):
        ip_add = pk.replace("_",".")
        if isHostValid(ip_add):
            try:
                obj = ServerStats.objects.filter(server=ip_add)
                serializer_user = ServerStatsSerializer(obj, many=True)
                data = json.dumps(serializer_user.data)
                result = {"status": "200_OK", "data": data}
                logging.info(result)
                connect_kafka_consumer('server_stats')
                metrics.monitor_server_completed.inc()
                metrics.monitor_server_distance.observe(ServerStats.distance)
                logging.info("metrics captured")
                return json.dumps(result)
            except Exception as error:
                logging.error(error)
        else:
            data = "Please provide your valid host"
            result = {"status": "404_NotFound", "data": data}
            logging.info(result)
            return json.dumps(result)

    def stats_delete(self, request, pk):
        ip_add = pk.replace("_", ".")
        if isHostValid(ip_add):
            try:
                objs = ServerStats.objects.filter(server=ip_add)
                for obj in objs:
                    obj.delete()
                data = "Deleted Success!"
                result = {"status": "200_OK", "data": data}
                logging.info(result)
                producer = connect_kafka_producer()
                publish_message(producer, 'server_stats', 'stats', data)
                return json.dumps(result)
            except Exception as error:
                logging.error(error)
        else:
            data = "Please provide your valid host"
            result = {"status": "400_BadRequest", "data": data}
            logging.info(result)
            return json.dumps(result)
