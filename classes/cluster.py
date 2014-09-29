__author__ = 'Vadim'

from mod_loader import import_module, get_index, update_dic_in_list, get_hash
import hashlib, threading


class Cluster():

    def __init__(self, driver='libvirt_drv', mod_path='modules'):
        self.__driver = driver
        self.__mod_path = mod_path
        self.__nodes = {}
        self.__instances = []

    def add_node(self, auth={}):
        try:
            load_driver = import_module(self.__mod_path,
                                        self.__driver,
                                       'Connect').Connect(host=auth['host'],
                                                               login=auth['login'],
                                                               password=auth['password'])
        except Exception, error:
            print(error)
            return False
        self.__nodes.update({load_driver.uuid: load_driver})
        self.__update_nodes_status()
        return True

    def start_cron(self):
        self.__timer = threading.Timer(60, self.__update_nodes_status())
        self.__timer.start()

    def live_migrate_instance(self, instance_id):
        pass

    def __update_nodes_status(self):
        for node_uuid, driver in self.__nodes.iteritems():
            raw_list = driver.get_instancs()
            for instance in raw_list:
                try:
                    old_instance = get_index(self.__instances, 'uuid', instance['uuid'])
                    disc = driver.get_instance_desc(instance['uuid'])
                    if get_hash(disc) != old_instance['desc_hash']:
                        old_instance['desc_hash'] = get_hash(disc)
                        old_instance['desc'] = disc
                except Exception, error:
                    print error
                    self.__instances.append({'uuid': instance['uuid'],
                                         'status': instance['status'],
                                         'on_node': node_uuid,
                                         'desc_hash': instance['desc_hash'],
                                         'desc': instance['desc']})

    def get_instances(self):
        return self.__instances

    def __restart_on_other_node(self, node_id, instance_id):
        pass

    def __del__(self):
        pass