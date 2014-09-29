__author__ = 'Vadim'

import libvirt
from mod_loader import get_hash
from xml.etree import ElementTree as ET

class Connect():

    def __init__(self, host='', login='', password=''):
        self.__host = host
        self.__login = login
        self.__password = password
        self.__lv = libvirt
        conn = self.__connect()
        main_xml = conn.getCapabilities()
        self.__root = ET.fromstring(main_xml)
        self.uuid = self.__root.find('./host/').text


    def __connect(self):
        return self.__lv.open("qemu+ssh://%s@%s/system" % (self.__login, self.__host))

    def get_instance_desc(self, uuid, desc_hash=False):
        conn = self.__connect()
        return conn.lookupByUUIDString(uuid).XMLDesc()

    def get_instancs(self, run_only=True):
        instance = []
        conn = self.__connect()
        for instance_id in conn.listDomainsID():
            dom = conn.lookupByID(instance_id)
            if dom.isActive() or run_only:
                instance.append({'uuid': dom.UUIDString(),
                                 'desc': dom.XMLDesc(),
                                 'status': dom.isActive(),
                                 'desc_hash': get_hash(dom.XMLDesc())})
        conn.close()
        return instance

    def __del__(self):
        pass