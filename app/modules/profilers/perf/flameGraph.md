# Flame Graph in LEP

## Data Flow

### *LEPD* ( data collecting by perf)

The perf tools are integrated in the Linux kernel since the 2.6 version.
The perf tools are based on the perf events subsystem.
The perf profiler uses hardware counters to profile the application.
The result of this profiler are really precise and because it is not doing instrumentation of the code, it is really fast.

The LEPD command for flame graph is as below:

```shell
perf record -F 99 -a -g -- sleep 1;perf script
```

#### - perf report
to see the list of the most costly functions, you just have to use perf report
```shell
perf report
```

then you will see a list of the most costly functions ordered by cost, like this:
```shell
# Events: 374K cycles
#
# Overhead         Command             Shared Object
# ........  ..............  ........................  ...............................................................
#
    87.58%        inlining  [vesafb]                  [k] 0xffffffff81100700
    83.27%         readelf  [vesafb]                  [k] 0xffffffff815c3930
    41.40%              sh  [vesafb]                  [k] 0xffffffff815c3930
    37.74%        inlining  libstdc++.so.6.0.14       [.] 0x653e0
    12.49%         readelf  libc-2.13.so              [.] vfprintf
     5.37%        inlining  inlining                  [.] parseFunction(std::string, std::string, std::map
     5.20%         readelf  libc-2.13.so              [.] _IO_new_file_xsputn
     4.50%         readelf  readelf                   [.] 0x150e
```

For every functions, you have the information about the cost of the function, the command used to launch it and the shared object in which the function is located.

##### - perf record

perf-record - Run a command and record its profile into perf.data
This command runs a command and gathers a performance counter profile from it, into perf.data - without displaying anything.
This file can then be inspected later on, using perf report.

-a, --all-cpus
System-wide collection from all CPUs.

-g, --call-graph
Do call-graph (stack chain/backtrace) recording.

-F, --freq=
Profile at this frequency.

An output example
```code
# To display the perf.data header info, please use --header/--header-only options.
#
#
# Total Lost Samples: 0
#
# Samples: 198  of event 'cpu-clock'
# Event count (approx.): 1999999980
#
# Children      Self  Command   Shared Object      Symbol
# ........  ........  ........  .................  .............................
#
    60.61%     0.00%  swapper   [kernel.kallsyms]  [k] default_idle
             |
             ---default_idle
                native_safe_halt

    60.61%    60.61%  swapper   [kernel.kallsyms]  [k] native_safe_halt
             |
             |--31.31%-- start_secondary
             |          cpu_startup_entry
             |          default_idle_call
             |          arch_cpu_idle
             |          default_idle
             |          native_safe_halt
             |
              --29.29%-- x86_64_start_kernel
                        x86_64_start_reservations
                        start_kernel
                        rest_init
                        cpu_startup_entry
                        default_idle_call
                        arch_cpu_idle
                        default_idle
                        native_safe_halt
```

##### - perf script
perf-script - Read perf.data (created by perf record) and display trace output
You can also run a set of pre-canned scripts that aggregate and
summarize the raw trace data in various ways (the list of scripts is
available via 'perf script -l').

-f, --fields
Comma separated list of fields to print.
Options are:
- comm
- tid
- pid
- time
- cpu
- event
- trace
- ip
- sym
- dso
- addr
- symoff

Field list can be prepended with the type, trace, sw or hw, to indicate to which event type the field list applies.
e.g., -f sw:comm,tid,time,ip,sym and -f trace:time,cpu,trace

An output snippet looks like this:
```code
swapper     0 [000] 1212828.569239:   10101010 cpu-clock:

   7fff810665d6 native_safe_halt ([kernel.kallsyms])

   7fff8103ae1e default_idle ([kernel.kallsyms])

   7fff8103b62f arch_cpu_idle ([kernel.kallsyms])

   7fff810c64da default_idle_call ([kernel.kallsyms])

   7fff810c6841 cpu_startup_entry ([kernel.kallsyms])

   7fff8182df3c rest_init ([kernel.kallsyms])

   7fff81f5f011 start_kernel ([kernel.kallsyms])

   7fff81f5e339 x86_64_start_reservations ([kernel.kallsyms])

   7fff81f5e485 x86_64_start_kernel ([kernel.kallsyms])
```

The meaning of the data can be found in this [perl script](https://github.com/brendangregg/FlameGraph/blob/master/stackcollapse-perf.pl) <br/>
To be specific:

*first line*
```code
swapper     0 [000] 1212828.569239:   10101010 cpu-clock:
```

| Field                    |  Explanation                          |
| -------------------------| :-------------------------------------|
| swapper                  | aaaaaaaaaaaaaaaaaaaaaaaaaaaaa         |
| 0                        | aaaaaaaaaaaaaaaaaaaaaaaaaaaaa         |
| [000]                    | aaaaaaaaaaaaaaaaaaaaaaaaaaaaa         |
| 1212828.569239           | aaaaaaaaaaaaaaaaaaaaaaaaaaaaa         |
| 10101010                 | aaaaaaaaaaaaaaaaaaaaaaaaaaaaa         |
| cpu-clock                | aaaaaaaaaaaaaaaaaaaaaaaaaaaaa         |


### *LEPV UI Chart* ( data visualization )

The charting library for flame graph in LEPV is based on [d3-flame-graph](https://github.com/spiermar/d3-flame-graph)
d3-flame-graph is based on d3 chart library of version 4.10.0, which is pretty new. while LEPV charting is based on
c3 charts, which is in turn based on d3 3.x, so there is version conflict.

As a workaround, we rename the d3 library that d3-flame-graph to d4, and let the d3-flame-chart depend on it.

The chart expects the input data in JSON, structured like this:
```code

{
  "name": "root",
  "value": 57412,
  "children": [
    {
      "name": "genunix`syscall_mstate",
      "value": 89
    },
    {
      "name": "unix`0xfffffffffb800c86",
      "value": 472,
      "children": [
        {
          "name": "genunix`gethrtime_unscaled",
          "value": 4
        }
      ]
    }
  ]
}

```


### *LEPV Python* ( data parsing and transformation )
TODO:
- Figure out the meaning of the fields in 'perf sccipt" output
- Figure out how to do the data transformation for D3 flame chart in Python
- How to get the data for existing perf cpu table? it seems lost with "perf record"...