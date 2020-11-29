// Empty JS for your own code to be here


$(function () {

   //var pending = new Array();
   // var running = new Array();
    var redButtons = {"btnTwagoPerfiles":0, "btnTwagoOfertas":0, "btnConcursa": 0, "btnBuscojob":0};
    var nIntervId;
    var btnTwagoOfertas = $('#btnTwagoOfertas');
    var btnTwagoPerfiles = $('#btnTwagoPerfiles');
    var btnConcursa = $('#btnConcursa');
    var btnBuscojob = $('#btnBuscojob');

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

    async function actualizarBotones(jobs) {
        await updateListRedButtons(jobs);
        let pending = jobs.pending;
        let running = jobs.running;
        // chequea todos los que están running
        if(running.length > 0){
            for(var i = 0; 1 < running.length; i++){
                if (running[i].spider == "twago-ofertas") {//si esta en running lo agrega a la lista de botones en rojo           
                    redButtons["btnTwagoPerfiles"] = 1;
                }
                else {
                    redButtons["btnTwagoPerfiles"] = 0;
                }
                if (running[i].spider == "btnTwagoOfertas") {//si esta en running lo agrega a la lista de botones en rojo           
                    redButtons["btnTwagoOfertas"] = 1;
                }
                else {
                    redButtons["btnTwagoOfertas"] = 0;
                }
                if (running[i].spider == "btnConcursa") {//si esta en running lo agrega a la lista de botones en rojo           
                    redButtons["btnConcursa"] = 1;
                }
                else {
                    redButtons["btnConcursa"] = 0;
                }
                if (running[i].spider == "btnBuscojob") {//si esta en running lo agrega a la lista de botones en rojo           
                    redButtons["btnBuscojob"] = 1;
                }
                else {
                    redButtons["btnTwagoOfertas"] = 0;
                }
            }
        }
        // chequea todos los que están en pending
        if(pending.length > 0){
            for(var i = 0; 1 < pending.length; i++){
                if (pending[i].spider == "twago-ofertas") {//si esta en pending lo agrega a la lista de botones en rojo           
                    redButtons["btnTwagoPerfiles"] = 1;
                }
                else {
                    redButtons["btnTwagoPerfiles"] = 0;
                }
                if (pending[i].spider == "btnTwagoOfertas") {//si esta en pending lo agrega a la lista de botones en rojo           
                    redButtons["btnTwagoOfertas"] = 1;
                }
                else {
                    redButtons["btnTwagoOfertas"] = 0;
                }
                if (pending[i].spider == "btnConcursa") {//si esta en pending lo agrega a la lista de botones en rojo           
                    redButtons["btnConcursa"] = 1;
                }
                else {
                    redButtons["btnConcursa"] = 0;
                }
                if (pending[i].spider == "btnBuscojob") {//si esta en pending lo agrega a la lista de botones en rojo           
                    redButtons["btnBuscojob"] = 1;
                }
                else {
                    redButtons["btnTwagoOfertas"] = 0;
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

	// async function getStatus(){
	// 	try{
    //         let response = await fetch('http://localhost:8000/administrador/daemonstatus')
    //         let res = await response.json()
    //         return res
	// 	}
    //     catch (err) {
    //         console.log("Error en getStatus => ", err)
    //     }	
    // }    

    function listJobs() {
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

    // async function getJobs(){
	// 	try{
    //         let response = await fetch('http://localhost:8000/administrador/listjobs')
    //         let jobs = await response.json()
    //         return jobs
	// 	}
    //     catch (err) {
    //         console.log("Error => ", err)
    //     }	
    // }    

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
        }    
    }

    function setButtonCancelando(boton){
        //var boton = $("#idBoton");
        if(boton.hasClass('btn-danger')){
            boton.removeClass("btn-danger");
            boton.addClass("btn-warning");
            boton.text('Cancelando  trabajo ...');
            boton.prop('disabled', true);
        }    
    }
    function setButtonBlue(boton){
        //var boton = $("#idBoton");
        if(boton.hasClass('btn-warning')){
            boton.removeClass("btn-warning");
            boton.addClass("btn-primary");
            boton.text('Lazar araña');
            boton.prop('disabled', false);
        }    
    }

    function setButtonRed(boton){
        //var boton = $("#"+idBoton);
        if(boton.hasClass('btn-warning')){
            boton.removeClass("btn-warning");
            boton.addClass("btn-danger");
            boton.text("Detener araña");
            boton.prop("disabled", false);
        }   
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



    btnTwagoOfertas.click(function (event) {
        event.preventDefault();
        var limite = $('#inTwagoOfertas').val();
        if ($(this).hasClass("btn-primary")) {
            (async function(){

                await schedule('twago-ofertas', limite);       //Inicia la araña correspondiente    
            })()
            setButtonRed($(this));
            iniciarCheckJobs()            
        }
        else {
            cancelSpider(localStorage.getItem("twago-ofertas"));
            listJobs()
            console.log("Eliminando twago-ofertas: " + localStorage.getItem("twago-ofertas"))
            setButtonBlue( $(this) );
        }
    });

    btnTwagoPerfiles.click(function (event) {
        event.preventDefault();
        var limite = $('#inTwagoPerfiles').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if(redButtons['btnTwagoPerfiles'] == 0){ // si el array redButtons no tiene activo al este boton
            (async function(){
                setButtonIniciando($(this));
                //$(this).prop("disabled", true);
                let run = await schedule('twago-perfiles', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    setButtonRed($(this)); //cambia el color del boton a rojo
                    redButtons['btnTwagoPerfiles'] = 1;
                    //let jobs = await listJobs(); //consulta sulta 
                    //updateTableJobsRunning(jobs);
                    console.log("se presionó twago-perfiles");
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                }
            })()
        }
        else {
            (async function(){ 
                setButtonCancelando($(this));                            
                let jobs = await listJobs();
                if( jobs.status === 'ok'){
                    let running = jobs.running;//obtiene los trabajos que se están ejecutando
                    let pending = jobs.pending;//obtiene los trabjajos pendientes 
                    for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                        if(running[i].spider == 'twago-perfiles'){
                            let jobId = running[i].id;
                            res = await cancelSpider(jobId);
                            alert("Se canceló el proceso con el id: "+ jobId);
                            setButtonBlue($(this));
                        }
                    }
                }
            })()
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

    btnBuscojob.click(function (event) {
        event.preventDefault();
        var limite = $('#inBuscoJob').val();
        if ($(this).hasClass("btn-primary")) {
            schedule('uybuscojob-ofertas', limite);       //Inicia la araña correspondiente    
            console.log("storage = " + localStorage.getItem("uybuscojob-ofertas"));
            setButtonRed($(this));
            iniciarCheckJobs()
        }
        else {
            cancelSpider(localStorage.getItem("uybuscojob-ofertas"));
            listJobs()
            console.log("Eliminando uybuscojob-ofertas: " + localStorage.getItem("uybuscojob-ofertas"))
            setButtonBlue($(this));
        }
    });

});




