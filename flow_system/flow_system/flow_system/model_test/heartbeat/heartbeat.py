from model_test.models import HeartbeatRes
from queue import Queue

import dpkt
import logging
import numpy as np
import os
import pprint

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

THETA = 0.3  # 统计量
EPSILON = 4  # 最小时间间隔
TLS_VERSION_BYTES = {b'\x03\x01', b'\x03\x02', b'\x03\x03'}

data_dir = "/home/ningjing/flow_system/flow_system/flow_system/data_raw/"

'''
使用心跳方法对样本进行检测
'''
def heartbeat_detection():
    # 1 读取目录下的所有流量文件
    logging.debug("heartbeat_detection cwd: (%s)", os.getcwd())
    Host = {}
    SNI = {}
    for file in os.listdir(data_dir):
        with open(data_dir + file, 'rb') as f:
            if file.endswith("pcap"):
                capture = dpkt.pcap.Reader(f) 
            elif file.endswith("pcapng"):
                capture = dpkt.pcapng.Reader(f) 
            else:
                continue
            for n, (ts, buf) in enumerate(capture, start=1):
                eth = dpkt.ethernet.Ethernet(buf)
                if isinstance(eth.data, dpkt.ip.IP):
                    ip = eth.data
                    if isinstance(ip.data, dpkt.tcp.TCP):
                        tcp = ip.data
                        if len(tcp.data) > 0:
                            try:
                                # 2.1 解析获得HTTP结果
                                request = dpkt.http.Request(tcp.data)
                                host = request.headers["host"]
                                if host and request.method == 'GET':
                                    key = host
                                    add(Host, key)
                                    Host[key][0].append(n)
                                    Host[key][1].append(ts)
                            except dpkt.dpkt.UnpackError as e:
                                logging.debug("dpkt.dpkt.UnpackError: (%s%%)" % e)
                                continue
        # TLS的ClientHello报文可能分布在不同的packet中，需要借助Queue
        q = Queue()
        q.put(1)
        while not q.empty():
            e = q.get()
            with open(data_dir + file, 'rb') as f:
                if file.endswith("pcap"):
                    capture = dpkt.pcap.Reader(f) 
                elif file.endswith("pcapng"):
                    capture = dpkt.pcapng.Reader(f) 
                else:
                    continue
                idx = 0
                for ts, buf in capture:
                    idx += 1
                    if idx < e:
                        continue
                    eth = dpkt.ethernet.Ethernet(buf)
                    if isinstance(eth.data, dpkt.ip.IP):
                        ip = eth.data
                        if isinstance(ip.data, dpkt.tcp.TCP):
                            tcp = ip.data
                            if tcp.data:
                                # 2.2 解析获得HTTPS结果
                                if tcp.data[0] == 22:  # TLSHandshake
                                    if tcp.data[1:3] in TLS_VERSION_BYTES:  # tlsv1.0 - tlsv1.2
                                        try:
                                            rcds, i = dpkt.ssl.tls_multi_factory(tcp.data)
                                        except dpkt.ssl.SSL3Exception:  # 已经检查过Version，理论上不会被except
                                            continue
                                        # 保证得到的Handshake Record是完整的
                                        if i < len(tcp.data):  # tcp.data没有全部用完，最后一个Record不完整
                                            q.put(idx + 1)  # 记录当前报文的后一个报文
                                            dport = tcp.dport
                                            seq = tcp.seq
                                            l = len(tcp.data)  # segment的长度
                                            while i < len(tcp.data):
                                                try:
                                                    _, _pkt = capture.__next__()
                                                    idx += 1
                                                except StopIteration:
                                                    print('File ends.')  # 应该有但是没有
                                                    break
                                                _eth = dpkt.ethernet.Ethernet(_pkt)
                                                if isinstance(_eth.data, dpkt.ip.IP):
                                                    _ip = _eth.data
                                                    if isinstance(_ip.data, dpkt.tcp.TCP):
                                                        _tcp = _ip.data
                                                        # 同一内容的分段
                                                        if _tcp.dport == dport and _tcp.flags & 0x10 and _tcp.seq == l + seq:
                                                            tcp.data = tcp.data + _tcp.data
                                                            l += len(_tcp.data)
                                                            try:
                                                                _, i = dpkt.ssl.tls_multi_factory(tcp.data)
                                                            except dpkt.ssl.SSL3Exception:  # bad TLS Version
                                                                break
                                                            # 可能会i == len(tcp.data) Index out Range
                                                            if i < len(tcp.data) and tcp.data[i] != 22:  # not handshake
                                                                break
                                            # 处理完粘包的tcp.data就break，退出while循环
                                            # 下次从idx + 1开始解析
                                            try:
                                                rcds, _ = dpkt.ssl.tls_multi_factory(tcp.data)
                                            except dpkt.ssl.SSL3Exception:  # bad TLS Version
                                                continue
                                            for r in rcds:
                                                try:
                                                    hss, _ = tls_multi_handshake(r.data)
                                                except dpkt.ssl.SSL3Exception:  # bad handshake type
                                                    break
                                                for h in hss:
                                                    if isinstance(h.data, dpkt.ssl.TLSClientHello):
                                                        ch = h.data
                                                        # h.data 即handshake protocol包的数据段，不包括 handshake type 和length字段，
                                                        # 从version字段开始计算长度
                                                        ext = ch.extensions
                                                        for each in ext:
                                                            if each[0] == 0:
                                                                sni = str(each[1][5:], encoding='utf-8')
                                                                key = sni
                                                                add(SNI, key)
                                                                SNI[key][0].append(idx)
                                                                SNI[key][1].append(ts)
                                            break
                                        # 处理直接得到的完整的tls handshake包 即i = len(tcp.data)
                                        try:
                                            rcds, _ = dpkt.ssl.tls_multi_factory(tcp.data)
                                        except dpkt.ssl.SSL3Exception:  # bad TLS Version
                                            continue
                                        for r in rcds:
                                            try:
                                                hss, _ = tls_multi_handshake(r.data)
                                            except dpkt.ssl.SSL3Exception:  # bad handshake type
                                                break
                                            for h in hss:
                                                if isinstance(h.data, dpkt.ssl.TLSClientHello):
                                                    ch = h.data
                                                    ext = ch.extensions
                                                    for each in ext:
                                                        if each[0] == 0:
                                                            sni = str(each[1][5:], encoding='utf-8')
                                                            key = sni
                                                            add(SNI, key)
                                                            SNI[key][0].append(idx)
                                                            SNI[key][1].append(ts)
    # 2 过滤心跳Host
    for k in Host.keys():
        seq = getInterval(Host[k][1], EPSILON)
        Host[k].append(seq)
        if len(seq) > 1 and md(seq) / np.mean(seq) < THETA:
            # 3 保存至数据库
            HeartbeatRes(domain=k, is_http=True, sequence_len=len(seq), sequence_mean=np.mean(seq)).save()
    # 2 过滤心跳Host
    for k in SNI.keys():
        seq = getInterval(SNI[k][1], EPSILON)
        SNI[k].append(seq)
        if len(seq) > 1 and md(seq) / np.mean(seq) < THETA:
            # 3 保存至数据库
            HeartbeatRes(domain=k, is_http=False, sequence_len=len(seq), sequence_mean=np.mean(seq)).save()

def add(d, k):
    if k not in d.keys():
        d[k] = [[], []]


def getInterval(l, thr):
    intervals = []

    if len(l) < 2:
        return intervals
    else:
        for i in range(len(l) - 1):
            interval = l[i + 1] - l[i]
            if interval > thr:
                intervals.append(interval)
        return intervals


def md(l):
    r"""
    return Mean Deviation
    """
    if len(l) == 0 or len(l) == 1:
        return 0
    mean = np.mean(l)
    sum = 0
    for i in range(len(l)):
        sum += abs(mean - l[i])
    return sum / len(l)

def tls_multi_handshake(buf):
    i, n = 0, len(buf)
    msgs = []
    while i + 4 <= n:
        t = buf[0]
        if t in dpkt.ssl.HANDSHAKE_TYPES.keys():
            try:
                msg = dpkt.ssl.TLSHandshake(buf[i:])
                msgs.append(msg)
            except dpkt.NeedData:
                break
        else:
            raise dpkt.ssl.SSL3Exception('Bad TLS HandshakeType in buf: %r' % buf[i:i + 4])
        i += len(msg)
    return msgs, i