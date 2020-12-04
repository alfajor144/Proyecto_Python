// Empty JS for your own code to be here


$(function () {

   //var pending = new Array();
   // var running = new Array();
    var redButtons = {"btnTwagoPerfiles":false , "btnTwagoOfertas": false, "btnConcursa":  false, "btnBuscojob": false};
    var colorButtons = {"btnTwagoPerfiles": 'blue' , "btnTwagoOfertas": 'blue', "btnConcursa": 'blue', "btnBuscojob":'blue'};
    var nIntervId;
    var valProgTwago = 0;
    var valProgPerfiles = 0
    var valProgBuscojob = 0;
    var valProgConcursa = 0;
    var progIntervId;
    var btnTwagoOfertas = $('#btnTwagoOfertas');
    var btnTwagoPerfiles = $('#btnTwagoPerfiles');
    var btnConcursa = $('#btnConcursa');
    var btnBuscojob = $('#btnBuscoJob');
    var btnProgreso = $('#btnProgreso');
    var barTwagoPerfiles = $("#barTwagoPerfiles");

    //Actualiza la lista de botones en rojo
    async function updateListRedButtons(jobs){
        console.log("updateListRedButtons running: "+ jobs.running)
        console.log("updateListRedButtons pending: "+ jobs.pending)
        let running = jobs.running;
        let pending = jobs.pending;
        if ( running.length == 0 ) {
            redButtons.btnTwagoPerfiles = false;
            redButtons.btnTwagoOfertas = false; 
            redButtons.btnConcursa = false;
            redButtons.btnBuscojob = false;
            //await detenerCheckJobs();
            //await detenerProgress();
        }else {
            for(var i=0; i < running.length; i++){
               //Busca los que vienen en running y actualiza el array redButtons
               running[i].spider == 'twago-perfiles' ? redButtons.btnTwagoPerfiles = true : redButtons.btnTwagoPerfiles = false;
               running[i].spider == 'twago-ofertas' ? redButtons.btnTwagoOfertas = true : redButtons.btnTwagoOfertas = false;
               running[i].spider == 'concursa-ofertas' ? redButtons.btnConcursa = true : redButtons.btnConcursa = false;
               running[i].spider == 'uybuscojob-ofertas' ? redButtons.btnBuscojob = true : redButtons.btnBuscojob = false;
            }
            for(var i=0; i < pending.length; i++){
               //Busca los que vienen en pending y actualiza el array redButtons
               running[i].spider == 'twago-perfiles' ? redButtons.btnTwagoPerfiles = true : redButtons.btnTwagoPerfiles = false;
               running[i].spider == 'twago-ofertas' ? redButtons.btnTwagoOfertas = true : redButtons.btnTwagoOfertas = false;
               running[i].spider == 'concursa-ofertas' ? redButtons.btnConcursa = true : redButtons.btnConcursa = false;
               running[i].spider == 'uybuscojob-ofertas' ? redButtons.btnBuscojob = true : redButtons.btnBuscojob = false;
            }
        }
    }

    async function progressSpider(name_spider){
        let result;
        try {
            result = $.ajax({
                method: "GET",
                url: "http://localhost:8000/administrador/progress/ajax",
                data: {'spider': name_spider}
            });
            return result;
        } catch (error) {
            console.error("Error en progressSpider() : " + error);
        }
    }


    async function actualizarBotones(jobs) {
        await updateListRedButtons(jobs);
        let pending = jobs.pending;
        let running = jobs.running;
        // chequea todos los que están running
        if(running.length > 0){
            for(var i = 0; i < running.length; i++){
                if ( typeof running[i].spider !== 'undefined' ) {//si esta en running lo agrega a la lista de botones en rojo
                    running[i].spider == "twago-ofertas" ? redButtons.btnTwagoOfertas = true : redButtons.btnTwagoOfertas = false ;
                }
                if ( typeof running[i].spider !== 'undefined' ) {//si esta en running lo agrega a la lista de botones en rojo
                    running[i].spider == "twago-perfiles" ? redButtons.btnTwagoPerfiles = true : redButtons.btnTwagoPerfiles = false ;
                }
                if ( typeof running[i].spider !== 'undefined' ) {//si esta en running lo agrega a la lista de botones en rojo
                    running[i].spider == "concursa-ofertas" ? redButtons.btnConcursa = true : redButtons.btnConcursa = false ;
                }
                if ( typeof running[i].spider !== 'undefined' ) {//si esta en running lo agrega a la lista de botones en rojo
                    running[i].spider == "uybuscojob-ofertas" ? redButtons.btnBuscojob = true : redButtons.btnBuscojob = false ;
                }
            }
        }

        // chequea todos los que están en pending
        if(pending.length > 0){
            for(var i = 0; i < pending.length; i++){
                if ( typeof pending[i].spider !== 'undefined' ) {//si esta en pending lo agrega a la lista de botones en rojo
                    pending[i].spider == "twago-ofertas" ? redButtons.btnTwagoOfertas = true : redButtons.btnTwagoOfertas = false ;
                }
                if ( typeof pending[i].spider !== 'undefined' ) {//si esta en pending lo agrega a la lista de botones en rojo
                    pending[i].spider == "twago-perfiles" ? redButtons.btnTwagoPerfiles = true : redButtons.btnTwagoPerfiles = false ;
                }
                if ( typeof pending[i].spider !== 'undefined' ) {//si esta en pending lo agrega a la lista de botones en rojo
                    pending[i].spider == "concursa-ofertas" ? redButtons.btnConcursa = true : redButtons.btnConcursa = false ;
                }
                if ( typeof pending[i].spider !== 'undefined' ) {//si esta en pending lo agrega a la lista de botones en rojo
                    pending[i].spider == "uybuscojob-ofertas" ? redButtons.btnBuscojob = true : redButtons.btnBuscojob = false ;
                }
            }
        }

        //lee el array redButtons y cambia los colores de los botones según corresponda
        redButtons.btnTwagoPerfiles === false ? await setButtonBlue(btnTwagoPerfiles) : await setButtonRed(btnTwagoPerfiles); 
        redButtons.btnTwagoOfertas === false ? await setButtonBlue(btnTwagoOfertas) : await setButtonRed(btnTwagoOfertas); 
        redButtons.btnConcursa === false ? await setButtonBlue(btnConcursa) : await setButtonRed(btnConcursa); 
        redButtons.btnBuscojob === false ? await setButtonBlue(btnBuscojob) : await setButtonRed(btnBuscojob); 

    }

    //Carga la tabla status
    async function updateTableStatus(res) {
        var tbody = $("#tbodyStatus");
        tbody.empty();
        var trNode = document.createElement('tr'); //Crea la fila
        var tdStatusNode = document.createElement('td');
        tdStatusNode.textContent = res.status;
        trNode.append(tdStatusNode);
        var tdRunningNode = document.createElement('td');
        tdRunningNode.textContent = res.running;
        trNode.append(tdRunningNode);
        var tdPendingNode = document.createElement('td');
        tdPendingNode.textContent = res.pending;
        trNode.append(tdPendingNode);
        var tdFinishedNode = document.createElement('td');
        tdFinishedNode.textContent = res.finished;
        trNode.append(tdFinishedNode);
        var tdNodeNameNode = document.createElement('td');
        tdNodeNameNode.textContent = res.node_name;
        trNode.append(tdNodeNameNode);
        tbody.append(trNode);
    }

    async function updateTableJobsRunning(res) {
        var tbody = $("#tbodyRunning");
        tbody.empty(); //Vacía la tabla
        running = res.running;
        if (running.length < 1) {
            var trNode = document.createElement('tr'); //Crea la fila
            var tdNroNode = document.createElement('td');
            tdNroNode.textContent = 0;
            trNode.append(tdNroNode);
            var tdIdJobNode = document.createElement('td');
            tdIdJobNode.textContent = " ";
            trNode.append(tdIdJobNode);
            var tdSpiderNode = document.createElement('td');
            tdSpiderNode.textContent = " ";
            trNode.append(tdSpiderNode);
            var tdStartTimeNode = document.createElement('td');
            tdStartTimeNode.textContent = " ";
            trNode.append(tdStartTimeNode);
            tbody.append(trNode);
        } else {
            for (let i = 0; i < running.length; i++) {
                var trNode = document.createElement('tr'); //Crea la fila
                var tdNroNode = document.createElement('td');
                tdNroNode.textContent = i + 1;
                trNode.append(tdNroNode);
                var tdIdJobNode = document.createElement('td');
                tdIdJobNode.textContent = running[i].id;
                trNode.append(tdIdJobNode);
                var tdSpiderNode = document.createElement('td');
                tdSpiderNode.textContent = running[i].spider;
                trNode.append(tdSpiderNode);
                var tdStartTimeNode = document.createElement('td');
                tdStartTimeNode.textContent = running[i].start_time;
                trNode.append(tdStartTimeNode);
                tbody.append(trNode);
            }
        }
    }

    async function updateTableJobsPending(res) {
        var tbody = $("#tbodyPending");
        tbody.empty(); //Vacía la tabla
        pending = res.running;
        if (pending.length < 1) {
            var trNode = document.createElement('tr'); //Crea la fila
            var tdNroNode = document.createElement('td');
            tdNroNode.textContent = 0;
            trNode.append(tdNroNode);
            var tdIdJobNode = document.createElement('td');
            tdIdJobNode.textContent = " ";
            trNode.append(tdIdJobNode);
            var tdSpiderNode = document.createElement('td');
            tdSpiderNode.textContent = " ";
            trNode.append(tdSpiderNode);
            tbody.append(trNode);
        } else {
            for (let i = 0; i < pending.length; i++) {
                var trNode = document.createElement('tr'); //Crea la fila
                var tdNroNode = document.createElement('td');
                tdNroNode.textContent = i + 1;
                trNode.append(tdNroNode);
                var tdIdJobNode = document.createElement('td');
                tdIdJobNode.textContent = pending[i].id;
                trNode.append(tdIdJobNode);
                var tdSpiderNode = document.createElement('td');
                tdSpiderNode.textContent = pending[i].spider;
                trNode.append(tdSpiderNode);
                tbody.append(trNode);
            }
        }
    }

    async function updateTableJobsFinished(res) {
        var tbody = $("#tbodyFinished");
        tbody.empty(); //Vacía la tabla
        finished = res.finished;
        if (finished.length < 1) {
            var trNode = document.createElement('tr'); //Crea la fila
            var tdNroNode = document.createElement('td');
            tdNroNode.textContent = 0;
            trNode.append(tdNroNode);
            var tdIdJobNode = document.createElement('td');
            tdIdJobNode.textContent = " ";
            trNode.append(tdIdJobNode);
            var tdSpiderNode = document.createElement('td');
            tdSpiderNode.textContent = " ";
            trNode.append(tdSpiderNode);
            var tdStartTimeNode = document.createElement('td');
            tdStartTimeNode.textContent = "";
            trNode.append(tdStartTimeNode);
            var tdEndTimeNode = document.createElement('td');
            tdEndTimeNode.textContent = "";
            trNode.append(tdEndTimeNode);
            tbody.append(trNode);
        } else {
            for (let i = 0; i < finished.length; i++) {
                var trNode = document.createElement('tr'); //Crea la fila
                var tdNroNode = document.createElement('td');
                tdNroNode.textContent = i + 1;
                trNode.append(tdNroNode);
                var tdIdJobNode = document.createElement('td');
                tdIdJobNode.textContent = finished[i].id;
                trNode.append(tdIdJobNode);
                var tdSpiderNode = document.createElement('td');
                tdSpiderNode.textContent = finished[i].spider;
                trNode.append(tdSpiderNode);
                var tdStartTimeNode = document.createElement('td');
                tdStartTimeNode.textContent = finished[i].start_time;
                trNode.append(tdStartTimeNode);
                var tdEndTimeNode = document.createElement('td');
                tdEndTimeNode.textContent = finished[i].end_time;
                trNode.append(tdEndTimeNode);
                tbody.append(trNode);
            }
        }
    }

    async function daemonStatus() {
        let result;
        try {
            result = $.ajax({
                method: "GET",
                url: "http://localhost:8000/administrador/daemonstatus",
                data: {}
            });
            return result;
        } catch (error) {
            console.error("Error en daemonStatus: " + error);
        }
    }

    async function listJobs() {
        let result;
        try {
            result = $.ajax({
                method: "GET",
                url: "http://localhost:8000/administrador/listjobs",
                data: {}
            });
            return result;
        } catch (error) {
            console.error('Error en listJobs(): ' + error);    
        }
    }


    /*** Permite obtener el token de django **/
    async function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        //RETORNANDO EL TOKEN
        return cookieValue;
    }//end function getCookie

    async function cancelSpider(id_job) {
        let result;
        var csrftoken = await getCookie('csrftoken');
        try {
            result = $.ajax({
                method: "POST",
                url: "http://localhost:8000/administrador/cancelspider",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    'job': id_job
                },
                dataType: "json"
            });
            return result;            
        } catch (error) {
            console.error("Error en cancelSpider(): " + error);
        }
    }

    async function setButtonIniciando(boton){
        //var boton = $("#idBoton");
        if(boton.hasClass('btn-primary')){
            boton.removeClass("btn-primary");
            boton.addClass("btn-warning");
            boton.text('Iniciando araña ...');
            boton.prop('disabled', true);
            return true;
        }
        return false;
    }

    async function setButtonCancelando(boton){
        //var boton = $("#idBoton");
        if(boton.hasClass("btn-danger")){
            boton.removeClass("btn-danger");
            boton.addClass("btn-warning");
            boton.text('Cancelando  trabajo ...');
            boton.prop('disabled', true);
            return true;
        }    
        return false;
    }

    async function setButtonBlue(boton){
        //var boton = $("#idBoton");
        if(boton.hasClass("btn-warning")){
            boton.removeClass("btn-warning");
            boton.addClass("btn-primary");
            boton.text('Lazar araña');
            boton.prop('disabled', false);
            return true;
        } 
        return false;   
    }

    async function setButtonRed(boton){
        //var boton = $("#"+idBoton);
        if(boton.hasClass("btn-warning")){
            boton.removeClass("btn-warning");
            boton.addClass("btn-danger");
            boton.text("Detener araña");
            boton.prop("disabled", false);
            return true;
        }   
        return false;
    }

    async function resetButtons(){
        redButtons.btnTwagoPerfiles = false;
        redButtons.btnTwagoOfertas = false; 
        redButtons.btnConcursa = false;
        redButtons.btnBuscojob = false;
        await setButtonBlue(btnBuscojob);
        await setButtonBlue(btnConcursa);
        await setButtonBlue(btnTwagoOfertas);
        await setButtonBlue(btnTwagoPerfiles);
    }
    
    async function iniciarCheckProgress() {
        console.log('======= Se inició checkProgress ========')
        progIntervId = setInterval(checkProgress, 2000);
    }

    async function checkProgress() {
        //recorreo los botones que están en rojo
        console.log('======= dentro de checkProgress ========')
            if( redButtons.btnTwagoPerfiles ){
                let res = await progressSpider('twago-perfiles');
                let progress = res["twago-perfiles"] + '%'
                barTwagoPerfiles.text(progress);
                barTwagoPerfiles.width(progress)
                valProgTwago = progress
            }
        /*
         * FALTA CÓDIGO
         */
    }

    //detiene el monitoreo del progreso de las arañas
    async function detenerProgress() {
        console.log('======= dentro de detenerProgress ========')
        clearInterval(progIntervId);
    }

    async function iniciarCheckJobs() {
        nIntervId = setInterval(checkJobs, 5000);
    }

    async function checkJobs() {
        let status = await daemonStatus();
        await updateTableStatus(status);
        // consulta el estado del servicio
        if (status.status == 'ok') {
            let jobs = await listJobs();
            //Actualiza las tres tablas
            await updateTableJobsRunning(jobs);
            await updateTableJobsPending(jobs);
            await updateTableJobsFinished(jobs);
            await actualizarBotones(jobs);    
            console.log("%%%%%%% CheckJobs running:" + jobs.running.length)
            if ( status.running == 0 && status.pending == 0) { //no hay trabajos
                resetButtons();//resetea la lista de botones en rojo 
                await detenerCheckJobs();// detiene el monitoreo del servicio de scrapyd
                await detenerProgress();
            }
        } else {
            alert("No hay comunicación de el servicio Scrapyd")    
        }
    }

    //detiene el monitoreo del servcio
    async function detenerCheckJobs() {
        clearInterval(nIntervId);
    }

    // inicia el trabajo de una araña
    async function schedule(name_spider, limite) {
        var csrftoken = await getCookie('csrftoken');
        let result;
        try {
            result = $.ajax({
                method: "POST",
                url: "http://localhost:8000/administrador/schedule",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    'spider': name_spider,
                    'limite': limite
                },
                dataType: "json"
            });
           return result;
        } catch (error) {
           console.error('Error en schedule(): ' + error); 
        }
    }



    /***************************************************
     * LLamandao inicial
     * *************************************************/
    (async function(){
        await iniciarCheckJobs();
    })()

    // actualiza y muestra la tabla de estado del servicio
    $('#aStatus').click(async function (event) {
        event.preventDefault();
        var statusIsShow = $("#collapse1").hasClass("show");
        if (statusIsShow == false) {
            let status = await daemonStatus();
            await updateTableStatus(status);
        }
    });

    // actualiza y muestra la tabla de trabajos corriendo
    $('#aJobsRunning').click(async function (event) {
        event.preventDefault();
        var jobsRunningIsShow = $("#collapse2").hasClass("show");
        if (jobsRunningIsShow == false) {
            let jobs = await listJobs();
            await updateTableJobsRunning(jobs);
        }
    });

    // actualiza y muestra la tabla de trabajos pendientes
    $('#aJobsPending').click(async function (event) {
        event.preventDefault();
        var jobsPendingIsShow = $("#collapse3").hasClass("show");
        if (jobsPendingIsShow == false) {
            let jobs = await listJobs();
            await updateTableJobsPending(jobs);
        }
    });

    // actualiza y muestra la tabla de trabajos finalizados
    $('#aJobsFinished').click(async function (event) {
        event.preventDefault();
        var jobsFinishedIsShow = $("#collapse4").hasClass("show");
        if (jobsFinishedIsShow == false) {
            let jobs = await listJobs();
            await updateTableJobsFinished(jobs);
        }
    });


    btnTwagoOfertas.click( async function (event) {
        event.preventDefault();
        var limite = $('#inTwagoOfertas').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if( !redButtons.btnTwagoOfertas ){ // si el array redButtons no tiene activo al este boton
            if(await setButtonIniciando($(this))){
                let run = await schedule('twago-ofertas', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    await setButtonRed($(this)) === true ? redButtons.btnTwagoOfertas = true : redButtons.btnTwagoOfertas = false;
                    console.log("se presionó twago-ofertas");
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                }
            }
        }
        else {
            if( await setButtonCancelando($(this))){
                let jobs = await listJobs();
                if( jobs.status === 'ok'){
                    let running = jobs.running;//obtiene los trabajos que se están ejecutando
                    let pending = jobs.pending;//obtiene los trabjajos pendientes 
                    for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                        if(running[i].spider == 'twago-ofertas'){
                            let jobId = running[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( await setButtonBlue($(this)) ){
                                    redButtons.btnTwagoOfertas = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons.btnTwagoOfertas = true;
                                    console.log("No se pudo poner el boton de twagoOfertas en azul")
                                }
                            }
                        }
                    }
                    for(var i = 0; i < pending.length; i++){//busca si hay trabajo pendiente perteneciente a esta araña
                        if(pending[i].spider == 'twago-ofertas'){
                            let jobId = pending[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( await setButtonBlue($(this)) ){
                                    redButtons.btnTwagoOfertas = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons.btnTwagoOfertas = true;
                                    console.log("No se pudo poner el boton de twagoPerfiles en azul")
                                }
                            }
                        }
                    }
                }
            }
        }
    });


    btnTwagoPerfiles.click( async function (event) {
        event.preventDefault();
        var limite = $('#inTwagoPerfiles').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if(!redButtons.btnTwagoPerfiles){ // si el array redButtons no tiene activo al este boton
            if(await setButtonIniciando($(this))){
                let run = await schedule('twago-perfiles', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    await setButtonRed($(this)) === true ? redButtons.btnTwagoPerfiles = true : redButtons.btnTwagoPerfiles = false;
                    console.log("se presionó twago-perfiles");
                    valProgPerfiles = 0
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                    await iniciarCheckProgress(); //inicia el monitoreo del progreso de descarga
                }
            }
        }
        else {
            if( await setButtonCancelando($(this))){
                let jobs = await listJobs();
                if( jobs.status === 'ok'){
                    let running = jobs.running;//obtiene los trabajos que se están ejecutando
                    let pending = jobs.pending;//obtiene los trabjajos pendientes 
                    for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                        if(running[i].spider == 'twago-perfiles'){
                            let jobId = running[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( await setButtonBlue($(this)) ){
                                    redButtons.btnTwagoPerfiles = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons.btnTwagoPerfiles = true;
                                    console.error("No se pudo poner el boton de twagoPerfiles en azul")
                                }
                            }
                        }
                    }
                    for(var i = 0; i < pending.length; i++){//busca si hay trabajo pendiente perteneciente a esta araña
                        if(pending[i].spider == 'twago-perfiles'){
                            let jobId = pending[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( await setButtonBlue($(this)) ){
                                    redButtons.btnTwagoPerfiles = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons.btnTwagoPerfiles = true;
                                    console.error("No se pudo poner el boton de twagoPerfiles en azul")
                                }
                            }
                        }
                    }
                }
            }
        }
    });


    btnConcursa.click( async function (event) {
        event.preventDefault();
        var limite = $('#inConcursa').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if( !redButtons.btnConcursa ){ // si el array redButtons no tiene activo al este boton
            if(await setButtonIniciando($(this))){
                let run = await schedule('concursa-ofertas', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    await setButtonRed($(this)) === true ? redButtons.btnConcursa = true : redButtons.btnConcursa = false;
                    console.log("se presionó concursa-ofertas");
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                }
            }
        }
        else {
            if( await setButtonCancelando($(this))){
                let jobs = await listJobs();
                if( jobs.status === 'ok'){
                    let running = jobs.running;//obtiene los trabajos que se están ejecutando
                    let pending = jobs.pending;//obtiene los trabjajos pendientes 
                    for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                        if(running[i].spider == 'concursa-ofertas'){
                            let jobId = running[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( await setButtonBlue($(this)) ){
                                    redButtons.btnConcursa = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons.btnConcursa = true;
                                    console.error("No se pudo poner el boton de Concursa-ofertas en azul")
                                }
                            }
                        }
                    }
                    for(var i = 0; i < pending.length; i++){//busca si hay trabajo pendiente perteneciente a esta araña
                        if(pending[i].spider == 'concursa-ofertas'){
                            let jobId = pending[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( await setButtonBlue($(this)) ){
                                    redButtons.btnConcursa = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons.btnConcursa = true;
                                    console.error("No se pudo poner el boton de twagoPerfiles en azul")
                                }
                            }
                        }
                    }
                }
            }
        }
    });


    btnBuscojob.click( async function (event) {
        event.preventDefault();
        var limite = $('#inBuscoJob').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if( !redButtons.btnBuscojob ){ // si el array redButtons no tiene activo al este boton
            if(await setButtonIniciando($(this))){
                let run = await schedule('uybuscojob-ofertas', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    await setButtonRed($(this)) === true ? redButtons.btnBuscojob = true : redButtons.btnBuscojob = false;
                    console.log("se presionó uybuscojob-ofertas");
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                }
            }
        }
        else {
            if( await setButtonCancelando($(this))){
                let jobs = await listJobs();
                if( jobs.status === 'ok'){
                    let running = jobs.running;//obtiene los trabajos que se están ejecutando
                    let pending = jobs.pending;//obtiene los trabjajos pendientes 
                    for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                        if(running[i].spider == 'uybuscojob-ofertas'){
                            let jobId = running[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( await setButtonBlue($(this)) ){
                                    redButtons.btnBuscojob = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons.btnBuscojob = true;
                                    console.error("No se pudo poner el boton de uybuscojob-ofertas en azul")
                                }
                            }
                        }
                    }
                    for(var i = 0; i < pending.length; i++){//busca si hay trabajo pendiente perteneciente a esta araña
                        if(pending[i].spider == 'uybuscojob-ofertas'){
                            let jobId = pending[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( await setButtonBlue($(this)) ){
                                    redButtons.btnBuscojob = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons.btnBuscojob = true;
                                    console.error("No se pudo poner el boton de btnBuscojob en azul")
                                }
                            }
                        }
                    }
                }
            }
        }
    });



    btnProgreso.click(async function(event){
        event.preventDefault();
        console.log("estas en progress")
        let res = await progressSpider('twago-perfiles');
        let progress = res["twago-perfiles"] + '%'
        barTwagoPerfiles.text(progress);
        barTwagoPerfiles.width(progress)
    })
});




