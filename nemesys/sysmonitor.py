# sysmonitor.py
# -*- coding: utf8 -*-

# Copyright (c) 2010 Fondazione Ugo Bordoni.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


#from SystemProfiler import SystemProfiler
from xml.dom.minidom import parse
import xml.parsers.expat
from string import join
from xml.etree import ElementTree as ET
from logger import logging
from xmlutils import getvalues
import paths


tag_results = 'SystemProfilerResults'
tag_threshold = 'SystemProfilerThreshold'
tag_vers = 'vers'
tag_avMem = 'availableMemory'
tag_wireless = 'wirelessON'
tag_fw = 'firewall'
tag_memLoad = 'memoryLoad'
tag_ip = 'ipAddr'
tag_sys = 'system'
tag_wdisk = 'diskWrite'
tag_cpu = 'cpuLoad'
tag_mac = 'macAddr'
tag_rdisk = 'diskRead'
tag_release = 'release'
tag_cores = 'cores'
tag_arch = 'arch'
tag_proc = 'processor'
tag_hosts = 'hostNumber'
tag_task = 'taskList'
tag_conn = 'activeConnections'

msg = '\nImpossibile effettuare la misura a causa delle condizioni non ideali del sistema!'

_sysdata = open('./result1.xml') #andrà sostituita con dati passati da sysProfiler
_thdata = open(paths.THRESHOLD)

def checkall():
  response = True
  #d = {tag_vers, tag_avMem, tag_wireless, tag_fw, tag_memLoad, tag_ip, tag_sys, tag_wdisk, tag_cpu, tag_mac, tag_rdisk, tag_release, tag_cores, tag_arch, tag_proc, tag_hosts, tag_task, tag_conn}

  #try 
  #  SystemProfiler (fileOutput, d)
  #except Exception as e:
  #  logger.debug('Errore durante il monitorig del sistema (checkall): %s' % e)
    

  values = getvalues(_sysdata, tag_results)
  
  threshold = getvalues(_thdata, tag_threshold)
  
  #logica di controllo del sistema

  connectionCheck(values[tag_conn], threshold[tag_conn])
  
  if values[tag_hosts] != 1:
    raise Exception, 'Presenza altri host in rete!'+str(msg)
  if values[tag_fw] != False:
    raise Exception, 'Firewall attivo!'+str(msg)
  if values[tag_wireless] != False:
    raise Exception, 'Wireless LAN attiva!'+str(msg)

  #logica di controllo con soglie lette da xml

  if values[tag_avMem] > threshold[tag_avMem]:
    raise Exception, 'Memoria non sufficiente!'+str(msg)
  if values[tag_memLoad] > threshold[tag_memLoad]:
    raise Exception, 'Memoria non sufficiente!'+str(msg)
  if values[tag_cpu] > threshold[tag_cpu]:
    raise Exception, 'CPU occupata!'+str(msg)
  if values[tag_wdisk] > threshold[tag_wdisk]:
    raise Exception, 'Eccessiva attività in scrittura del disco!'+str(msg)
  if values[tag_rdisk] > threshold[tag_rdisk]:
    raise Exception, 'Eccessiva attività in lettura del disco!'+str(msg)

    
  return True

  

def mediumcheck():

#  d = {tag_avMem, tag_wireless, tag_fw, tag_memLoad, tag_cpu, tag_hosts, tag_task, tag_conn}
#  try 
#    SystemProfiler (fileOutput, d)
#  except Exception as e:
#    logger.debug('Errore durante il monitorig del sistema (mediumcheck): %s' % e)

  #parsing xml
  values = getvalues(1)  
  threshold = getvalues (2)

  #logica di controllo del sistema
  
  connectionCheck(values[tag_conn], threshold[tag_conn])
   
  if values[tag_fw] != False:
    raise Exception, 'Firewall attivo!'+str(msg)
  if values[tag_wireless] != False:
    raise Exception, 'Wireless LAN attiva!'+str(msg)

  #logica di controllo con soglie lette da xml

  if values[tag_avMem] > threshold[tag_avMem]:
    raise Exception, 'Memoria non sufficiente!'+str(msg)
  if values[tag_memLoad] > threshold[tag_memLoad]:
    raise Exception, 'Memoria non sufficiente!'+str(msg)
  if values[tag_cpu] > threshold[tag_cpu]:
    raise Exception, 'CPU occupata!'+str(msg)
 
  return True



def fastcheck():

#  d = {tag_memLoad, tag_cpu, tag_task, tag_conn}
#  try 
#    SystemProfiler (fileOutput, d)
#  except Exception as e:
#    logger.debug('Errore durante il monitorig del sistema (fastcheck): %s' % e)

  #parsing xml
  values = getvalues(1)  
  threshold = getvalues (2)

  #logica di controllo del sistema
  #logica di controllo con soglie lette da xml

  connectionCheck(values[tag_conn], threshold[tag_conn])

  if values[tag_avMem] > threshold[tag_avMem]:
    raise Exception, 'Memoria non sufficiente!'+str(msg)
  if values[tag_memLoad] > threshold[tag_memLoad]:
    raise Exception, 'Memoria non sufficiente!'+str(msg)
  if values[tag_cpu] > threshold[tag_cpu]:
    raise Exception, 'CPU occupata!'+str(msg)

  return True



#creazione dizionario con risposte del SystemProfiler
def getvalues(data, tag):
  '''
  #parsing xml
  if i == 1:
    data = open('./result1.xml')
    tag_primary = tag_results
  if i == 2: 
    data = open('./threshold.xml')
    tag_primary = tag_threshold
  '''
  try:
    xml = parse(data)
  except ExpatError as e:
    #logger.error('Il dato ricevuto non è in formato XML: %s' % data)
    return None
  
  nodes = xml.getElementsByTagName(tag)
  if (len(nodes) < 1):
    #logger.debug('Nessun risultato trovato nell\'XML:\n%s' % xml.toxml())
    return None
 
  node = nodes[0]
  
  values = {}
  
  for subelement in ET.XML(node.toxml()):
    values.update({subelement.tag:subelement.text})
  
  '''
  inserire controllo su valori riportati da SystemProfiler
  '''

  return values


#ettettua il controllo sulle connessioni attive  
def connectionCheck(connActive, connList):
  
  c = []
  for j in connActive.split(';'):
    c.append(j.split(':')[1])
  
  for i in connList.split(';'):
    if i in c:
      raise Exception, 'Sono attive connessioni non desiderate: '+str(msg)
  
  return True


  

if __name__ == '__main__':
 import sysmonitor
 ip = checkall()
 print 'test sysmonitor'
 print ip
