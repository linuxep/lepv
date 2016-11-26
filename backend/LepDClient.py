"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import json
import socket
from decimal import Decimal
import pprint
import re

class LepDClient:

    def __init__(self, server, port=12307, config='release'):
        self.server = server
        self.port = port
        self.bufferSize = 2048
        self.config = config

    def listAllMethods(self):
        response = self.sendRequest("ListAllMethod")
        if (response == None or 'result' not in response):
            return None
        
        results = response['result'].strip().split(" ")
        return results

    def ping(self):
        response = self.sendRequest("SayHello")
            
        print(response)
        if (response != None and 'result' in response and response['result'].startswith('Hello')):
            return True
        else:
            return False
        

    def getProcCpuinfoX(self):
        
        responseARM = '{"result":	"Processor\\t: ARMv7 Processor rev 4 (v7l)\\nprocessor\\t: 0\\nBogoMIPS\\t: 1810.43\\n\\nprocessor\\t: 1\\nBogoMIPS\\t: 1823.53\\n\\nFeatures\\t: swp half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt \\nCPU implementer\\t: 0x41\\nCPU architecture: 7\\nCPU variant\\t: 0x0\\nCPU part\\t: 0xc07\\nCPU revision\\t: 4\\n\\nHardware\\t: sun7i\\nRevision\\t: 0000\\nSerial\\t\\t: 0000000000000000\\nlepdendstring"}'
        
        responseX86 = '{"result":	"processor\\t: 0\\nvendor_id\\t: GenuineIntel\\ncpu family\\t: 6\\nmodel\\t\\t: 6\\nmodel name\\t: QEMU Virtual CPU\\nstepping\\t: 3\\nmicrocode\\t: 0x1\\ncpu MHz\\t\\t: 2599.998\\ncache size\\t: 4096 KB\\nphysical id\\t: 0\\nsiblings\\t: 1\\ncore id\\t\\t: 0\\ncpu cores\\t: 1\\napicid\\t\\t: 0\\ninitial apicid\\t: 0\\nfpu\\t\\t: yes\\nfpu_exception\\t: yes\\ncpuid level\\t: 13\\nwp\\t\\t: yes\\nflags\\t\\t: fpu de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pse36 clflush mmx fxsr sse sse2 syscall nx lm rep_good nopl pni cx16 x2apic popcnt hypervisor lahf_lm\\nbugs\\t\\t:\\nbogomips\\t: 5199.99\\nclflush size\\t: 64\\ncache_alignment\\t: 64\\naddress sizes\\t: 40 bits physical, 48 bits virtual\\npower management:\\n\\nprocessor\\t: 1\\nvendor_id\\t: GenuineIntel\\ncpu family\\t: 6\\nmodel\\t\\t: 6\\nmodel name\\t: QEMU Virtual CPU\\nstepping\\t: 3\\nmicrocode\\t: 0x1\\ncpu MHz\\t\\t: 2599.998\\ncache size\\t: 4096 KB\\nphysical id\\t: 1\\nsiblings\\t: 1\\ncore id\\t\\t: 0\\ncpu cores\\t: 1\\napicid\\t\\t: 1\\ninitial apicid\\t: 1\\nfpu\\t\\t: yes\\nfpu_exception\\t: yes\\ncpuid level\\t: 13\\nwp\\t\\t: yes\\nflags\\t\\t: fpu de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pse36 clflush mmx fxsr sse sse2 syscall nx lm rep_good nopl pni cx16 x2apic popcnt hypervisor lahf_lm\\nbugs\\t\\t:\\nbogomips\\t: 5199.99\\nclflush size\\t: 64\\ncache_alignment\\t: 64\\naddress sizes\\t: 40 bits physical, 48 bits virtual\\npower management:\\n\\nlepdendstring"}'
        
        response = json.loads(responseARM)
        
        return response


    def getTopOutput(self):
        response = self.sendRequest("GetCmdTop")
        if (response == None or 'result' not in response):
             return None

        response = response['result'].strip().split("\n")
        
        headerLine = response.pop(0)
        
        result = {}
        for responseLine in response:
            # print(responseLine)
            lineValues = responseLine.split()
            
            pid = lineValues[0]
            result[pid] = {}

            result[pid]['pid'] = pid
            result[pid]['user'] = lineValues[1]
            result[pid]['pri'] = lineValues[2]
            result[pid]['ni'] = lineValues[3]
            result[pid]['vsz'] = lineValues[4]
            result[pid]['rss'] = lineValues[5]
            result[pid]['s'] = lineValues[6]
            result[pid]['cpu'] = lineValues[7]
            result[pid]['mem'] = lineValues[8]
            result[pid]['time'] = lineValues[9]

            result[pid]['command'] = ' '.join([str(x) for x in lineValues[10:]])
            
            if(len(result) >= 25):
                break

        return result

    def getCmdPerfCpuclock(self, count=25):
        pass

    def getIostatResult(self):
        response = self.sendRequest("GetCmdIostat")
        if (response == None or 'result' not in response):
            return None

        resultLines = response['result'].split('\n')
        # 'Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util'
        # 'vda               9.31     0.44    0.24    0.42    38.76     4.04   129.68     0.00 6331.59 14163.45 1931.28   1.58   0.10'

        for i in range(len(resultLines)):
            if (not resultLines[i].startswith('Device:')):
                continue
            
            return resultLines[i:]

    def getCmdMpStat(self):
        response = self.sendRequest("GetCmdMpstat")
        if (response == None or 'result' not in response):
            return None

        lines = response['result'].strip().split("\n")

        lines.pop(0)
        lines.pop(0)
        return lines


    def getProcStat(self):
        response = self.sendRequest("GetProcStat")
        if (response == None or 'result' not in response):
            return None

        procStats = {}
        lines = response['result'].strip().split("\n")
        for line in lines:
            if "cpu" in line:
                data = line.split(" ")
                if data[1] == "":
                    data.pop(1)
                #This is cpuX
                procStat = {}

                procStat['id'] = data[0]
                procStat['user'] = Decimal(data[1])
                procStat['nice'] = Decimal(data[2])
                procStat['system'] = Decimal(data[3])
                procStat['idle'] = Decimal(data[4])
                procStat['iowait'] = Decimal(data[5])
                procStat['irq'] = Decimal(data[6])
                procStat['softirq'] = Decimal(data[7])
                procStat['steal'] = Decimal(data[8])
                procStat['guest'] = Decimal(data[9])
                procStat['guestnice'] = Decimal(data[10])

                total = procStat['user'] + procStat['nice'] + procStat['system'] + procStat['idle'] + procStat['iowait'] + procStat['irq'] + procStat['softirq'] + procStat['steal'] + procStat['guest'] + procStat['guestnice']

                procStat['user.ratio'] = Decimal(procStat['user'] / total * 100).quantize(Decimal('0.00'))
                procStat['nice.ratio'] = Decimal(procStat['nice'] / total * 100).quantize(Decimal('0.00'))
                procStat['system.ratio'] = Decimal(procStat['system'] / total * 100).quantize(Decimal('0.00'))
                procStat['idle.ratio'] = Decimal(procStat['idle'] / total * 100).quantize(Decimal('0.00'))
                procStat['iowait.ratio'] = Decimal(procStat['iowait'] / total * 100).quantize(Decimal('0.00'))
                procStat['irq.ratio'] = Decimal(procStat['irq'] / total * 100).quantize(Decimal('0.00'))
                procStat['softirq.ratio'] = Decimal(procStat['softirq'] / total * 100).quantize(Decimal('0.00'))
                procStat['steal.ratio'] = Decimal(procStat['steal'] / total * 100).quantize(Decimal('0.00'))
                procStat['guest.ratio'] = Decimal(procStat['guest'] / total * 100).quantize(Decimal('0.00'))
                procStat['guestnice.ratio'] = Decimal(procStat['guestnice'] / total * 100).quantize(Decimal('0.00'))

                procStats[procStat['id']] = procStat

        return procStats
    
    def tryAllMethods(self):
        methods = self.listAllMethods()
        
        failedMethods = []
        for methodName in methods:
            print('')
            print('<[ ' + methodName + " ]>")
            response = self.sendRequest(methodName)

            if (response == None or 'result' not in response):
                failedMethods.append(methodName)
                continue

            lines = response['result'].strip().split("\n")
            for line in lines:
                print(line)

        if (len(failedMethods) > 0):
            print("Methods that returned empty response:")
            for methodName in failedMethods:
                print(methodName)
        else:
            print("\n\nAdd methods are working!")
    
    
    def getPerfDataLines(self):
        armResponse = '''
        {
	"result":	"# To display the perf.data header info, please use --header/--header-only options.\\n#\\n#\\n# Total Lost Samples: 0\\n#\\n# Samples: 8K of event 'cpu-clock'\\n# Event count (approx.): 8050\\n#\\n# Overhead  Command      Shared Object       Symbol                         \\n# ........  ...........  ..................  ...............................\\n#\\n    98.47%  swapper      [kernel.kallsyms]   [k] default_idle\\n     0.78%  swapper      [kernel.kallsyms]   [k] __delay\\n     0.09%  kworker/0:1  [kernel.kallsyms]   [k] __delay\\n     0.07%  swapper      [kernel.kallsyms]   [k] tick_nohz_idle_enter\\n     0.06%  swapper      [kernel.kallsyms]   [k] _raw_spin_unlock_irq\\n     0.02%  perf         [kernel.kallsyms]   [k] sub_preempt_count\\n     0.02%  sleep        [kernel.kallsyms]   [k] _raw_spin_unlock_irqrestore\\n     0.02%  sleep        [kernel.kallsyms]   [k] in_lock_functions\\n     0.01%  kpktgend_0   [kernel.kallsyms]   [k] schedule\\n     0.01%  kworker/0:1  [kernel.kallsyms]   [k] Get_Bat_Coulomb_Count\\n     0.01%  kworker/0:1  [kernel.kallsyms]   [k] _raw_spin_unlock_irq\\n     0.01%  kworker/0:1  [kernel.kallsyms]   [k] i2c_sunxi_xfer\\n     0.01%  kworker/0:1  [kernel.kallsyms]   [k] nr_blockdev_pages\\n     0.01%  kworker/1:1  [kernel.kallsyms]   [k] gmac_mdio_read\\n     0.01%  menu-cached  libdbus-1.so.3.5.8  [.] 0x0000883e\\n     0.01%  perf         [kernel.kallsyms]   [k] __memzero\\n     0.01%  perf         [kernel.kallsyms]   [k] do_page_fault\\n     0.01%  sleep        [kernel.kallsyms]   [k] __lru_cache_add\\n     0.01%  sleep        [kernel.kallsyms]   [k] __raw_spin_lock\\n     0.01%  sleep        [kernel.kallsyms]   [k] _raw_spin_unlock_irq\\n     0.01%  sleep        [kernel.kallsyms]   [k] cgroup_exit\\n     0.01%  sleep        [kernel.kallsyms]   [k] do_lookup\\n     0.01%  sleep        [kernel.kallsyms]   [k] find_get_page\\n     0.01%  sleep        [kernel.kallsyms]   [k] flush_tlb_range\\n     0.01%  sleep        [kernel.kallsyms]   [k] link_path_walk\\n     0.01%  sleep        [kernel.kallsyms]   [k] radix_tree_lookup_element\\n     0.01%  sleep        ld-2.15.so          [.] 0x000070d2\\n     0.01%  sleep        ld-2.15.so          [.] 0x000074c4\\n     0.01%  sleep        ld-2.15.so          [.] 0x0000ca8e\\n     0.01%  sleep        libc-2.15.so        [.] 0x0001ed38\\n     0.01%  sleep        libc-2.15.so        [.] 0x00023658\\n     0.01%  sleep        libc-2.15.so        [.] 0x0004c7be\\n     0.01%  sleep        libc-2.15.so        [.] 0x00053cbe\\n     0.01%  sleep        libc-2.15.so        [.] 0x000585be\\n     0.01%  sleep        libc-2.15.so        [.] 0x00059e40\\n     0.01%  swapper      [kernel.kallsyms]   [k] _test_and_clear_bit\\n     0.01%  swapper      [kernel.kallsyms]   [k] file_free_rcu\\n     0.01%  swapper      [kernel.kallsyms]   [k] ipv4_get_l4proto\\n     0.01%  swapper      [kernel.kallsyms]   [k] rcu_idle_enter\\n     0.01%  x11vnc       [kernel.kallsyms]   [k] ktime_get_ts\\n     0.01%  x11vnc       [kernel.kallsyms]   [k] sys_gettimeofday\\n     0.01%  x11vnc       libX11.so.6.3.0     [.] 0x00010eb8\\n     0.01%  x11vnc       x11vnc              [.] 0x0005e540\\n     0.01%  x11vnc       x11vnc              [.] 0x00065884\\n\\n\\n#\\n# (Cannot load tips.txt file, please install perf!)\\n#\\nlepdendstring"
}
        '''
        
        x86Response = '''
        {
	"result":	"# ========\\n# captured on: Fri Nov 25 06:53:48 2016\\n# hostname : ubuntu\\n# os release : 3.13.0-32-generic\\n# perf version : 3.13.11.4\\n# arch : x86_64\\n# nrcpus online : 2\\n# nrcpus avail : 2\\n# cpudesc : Intel(R) Core(TM) i7-6500U CPU @ 2.50GHz\\n# cpuid : GenuineIntel,6,78,3\\n# total memory : 1002748 kB\\n# cmdline : /usr/lib/linux-lts-trusty-tools-3.13.0-32/perf record -a -e cpu-clock sleep 1 \\n# event : name = cpu-clock, type = 1, config = 0x0, config1 = 0x0, config2 = 0x0, excl_usr = 0, excl_kern = 0, excl_host = 0, excl_guest = 1, precise_ip = 0, attr_mmap2 = 0, attr_mmap  = 1, attr_mmap_data = 0\\n# HEADER_CPU_TOPOLOGY info available, use -I to display\\n# HEADER_NUMA_TOPOLOGY info available, use -I to display\\n# pmu mappings: cpu = 4, software = 1, tracepoint = 2, breakpoint = 5\\n# ========\\n#\\n# Samples: 2K of event 'cpu-clock'\\n# Event count (approx.): 698500000\\n#\\n# Overhead          Command                            Shared Object                           Symbol\\n# ........  ...............  .......................................  ...............................\\n#\\n    45.17%            uwsgi  libpython3.5m.so.1.0                     [.] 0x000000000011c525         \\n    12.96%            uwsgi  libpthread-2.19.so                       [.] 0x0000000000011770         \\n    11.92%            uwsgi  libc-2.19.so                             [.] 0x000000000007afa8         \\n     8.23%            uwsgi  [kernel.kallsyms]                        [k] context_tracking_user_exit \\n     5.94%            uwsgi  [kernel.kallsyms]                        [k] context_tracking_user_enter\\n     1.72%            uwsgi  [kernel.kallsyms]                        [k] system_call_after_swapgs   \\n     1.25%            uwsgi  _socket.cpython-35m-x86_64-linux-gnu.so  [.] 0x0000000000006b00         \\n     1.15%            uwsgi  [kernel.kallsyms]                        [k] audit_net                  \\n     0.89%            uwsgi  [kernel.kallsyms]                        [k] SYSC_recvfrom              \\n     0.89%            uwsgi  [kernel.kallsyms]                        [k] _raw_spin_lock_bh          \\n     0.82%            uwsgi  [kernel.kallsyms]                        [k] syscall_trace_enter        \\n     0.82%            uwsgi  [kernel.kallsyms]                        [k] fget_light                 \\n     0.82%            uwsgi  [kernel.kallsyms]                        [k] sock_recvmsg               \\n     0.75%            uwsgi  [kernel.kallsyms]                        [k] aa_revalidate_sk           \\n     0.57%            uwsgi  [kernel.kallsyms]                        [k] tcp_recvmsg                \\n     0.50%            uwsgi  [kernel.kallsyms]                        [k] sockfd_lookup_light        \\n     0.43%            uwsgi  [kernel.kallsyms]                        [k] syscall_trace_leave        \\n     0.43%            uwsgi  [kernel.kallsyms]                        [k] security_socket_recvmsg    \\n     0.36%            uwsgi  [kernel.kallsyms]                        [k] local_bh_enable_ip         \\n     0.36%            uwsgi  [kernel.kallsyms]                        [k] inet_recvmsg               \\n     0.36%            uwsgi  [kernel.kallsyms]                        [k] _raw_spin_unlock           \\n     0.36%            uwsgi  [kernel.kallsyms]                        [k] int_check_syscall_exit_work\\n     0.32%            uwsgi  [kernel.kallsyms]                        [k] local_bh_enable            \\n     0.32%            uwsgi  [kernel.kallsyms]                        [k] aa_net_perm                \\n     0.29%            uwsgi  [kernel.kallsyms]                        [k] apparmor_socket_recvmsg    \\n     0.21%            uwsgi  [kernel.kallsyms]                        [k] release_sock               \\n     0.21%            uwsgi  [kernel.kallsyms]                        [k] tcp_cleanup_rbuf           \\n     0.21%            uwsgi  [kernel.kallsyms]                        [k] _raw_spin_unlock_bh        \\n     0.14%            uwsgi  [kernel.kallsyms]                        [k] local_bh_disable           \\n     0.14%            uwsgi  [kernel.kallsyms]                        [k] sys_recvfrom               \\n     0.14%            uwsgi  [kernel.kallsyms]                        [k] tracesys                   \\n     0.11%           compiz  [kernel.kallsyms]                        [k] vmw_fifo_ping_host         \\n     0.11%            uwsgi  [kernel.kallsyms]                        [k] __do_softirq               \\n     0.11%            uwsgi  [kernel.kallsyms]                        [k] _cond_resched              \\n     0.11%            uwsgi  [kernel.kallsyms]                        [k] _raw_spin_unlock_irqrestore\\n     0.11%            uwsgi  [kernel.kallsyms]                        [k] retint_careful             \\n     0.07%            sleep  [kernel.kallsyms]                        [k] _raw_spin_unlock_irqrestore\\n     0.07%             Xorg  [kernel.kallsyms]                        [k] iowrite32                  \\n     0.07%             Xorg  [kernel.kallsyms]                        [k] vmw_fifo_ping_host         \\n     0.07%            uwsgi  [kernel.kallsyms]                        [k] lock_sock_nested           \\n     0.07%            uwsgi  [kernel.kallsyms]                        [k] int_ret_from_sys_call      \\n     0.07%            uwsgi  [kernel.kallsyms]                        [k] int_restore_rest           \\n     0.04%            sleep  [kernel.kallsyms]                        [k] __call_rcu                 \\n     0.04%       irqbalance  [kernel.kallsyms]                        [k] kstat_irqs                 \\n     0.04%       irqbalance  [kernel.kallsyms]                        [k] strcmp                     \\n     0.04%         vmtoolsd  libvmtools.so                            [.] 0x00000000000207a0         \\n     0.04%         vmtoolsd  libX11.so.6.3.0                          [.] _XEventsQueued             \\n     0.04%  ManagementAgent  [kernel.kallsyms]                        [k] __call_rcu                 \\n     0.04%           compiz  [kernel.kallsyms]                        [k] sock_def_readable          \\n     0.04%          firefox  libxul.so                                [.] 0x0000000001809fc8         \\n     0.04%            uwsgi  [kernel.kallsyms]                        [k] tcp_release_cb             \\n\\n\\n#\\n# (For a higher level overview, try: perf report --sort comm,dso)\\n#\\nlepdendstring"
}
        '''
        response = json.loads(armResponse)
        lines = response['result'].strip().split("\n")
        
        for line in lines:
            print(line)
            
        return lines
        

    def getResponse(self, methodName):
        response = self.sendRequest(methodName)
        if (response == None or 'result' not in response):
            return []

        lines = response['result'].strip().split("\n")
        return lines
        
        
    def sendRequest(self, methodName):
        sock = None

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialise our socket
            sock.connect((self.server, self.port)) # connect to host <HOST> to port <PORT>

            input_data = {}
            input_data['method'] = methodName

            dumped_data = json.dumps(input_data) # Dump the input dictionary to proper json

            sock.send(dumped_data.encode())
            serverResponse = str.encode("")
            end = str.encode("lepdendstring")
            while True:
                data = sock.recv(self.bufferSize)
                if end in data:
                    data = data.replace(end,str.encode(""))
                    serverResponse = serverResponse + data
                    break
                serverResponse = serverResponse + data
            responseJsonDecoded = json.loads(serverResponse.decode()) # decode the data received

            return responseJsonDecoded

        except Exception as error:
            print(methodName + ": " + str(error))
        finally:
            if (sock):
                sock.close()

if( __name__ =='__main__' ):

    pp = pprint.PrettyPrinter(indent=2)
    client = LepDClient('www.linuxxueyuan.com', config='debug')
    
    # client.ping()

    # client = LepDClient('www.linuxxueyuan.com')

    # client.getCmdPerfCpuclock()
    
    client.getPerfDataLines()
    
    # client.tryAllMethods()

    # pp.pprint(client.getIoTop())
    # pp.pprint(client.getCmdMpStat())
    
    # pp.pprint(client.sendRequest('GetProcSlabinfo'))
    # 
    # pp.pprint(client.ping())
    # 
    # print(client.getCmdVmstat())
    # 
    # pp.pprint(client.getAverageLoad())
    # 
    # pp.pprint(client.getTopResult())



