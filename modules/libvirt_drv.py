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
        self.__connect()
        main_xml = self.__conn.getCapabilities()
        self.__root = ET.fromstring(main_xml)
        self.uuid = self.__root.find('./host/').text

    def __connect(self):
        try:
            if self.__conn.isAlive():
                return True
        except Exception, error:
            print error
        self.__conn = self.__lv.open("qemu+ssh://%s@%s/system" % (self.__login, self.__host))
        if self.__conn == None:
            return False
        return True

    def get_instance_desc(self, uuid, desc_hash=False):
        if not self.__connect():
            return False
        return self.__conn.lookupByUUIDString(uuid).XMLDesc()

    def get_instancs(self, run_only=True):
        if not self.__connect():
            return False
        instance = []
        for instance_id in self.__conn.listDomainsID():
            dom = self.__conn.lookupByID(instance_id)
            if dom.isActive() or run_only:
                instance.append({'uuid': dom.UUIDString(),
                                 'desc': dom.XMLDesc(),
                                 'status': dom.isActive(),
                                 'desc_hash': get_hash(dom.XMLDesc())})
        return instance

    def __del__(self):
        pass