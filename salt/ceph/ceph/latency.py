#!/usr/bin/env python


import os
import sys
import re
import io
import cStringIO
import datetime
import argparse

OP_TRACKER_PATTERN=re.compile('op tracker -- seq: ([0-9]+), time: ([0-9\-:\. ]+), event: (.*), op: (.*)')

class Op:
    def __init__(self, seq, timestamp, event, op):
        self._seq = seq
        self._timestamp = timestamp
        self._event = event
        self._op = op

    @property
    def seq(self):
        return self._seq

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def event(self):
        return self._event

    @property
    def op(self):
        return self._op

class OpTracker:
    def __init__(self, id):
        self._seq = id
        self._actions = []

    @property
    def seq(self):
        return self._seq

    @property
    def events(self):
        return self._actions

    @property
    def latency(self):
        if len(self._actions) < 2:
            return datetime.timedelta(0)

        first = self._actions[0].timestamp
        last = self._actions[len(self._actions)-1].timestamp
        return last - first

    def add(self, timestamp, action, message):
        op = Op(self.seq, timestamp, action, message)
        self._actions.append(op)

    def sort(self):
        self._actions.sort(lambda x,y: x.timestamp < y.timestamp)
        
    def report(self):
        tslast = self._actions[0].timestamp
        buf = cStringIO.StringIO()
        buf.write('seq %d:\n' % (self.seq))
        for op in self._actions:
            buf.write('\t')
            buf.write(str(op.timestamp-tslast).rjust(14, ' '))
            buf.write('\t')
            buf.write(op.timestamp.strftime("%H:%M:%S.%f"))
            buf.write(op.event.rjust(35, ' '))
            buf.write('\t')
            buf.write(op.op)
            buf.write('\n')

            tslast = op.timestamp

        buf.write('\t')
        buf.write(str(self.latency).rjust(14, ' '))
        buf.write('\ttotal latency\n')

        print(buf.getvalue())
        buf.close()

def report_latency(fobj, min=None):
    tracks = {}
    for l in fobj:
        try:
            result = OP_TRACKER_PATTERN.search(l)
            if result == None:
                continue
            seq = int(result.group(1))
            timestamp = datetime.datetime.strptime(result.group(2),"%Y-%m-%d %H:%M:%S.%f") # 14:03:26.733656
            event = result.group(3)
            op = result.group(4)

            if not tracks.has_key(seq):
                tracks[seq] = track = OpTracker(seq)
            else:
                track = tracks[seq]

            track.add(timestamp, event, op)
        except:
            pass
    if min != None:
        min = datetime.timedelta(milliseconds=int(min))

    latencyStats = {}
    for seq, track in tracks.items():
        latency = track.latency
        curms = int(latency.total_seconds() * 1000)

        if latencyStats.has_key(curms):
            latencyStats[curms] = latencyStats[curms] + 1
        else:
            latencyStats[curms] = 1

        if min != None and latency < min:
            continue
        track.report()

    for i in latencyStats.keys():
        print("%d ms = %d" % (i, latencyStats[i]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log',  type=argparse.FileType('rb'))
    parser.add_argument('--min',  type=int, default=None)
    cmdobj = parser.parse_args()
    report_latency(cmdobj.log, cmdobj.min)

if __name__ == '__main__':
    main()