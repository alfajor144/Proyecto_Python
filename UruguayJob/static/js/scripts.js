// Empty JS for your own code to be here


$(function () {

   //var pending = new Array();
   // var running = new Array();
    var redButtons = {"btnTwagoPerfiles":0, "btnTwagoOfertas":0, "btnConcursa": 0, "btnBuscojob":0};
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
        if (running.length == 0 && pending.length == 0) {
            redButtons["btnTwagoPerfiles"] = 0;
            redButtons["btnTwagoOfertas"] = 0; 
            redButtons["btnConcursa"] = 0;
            redButtons["btnBuscojob"] = 0;
            await detenerCheckJobs();
            await detenerProgress();
        }else {
            for(var i=0; i < running.length; i++){
               //Busca los que vienen en running y actualiza el array redButtons
               running[i].spider == 'twago-perfiles' ? redButtons['btnTwagoPerfiles'] = 1 : redButtons['btnTwagoPerfiles'] = 0;
               running[i].spider == 'twago-ofertas' ? redButtons['btnTwagoOfertas'] = 1 : redButtons['btnTwagoOfertas'] = 0;
               running[i].spider == 'twago-concursa' ? redButtons['btnConcursa'] = 1 : redButtons['btnConcursa'] = 0;
               running[i].spider == 'twago-uybuscojob' ? redButtons['btnBuscojob'] = 1 : redButtons['btnBuscojob'] = 0;
            }
            for(var i=0; i < pending.length; i++){
               //Busca los que vienen en pending y actualiza el array redButtons
               pending[i].spider == 'twago-perfiles' ? redButtons['btnTwagoPerfiles'] = 1 : redButtons['btnTwagoPerfiles'] = 0;
               pending[i].spider == 'twago-ofertas' ? redButtons['btnTwagoOfertas'] = 1 : redButtons['btnTwagoOfertas'] = 0;
               pending[i].spider == 'twago-concursa' ? redButtons['btnConcursa'] = 1 : redButtons['btnConcursa'] = 0;
               pending[i].spider == 'twago-uybuscojob' ? redButtons['btnBuscojob'] = 1 : redButtons['btnBuscojob'] = 0;
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
                    running[i].spider == "twago-ofertas" ? redButtons["btnTwagoOfertas"] = 1 : redButtons["btnTwagoOfertas"] = 0 ;
                }
                if ( typeof running[i].spider !== 'undefined' ) {//si esta en running lo agrega a la lista de botones en rojo
                    running[i].spider == "twago-perfiles" ? redButtons["btnTwagoPerfiles"] = 1 : redButtons["btnTwagoPerfiles"] = 0 ;
                }
                if ( typeof running[i].spider !== 'undefined' ) {//si esta en running lo agrega a la lista de botones en rojo
                    running[i].spider == "concursa-ofertas" ? redButtons["btnConcursa"] = 1 : redButtons["btnConcursa"] = 0 ;
                }
                if ( typeof running[i].spider !== 'undefined' ) {//si esta en running lo agrega a la lista de botones en rojo
                    running[i].spider == "uybuscojob-ofertas" ? redButtons["btnBuscojob"] = 1 : redButtons["btnBuscojob"] = 0 ;
                }
            }
        }

        // chequea todos los que están en pending
        if(pending.length > 0){
            for(var i = 0; i < pending.length; i++){
                if ( typeof pending[i].spider !== 'undefined' ) {//si esta en pending lo agrega a la lista de botones en rojo
                    pending[i].spider == "twago-ofertas" ? redButtons["btnTwagoOfertas"] = 1 : redButtons["btnTwagoOfertas"] = 0 ;
                }
                if ( typeof pending[i].spider !== 'undefined' ) {//si esta en pending lo agrega a la lista de botones en rojo
                    pending[i].spider == "twago-perfiles" ? redButtons["btnTwagoPerfiles"] = 1 : redButtons["btnTwagoPerfiles"] = 0 ;
                }
                if ( typeof pending[i].spider !== 'undefined' ) {//si esta en pending lo agrega a la lista de botones en rojo
                    pending[i].spider == "concursa-ofertas" ? redButtons["btnConcursa"] = 1 : redButtons["btnConcursa"] = 0 ;
                }
                if ( typeof pending[i].spider !== 'undefined' ) {//si esta en pending lo agrega a la lista de botones en rojo
                    pending[i].spider == "uybuscojob-ofertas" ? redButtons["btnBuscojob"] = 1 : redButtons["btnBuscojob"] = 0 ;
                }
            }
        }

        //lee el array redButtons y cambia los colores de los botones según corresponda
        redButtons['btnTwagoPerfiles'] == 0 ? setButtonBlue(btnTwagoPerfiles) : setButtonRed(btnTwagoPerfiles); 
        redButtons['btnTwagoOfertas'] == 0 ? setButtonBlue(btnTwagoOfertas) : setButtonRed(btnTwagoOfertas); 
        redButtons['btnConcursa'] == 0 ? setButtonBlue(btnConcursa) : setButtonRed(btnConcursa); 
        redButtons['btnBuscojob'] == 0 ? setButtonBlue(btnBuscojob) : setButtonRed(btnBuscojob); 

    }

    //Carga la tabla status
    function updateTableStatus(res) {
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

    function updateTableJobsRunning(res) {
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

    function updateTableJobsPending(res) {
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

    function updateTableJobsFinished(res) {
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
    function getCookie(name) {
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
        var csrftoken = getCookie('csrftoken');
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

    function setButtonIniciando(boton){
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

    function setButtonCancelando(boton){
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

    function setButtonBlue(boton){
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

    function setButtonRed(boton){
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

    function resetButtons(){
        redButtons["btnTwagoPerfiles"] = 0;
        redButtons["btnTwagoOfertas"] = 0; 
        redButtons["btnConcursa"] = 0;
        redButtons["btnBuscojob"] = 0;
        setButtonBlue(btnBuscojob);
        setButtonBlue(btnConcursa);
        setButtonBlue(btnTwagoOfertas);
        setButtonBlue(btnTwagoPerfiles);
    }
    
    async function iniciarCheckProgress() {
        console.log('======= Se inició checkProgress ========')
        progIntervId = setInterval(checkProgress, 2000);
    }

    async function checkProgress() {
        //recorreo los botones que están en rojo
        console.log('======= dentro de checkProgress ========')
        for(var i=0; i > redButtons.length; i++){
            if(redButtons['btnTwagoPerfiles'] === 0){
                 valProgPerfiles = await progressSpider('twago-perfiles');
                console.log(valProgPerfiles);
            }
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
        nIntervId = setInterval(checkJobs, 10000);
    }

    async function checkJobs() {
        let status = await daemonStatus();
        updateTableStatus(status);
        // consulta el estado del servicio
        if (status.status == 'ok') {
            if ( status.running == 0 && status.pending == 0) { //no hay trabajos
                resetButtons();//resetea la lista de botones en rojo 
                await detenerCheckJobs();// detiene el monitoreo del servicio de scrapyd
            }
            else{ //Si hay trabajos consulta la lista y actua en consecuencia
                let jobs = await listJobs();
                //Actualiza las tres tablas
                updateTableJobsRunning(jobs);
                updateTableJobsPending(jobs);
                updateTableJobsFinished(jobs);
                await actualizarBotones(jobs);    
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
        var csrftoken = getCookie('csrftoken');
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
    $('#aStatus').click(function (event) {
        event.preventDefault();
        var statusIsShow = $("#collapse1").hasClass("show");
        if (statusIsShow == false) {
            (async function(){
                let status = await daemonStatus();
                updateTableStatus(status);
            })()
        }
    });

    // actualiza y muestra la tabla de trabajos corriendo
    $('#aJobsRunning').click(function (event) {
        event.preventDefault();
        var jobsRunningIsShow = $("#collapse2").hasClass("show");
        if (jobsRunningIsShow == false) {
            (async function(){
                let jobs = await listJobs();
                updateTableJobsRunning(jobs);
            })()
        }
    });

    // actualiza y muestra la tabla de trabajos pendientes
    $('#aJobsPending').click(function (event) {
        event.preventDefault();
        var jobsPendingIsShow = $("#collapse3").hasClass("show");
        if (jobsPendingIsShow == false) {
            (async function(){
                let jobs = await listJobs();
                updateTableJobsPending(jobs);
            })()
        }
    });

    // actualiza y muestra la tabla de trabajos finalizados
    $('#aJobsFinished').click(function (event) {
        event.preventDefault();
        var jobsFinishedIsShow = $("#collapse4").hasClass("show");
        if (jobsFinishedIsShow == false) {
            (async function(){
                let jobs = await listJobs();
                updateTableJobsFinished(jobs);
            })()
        }
    });


    btnTwagoOfertas.click( async function (event) {
        event.preventDefault();
        var limite = $('#inTwagoOfertas').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if(redButtons['btnTwagoOfertas'] == 0){ // si el array redButtons no tiene activo al este boton
            if(setButtonIniciando($(this))){
                let run = await schedule('twago-ofertas', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    setButtonRed($(this)) === true ? redButtons['btnTwagoOfertas'] = 1 : redButtons['btnTwagoOfertas'] = 0;
                    console.log("se presionó twago-ofertas");
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                }
            }
        }
        else {
            if( setButtonCancelando($(this))){
                let jobs = await listJobs();
                if( jobs.status === 'ok'){
                    let running = jobs.running;//obtiene los trabajos que se están ejecutando
                    let pending = jobs.pending;//obtiene los trabjajos pendientes 
                    for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                        if(running[i].spider == 'twago-ofertas'){
                            let jobId = running[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( setButtonBlue($(this)) ){
                                    redButtons['btnTwagoOfertas'] = 0;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons['btnTwagoOfertas'] = 1;
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
                                if( setButtonBlue($(this)) ){
                                    redButtons['btnTwagoOfertas'] = 0;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons['btnTwagoOfertas'] = 1;
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
        if(redButtons['btnTwagoPerfiles'] == 0){ // si el array redButtons no tiene activo al este boton
            if(setButtonIniciando($(this))){
                let run = await schedule('twago-perfiles', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    setButtonRed($(this)) === true ? redButtons['btnTwagoPerfiles'] = 1 : redButtons['btnTwagoPerfiles'] = 0;
                    console.log("se presionó twago-perfiles");
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                    await iniciarCheckProgress(); //inicia el monitoreo del progreso de descarga
                }
            }
        }
        else {
            if( setButtonCancelando($(this))){
                let jobs = await listJobs();
                if( jobs.status === 'ok'){
                    let running = jobs.running;//obtiene los trabajos que se están ejecutando
                    let pending = jobs.pending;//obtiene los trabjajos pendientes 
                    for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                        if(running[i].spider == 'twago-perfiles'){
                            let jobId = running[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( setButtonBlue($(this)) ){
                                    redButtons['btnTwagoPerfiles'] = 0;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons['btnTwagoPerfiles'] = 1;
                                    console.log("No se pudo poner el boton de twagoPerfiles en azul")
                                }
                            }
                        }
                    }
                    for(var i = 0; i < pending.length; i++){//busca si hay trabajo pendiente perteneciente a esta araña
                        if(pending[i].spider == 'twago-perfiles'){
                            let jobId = pending[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( setButtonBlue($(this)) ){
                                    redButtons['btnTwagoPerfiles'] = 0;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons['btnTwagoPerfiles'] = 1;
                                    console.log("No se pudo poner el boton de twagoPerfiles en azul")
                                }
                            }
                        }
                    }
                }
            }
        }
    });

    btnConcursa.click(function (event) {
        event.preventDefault();
        var limite = $('#inConcursa').val();
        if ($(this).hasClass("btn-primary")) {
            schedule('concursa-ofertas', limite);       //Inicia la araña correspondiente    
            console.log("storage = " + localStorage.getItem("concursa-ofertas"));
            setButtonRed($(this));
            iniciarCheckJobs()            
        }
        else {
            cancelSpider(localStorage.getItem("concursa-ofertas"));
            listJobs()
            console.log("Eliminando twago-ofertas: " + localStorage.getItem("concursa-ofertas"))
            setButtonBlue($(this));
        }
    });


    btnConcursa.click( async function (event) {
        event.preventDefault();
        var limite = $('#inConcursa').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if(redButtons['btnConcursa'] == 0){ // si el array redButtons no tiene activo al este boton
            if(setButtonIniciando($(this))){
                let run = await schedule('concursa-ofertas', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    setButtonRed($(this)) === true ? redButtons['btnConcursa'] = 1 : redButtons['btnConcursa'] = 0;
                    console.log("se presionó concursa-ofertas");
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                }
            }
        }
        else {
            if( setButtonCancelando($(this))){
                let jobs = await listJobs();
                if( jobs.status === 'ok'){
                    let running = jobs.running;//obtiene los trabajos que se están ejecutando
                    let pending = jobs.pending;//obtiene los trabjajos pendientes 
                    for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                        if(running[i].spider == 'concursa-ofertas'){
                            let jobId = running[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( setButtonBlue($(this)) ){
                                    redButtons['btnConcursa'] = 0;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons['btnConcursa'] = 1;
                                    console.log("No se pudo poner el boton de Concursa-ofertas en azul")
                                }
                            }
                        }
                    }
                    for(var i = 0; i < pending.length; i++){//busca si hay trabajo pendiente perteneciente a esta araña
                        if(pending[i].spider == 'concursa-ofertas'){
                            let jobId = pending[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( setButtonBlue($(this)) ){
                                    redButtons['btnConcursa'] = 0;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons['btnConcursa'] = 1;
                                    console.log("No se pudo poner el boton de twagoPerfiles en azul")
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
        if(redButtons['btnBuscojob'] == 0){ // si el array redButtons no tiene activo al este boton
            if(setButtonIniciando($(this))){
                let run = await schedule('uybuscojob-ofertas', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    setButtonRed($(this)) === true ? redButtons['btnBuscojob'] = 1 : redButtons['btnBuscojob'] = 0;
                    console.log("se presionó uybuscojob-ofertas");
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                }
            }
        }
        else {
            if( setButtonCancelando($(this))){
                let jobs = await listJobs();
                if( jobs.status === 'ok'){
                    let running = jobs.running;//obtiene los trabajos que se están ejecutando
                    let pending = jobs.pending;//obtiene los trabjajos pendientes 
                    for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                        if(running[i].spider == 'uybuscojob-ofertas'){
                            let jobId = running[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( setButtonBlue($(this)) ){
                                    redButtons['btnBuscojob'] = 0;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons['btnBuscojob'] = 1;
                                    console.log("No se pudo poner el boton de uybuscojob-ofertas en azul")
                                }
                            }
                        }
                    }
                    for(var i = 0; i < pending.length; i++){//busca si hay trabajo pendiente perteneciente a esta araña
                        if(pending[i].spider == 'uybuscojob-ofertas'){
                            let jobId = pending[i].id;
                            res = await cancelSpider(jobId);
                            if( res.status === 'ok' ){
                                if( setButtonBlue($(this)) ){
                                    redButtons['btnBuscojob'] = 0;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    redButtons['btnBuscojob'] = 1;
                                    console.log("No se pudo poner el boton de btnBuscojob en azul")
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
        console.log(res)
    })
});




