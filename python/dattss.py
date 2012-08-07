# DaTtSs Python Wrapper

__author__ = 'Stanislas Polu <polu.stanislas@gmail.com>'
__version__ = '0.1.0'

import pycurl
import threading
import re
import math
import json


class Process():
  '''Class implementing a DaTtSs Client Process'''

  def __init__(self, name, auth, pct=0.1, host='agg.dattss.com', port=80, push_period=5.0, debug=False):
    '''Args: name the name of the process
             auth the AUTH_KEY
             pct [optional] the percentile value
             host [optional] the DaTtSs server host
             port [optional] the DaTtSs server port
             push_period [optional] the period for commit & push'''
    '''Parameters'''
    self.name = name
    self.auth = auth
    self.pct = pct
    self.host = host
    self.port = port
    self.push_period = push_period
    self.debug = debug

    '''Locking & Timers'''
    self.stopped = False
    self.lock = threading.Lock()
    self.timer = None

    '''The accumulator'''
    self.acc = { "c": {},
                 "g": {},
                 "ms": {} };
    
    '''Starting'''
    self.start()

  def make_partials(self):
    '''Computes the partials from the accumulated values
       Returns: partial a computed partial'''
    if self.debug:
      print "DaTtSs: " + self.name + " make_partials"
    partials = { "c": [],
                 "g": [],
                 "ms": [] }
    for typ in ['c', 'ms', 'g']:
      if typ in self.acc:
        for st in self.acc[typ]:
          p = { "typ": typ,
                "nam": st,
                "pct": self.pct,
                "sum": 0,
                "cnt": 0,
                "max": None,
                "min": None,
                "fst": None,
                "lst": None,
                "emp": False }

          def dsort(a, b):
            return a['date'] - b['date']
          self.acc[typ][st].sort(dsort)

          for v in self.acc[typ][st]:
            p['sum'] += v['value']
            p['cnt'] += 1
            if p['max'] is None: 
              p['max'] = v['value']
            else:
              if p['max'] < v['value']:
                p['max'] = v['value']
            if p['min'] is None:
              p['min'] = v['value']
            else:
              if p['min'] > v['value']:
                p['min'] = v['value']
              if p['fst'] is None:
                p['fst'] = v['value']
            p['lst'] = v['value']
            p['emp'] = p['emp'] or v['emphasis']
            
          def vsort(a, b):
            return a['value'] - b['value']
          self.acc[typ][st].sort(vsort)
          l = len(self.acc[typ][st])
          bidx = int(max(min(math.ceil(self.pct * l), l-1), 0))
          tidx = int(max(min(round((1.0 - self.pct) * l), l-1), 0))
          p['bot'] = self.acc[typ][st][bidx]['value']
          p['top'] = self.acc[typ][st][tidx]['value']

          partials[typ] += [p]

    self.acc = { "c": {},
                 "g": {},
                 "ms": {} }
    return partials

  def do_commit(self):
    '''Compute the partials and sends it to the DaTtSs server'''
    with self.lock:
      if not self.stopped:
        if self.debug:
          print "DaTtSs: " + self.name + " do_commit"
        commit = { "nam": self.name,
                   "upt": 0,
                   "prt": self.make_partials() }
        url = "http://%s:%d/agg?auth=%s" % (self.host, self.port, self.auth)
        if self.debug:
          print "POST " + url
          print json.dumps(commit)
        ''' TODO: Post Data ''' 
        self.timer = threading.Timer(self.push_period, self.do_commit)
        self.timer.start()

  def agg(self, stat, value):
    '''Aggregates a a new value
       Args: stat the statistic name
             value the statistic value (as string with type [see doc])'''
    with self.lock:
      if not self.stopped:
        stat_m = re.match("^[A-Za-z0-9\-_\.\!]+$", stat)
        if not stat_m:
          return

        val_m = re.match("(-?[0-9]+)(c|ms|g)(\!?)", value)
        if val_m:
          typ = val_m.group(2)
          val = int(val_m.group(1))
          emph = val_m.group(3) == "!"
          if not stat in self.acc[typ]:
            self.acc[typ][stat] = []
          self.acc[typ][stat] += [{ 'date': 0,
                                    'value': val,
                                    'emphasis': emph }]
          if self.debug:
            print "DaTtSs: " + self.name + " agg " + stat + " " + typ + " " + str(val) + " " + str(emph)

  def start(self):
    '''Starts the commit timers and accepts data'''
    if self.debug:
      print "DaTtSs: " + self.name + " start"
    self.stopped = False
    self.timer = threading.Timer(self.push_period, self.do_commit)
    self.timer.start()

  def stop(self):
    '''Stops the commit timers and refuse data'''
    if self.debug:
      print "DaTtSs: " + self.name + " stop"
    if not self.timer is None:
      self.timer.cancel()
      self.timer = None
    self.stopped = True
    


class DaTtSs():
  '''Class implementing the Process Singleton generator'''

  '''Cache containing the singleton processes (class variable)'''
  cache = {} 
  lock = threading.Lock()

  def __init__(self, auth, host='agg.dattss.com', port=80, pct=0.1, push_period=5.0, debug=False):
    '''Args: auth the AUTH_KEY
             pct [optional] the percentile value
             host [optional] the DaTtSs server host
             port [optional] the DaTtSs server port
             push_period [optional] the period for commit & push'''
    self.auth = auth
    self.host = host
    self.port = port
    self.pct = pct
    self.debug = debug
  
  def process(self, name, auth=None, pct=None):
    '''Builds or return a process for a auth and name
       Args: name the name of the process
             auth [optional] the AUTH_KEY
             pct [optional] the percentile value'''
    if auth is None:
      auth = self.auth
    if pct is None:
      pct = self.pct

    with DaTtSs.lock:
      if not auth in self.cache:
        DaTtSs.cache[auth] = {}
      if not name in self.cache[auth]:
        DaTtSs.cache[auth][name] = Process(name, auth, pct=pct, host=self.host, port=self.port, debug=self.debug)

      return DaTtSs.cache[auth][name]

