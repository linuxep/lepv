/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

function getCpuCoreCount(server) {

    // hard code for demo

    if ('www.linuxxueyuan.com' == server) {
        return 2;
    }
    
    if ('www.linuxep.com' == server) {
        return 1;
    }
    
    return 1;

    //var coreCount = 1;
    //var url = "/capacity/cpu/" + server;
    //
    //var getMethod = $.get(url, function(data, status) {
    //    coreCount = data['coresCount'];
    //});
    //
    //getMethod.done( function() {
    //        return coreCount;
    //    }
    //)
}

function getMemoryTotal(server) {

    // hard code for demo

    if ('www.linuxxueyuan.com' == server) {
        return 992;
    }

    if ('www.linuxep.com' == server) {
        return 993;
    }

    return 1000;

    //var url = "/capacity/cpu/" + server;
    //
    //$.get(url, function(data, status) {
    //    coreCount = data['coresCount'];
    //    return coreCount;
    //});
}
