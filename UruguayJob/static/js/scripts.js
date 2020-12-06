// Empty JS for your own code to be here


$(function () {

    var colorButtons = {"btnPerfiles": 'blue' , "btnTwago": 'blue', "btnConcursa": 'blue', "btnBuscojob":'blue'};
    var nIntervId;
    var valProgTwago = 0;
    var valProgPerfiles = 0
    var valProgBuscojob = 0;
    var valProgConcursa = 0;
    var progIntervId;
    var monitorProgres = false;
    var monitorJobs = false;
    var btnTwago = $('#btnTwago');
    var btnPerfiles = $('#btnPerfiles');
    var btnConcursa = $('#btnConcursa');
    var btnBuscojob = $('#btnBuscoJob');
    var barraPerfiles = $("#barraPerfiles");
    var barraTwago = $("#barraTwago");
    var barraConcursa = $("#barraConcursa")
    var barraBuscojob = $("#barraBuscojob");

//    //Actualiza la lista de botones en rojo
//    async function updateColorButtons(jobs){
//        console.log("updateColorButtons running: "+ jobs.running)
//        console.log("updateColorButtons pending: "+ jobs.pending)
//        let running = jobs.running;
//        let pending = jobs.pending;
//        if ( running.length == 0 ) {
//            colorButtons.btnPerfiles = 'blue';
//            colorButtons.btnTwago = 'blue'; 
//            colorButtons.btnConcursa = 'blue';
//            colorButtons.btnBuscojob = 'blue';
//            //await detenerCheckJobs();
//            //await detenerProgress();
//        }else {
//            for(var i=0; i < running.length; i++){
//               //Busca los que vienen en running y actualiza el array colorButtons
//               running[i].spider == 'twago-perfiles' ? colorButtons.btnPerfiles = 'red' : colorButtons.btnPerfiles = '';
//               running[i].spider == 'twago-ofertas' ? colorButtons.btnTwago = 'red' : colorButtons.btnTwago = false;
//               running[i].spider == 'concursa-ofertas' ? colorButtons.btnConcursa = 'red' : colorButtons.btnConcursa = false;
//               running[i].spider == 'uybuscojob-ofertas' ? colorButtons.btnBuscojob = 'red' : colorButtons.btnBuscojob = false;
//            }
//            for(var i=0; i < pending.length; i++){
//               //Busca los que vienen en pending y actualiza el array colorButtons
//               running[i].spider == 'twago-perfiles' ? colorButtons.btnPerfiles = true : colorButtons.btnPerfiles = false;
//               running[i].spider == 'twago-ofertas' ? colorButtons.btnTwago = true : colorButtons.btnTwago = false;
//               running[i].spider == 'concursa-ofertas' ? colorButtons.btnConcursa = true : colorButtons.btnConcursa = false;
//               running[i].spider == 'uybuscojob-ofertas' ? colorButtons.btnBuscojob = true : colorButtons.btnBuscojob = false;
//            }
//        }
//    }

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
        //await updateColorButtons(jobs);
        let pending = jobs.pending;
        let running = jobs.running;
        // chequea todos los que están running
        console.log("dentro de actualizar botones. pending: " + pending.length + ", running: " + running.length);
        if(running.length > 0){
            for(var i = 0; i < running.length; i++){
                if ( typeof running[i].spider !== 'undefined' ) { //
                    if( running[i].spider == "twago-ofertas" ){ //si twago-perfiles está en running lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnTwago) ){ //cabia a rojo el boton btnTwago
                            colorButtons.btnTwago = 'red';
                        }else{
                            colorButtons.btnTwago = 'blue';
                        }
                    }

                    if( running[i].spider == "twago-perfiles" ){ //si twago-perfiles está en running lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnPerfiles) ){ //cabia a rojo el boton btnPerfiles
                            colorButtons.btnPerfiles = 'red';
                        }else{
                            colorButtons.btnPerfiles = 'blue';
                        }
                    }
                    if( running[i].spider == "concursa-ofertas" ){ //si concursa-ofertas está en running lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnConcursa) ){ //cabia a rojo el boton btnConcursa
                            colorButtons.btnConcursa = 'red';
                        }else{
                            colorButtons.btnConcursa = 'blue';
                        }
                    }
                    if( running[i].spider == "uybuscojob-ofertas" ){ //si uybuscojob-ofertas está en running lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnBuscojob) ){ //cabia a rojo el boton btnBuscojob
                            colorButtons.btnBuscojob = 'red';
                        }else{
                            colorButtons.btnBuscojob = 'blue';
                        }
                    }
                    if( running[i].spider == "twago-ofertas" ){ //si twago-perfiles está en running lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnTwago) ){ //cabia a rojo el boton btnTwago
                            colorButtons.btnTwago = 'red';
                        }else{
                            colorButtons.btnTwago = 'blue';
                        }
                    }
                }
            }
        }


        // chequea todos los que están pending
        if(pending.length > 0){
            for(var i = 0; i < pending.length; i++){
                if ( typeof pending[i].spider !== 'undefined' ) { //
                    if( pending[i].spider == "twago-ofertas" ){ //si twago-perfiles está en pending lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnTwago) ){ //cabia a rojo el boton btnTwago
                            colorButtons.btnTwago = 'red';
                        }else{
                            colorButtons.btnTwago = 'blue';
                        }
                    }

                    if( pending[i].spider == "twago-perfiles" ){ //si twago-perfiles está en pending lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnPerfiles) ){ //cabia a rojo el boton btnPerfiles
                            colorButtons.btnPerfiles = 'red';
                        }else{
                            colorButtons.btnPerfiles = 'blue';
                        }
                    }
                    if( pending[i].spider == "concursa-ofertas" ){ //si concursa-ofertas está en pending lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnConcursa) ){ //cabia a rojo el boton btnConcursa
                            colorButtons.btnConcursa = 'red';
                        }else{
                            colorButtons.btnConcursa = 'blue';
                        }
                    }
                    if( pending[i].spider == "uybuscojob-ofertas" ){ //si uybuscojob-ofertas está en pending lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnBuscojob) ){ //cabia a rojo el boton btnBuscojob
                            colorButtons.btnBuscojob = 'red';
                        }else{
                            colorButtons.btnBuscojob = 'blue';
                        }
                    }
                    if( pending[i].spider == "twago-ofertas" ){ //si twago-perfiles está en pending lo agrega a la lista de botones en rojo
                        if( setButtonRed(btnTwago) ){ //cabia a rojo el boton btnTwago
                            colorButtons.btnTwago = 'red';
                        }else{
                            colorButtons.btnTwago = 'blue';
                        }
                    }
                }
            }
        }

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
        if(boton.hasClass("btn-warning")){
            boton.text("Iniciando la araña ...");
            return true;
        }else{
            if( boton.hasClass("btn-danger") ) boton.removeClass("btn-danger");
            if( boton.hasClass("btn-primary") ) boton.removeClass("btn-primary"); 
            boton.addClass("btn-warning");
            boton.text("Iniciando la araña ...");
            boton.prop("disabled", true);
            if(boton.attr('id') === 'btnPerfiles'){
                colorButtons.btnPerfiles = 'yellow';
                return true;
            }else if( boton.attr('id') === 'btnTwago' ){
                colorButtons.btnTwago = 'yellow';
                return true;
            }else if( boton.attr('id') === 'btnConcursa' ){
                colorButtons.btnConcursa = 'yellow';
                return true;
            }else if( boton.attr('id') === 'btnBuscojob' ){
                colorButtons.btnBuscojob = 'yellow';
                return true;
            }
            return false;
        }
    }

    async function setButtonCancelando(boton){
        if(boton.hasClass("btn-warning")){
            return true;
        }else{
            if( boton.hasClass("btn-danger") ) boton.removeClass("btn-danger");
            if( boton.hasClass("btn-primary") ) boton.removeClass("btn-primary"); 
            boton.addClass("btn-warning");
            boton.text("Parando araña");
            boton.prop("disabled", true);
            if(boton.attr('id') === 'btnPerfiles'){
                colorButtons.btnPerfiles = 'yellow';
                return true;
            }else if( boton.attr('id') === 'btnTwago' ){
                colorButtons.btnTwago = 'yellow';
                return true;
            }else if( boton.attr('id') === 'btnConcursa' ){
                colorButtons.btnConcursa = 'yellow';
                return true;
            }else if( boton.attr('id') === 'btnBuscojob' ){
                colorButtons.btnBuscojob = 'yellow';
                return true;
            }
            return false;
        }  
    }

    async function setButtonBlue(boton){
        if(boton.hasClass("btn-primary")){
            boton.text("Lanzar araña");
            return true;
        }else{
            if( boton.hasClass("btn-danger") ) boton.removeClass("btn-danger");
            if( boton.hasClass("btn-warning") ) boton.removeClass("btn-warning"); 
            boton.addClass("btn-primary");
            boton.text("Lanzar araña");
            boton.prop("disabled", false);
            if(boton.attr('id') === 'btnPerfiles'){
                colorButtons.btnPerfiles = 'blue';
                return true;
            }else if( boton.attr('id') === 'btnTwago' ){
                colorButtons.btnTwago = 'blue';
                return true;
            }else if( boton.attr('id') === 'btnConcursa' ){
                colorButtons.btnConcursa = 'blue';
                return true;
            }else if( boton.attr('id') === 'btnBuscojob' ){
                colorButtons.btnBuscojob = 'blue';
                return true;
            }
            return false;
        }  
    }

    async function setButtonRed(boton){
        if(boton.hasClass("btn-danger")){
            boton.text("Detener araña");
            return true;
        }else{
            if( boton.hasClass("btn-primary") ) boton.removeClass("btn-primary");
            if( boton.hasClass("btn-warning") ) boton.removeClass("btn-warning"); 
            boton.addClass("btn-danger");
            boton.text("Detener araña");
            boton.prop("disabled", false);
            if(boton.attr('id') === 'btnPerfiles'){
                colorButtons.btnPerfiles = 'red';
                return true;
            }else if( boton.attr('id') === 'btnTwago' ){
                colorButtons.btnTwago = 'red';
                return true;
            }else if( boton.attr('id') === 'btnConcursa' ){
                colorButtons.btnConcursa = 'red';
                return true;
            }else if( boton.attr('id') === 'btnBuscojob' ){
                colorButtons.btnBuscojob = 'red';
                return true;
            }
            return false;
        }  
    }

    async function resetButtons(){
        colorButtons.btnPerfiles = 'blue';
        colorButtons.btnTwago = 'blue'; 
        colorButtons.btnConcursa = 'blue';
        colorButtons.btnBuscojob = 'blue';
        resetBuscojob = await setButtonBlue(btnBuscojob);
        if( !resetBuscojob ){
            console.error("no se pudo resetear buscojob")
        }
        resetConcursa = await setButtonBlue(btnConcursa);
        if( !resetConcursa ){
            console.error("no se pudo resetear Concursa")
        }
        resetTwago = await setButtonBlue(btnTwago);
        if( !resetTwago ){
            console.error("no se pudo resetear Twago")
        }
        resetPerfiles = await setButtonBlue(btnPerfiles);
        if( !resetPerfiles ){
            console.error("no se pudo resetear Perfiles")
        }
    }
    
    async function iniciarCheckProgress() {
        console.log('======= Se inició checkProgress ========')
        if( monitorProgres === false ){
            progIntervId = setInterval(checkProgress, 2000);
            monitorProgres = true;
        }   
    }

    async function setBarraProgress(barraProgress, porcentaje){
        let texto = porcentaje + '%';
        if( porcentaje < 101 ){
            barraProgress.text(texto);
            barraProgress.width(texto);
        }
    }

    async function checkProgress() {
        // si perfiles está en rojo actuliza su barra
        if( colorButtons.btnPerfiles === 'red' ){
            let res = await progressSpider('twago-perfiles');
            let progress = res["twago-perfiles"];
            console.info("progress: " + progress)
            if(valProgPerfiles < progress ){
                valProgPerfiles = progress
            }
            setBarraProgress(barraPerfiles, valProgPerfiles);
        }
    }

    //detiene el monitoreo del progreso de las arañas
    async function detenerProgress() {
        //console.log('======= dentro de detenerProgress ========')
        clearInterval(progIntervId);
        monitorProgres = false;
    }

    async function iniciarCheckJobs() {
        if( monitorJobs === false){
            monitorJobs = true;
            nIntervId = setInterval(checkJobs, 5000);
        }
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
            await actualizarBotones(jobs); //actuliza la lista de colores y cambia los botones al color que corresponda
            //console.log("%%%%%%% CheckJobs running:" + jobs.running.length)
            if ( status.running == 0 && status.pending == 0) { //no hay trabajos
                await resetButtons();//resetea la lista de botones en rojo 
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
        monitorJobs = false;        
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

    async function deleteJobs(name_spider){
        haveJobs = true;
        var countJobs = 0;
        var jobs;
        while(haveJobs === true){
            jobs = [];
            jobs = await listJobs();// consulta los trabajos 
            if( jobs.status == 'ok'){
                let running = jobs.running;//obtiene los trabajos que se están ejecutando
                let pending = jobs.pending;

                for(var i = 0; i < pending.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                    if(pending[i].spider == name_spider){ //Si corriendo uno de esta araña lo manda a detener
                        let jobId = pending[i].id;        //obtiene el id
                        res = await cancelSpider(jobId);
                        //console.log("se mando a cancelar el id: " + jobId);
                        if( res.status === 'ok' ){
                            console.log('Eliminado con exito (pending), jobId: ' + jobId)
                        }else{
                            console.error('error al itentar eliminar (pending), jobid: ' + jobid)
                            return false;
                        }
                    }
                }

                for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
                    if(running[i].spider == name_spider){ //Si corriendo uno de esta araña lo manda a detener
                        let jobId = running[i].id;        //obtiene el id
                        res = await cancelSpider(jobId);
                        //console.log("se mando a cancelar el id: " + jobId);
                        if( res.status === 'ok' ){
                            console.log('Eliminado con exito (running), jobId: ' + jobId)
                        }else{
                            console.error('Error al itentar eliminar (running), jobId: ' + jobId)
                            return false;
                        }
                    }
                }
                
                /*Cosulta nuevamente y chequea que no que denden trabajos pendientes*/
                jobs = await listJobs();
                running = jobs.running;
                pending = jobs.pending;
                for(var i=0; i < running.length; i ++){
                    if(running[i].spider == name_spider)  countJobs ++;
                }
                for(var i=0; i < pending.length; i ++){
                    if(pending[i].spider == name_spider)  countJobs ++;
                }
                if(countJobs !== 0 ) haveJobs = false;
            }
        }
        actualizarBotones(jobs);
        return true;
    }


    btnTwago.click( async function (event) {
        event.preventDefault();
        var limite = $('#inTwagoOfertas').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if( !colorButtons.btnTwago ){ // si el array colorButtons no tiene activo al este boton
            if(await setButtonIniciando($(this))){
                let run = await schedule('twago-ofertas', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    await setButtonRed($(this)) === true ? colorButtons.btnTwago = true : colorButtons.btnTwago = false;
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
                                    colorButtons.btnTwago = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    colorButtons.btnTwago = true;
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
                                    colorButtons.btnTwago = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    colorButtons.btnTwago = true;
                                    console.log("No se pudo poner el boton de twagoPerfiles en azul")
                                }
                            }
                        }
                    }
                }
            }
        }
    });


    btnPerfiles.click( async function (event) {
        event.preventDefault();
        console.log("presionaste Perfiles 1: " + colorButtons.btnPerfiles)
        var limite = $('#inTwagoPerfiles').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if(colorButtons.btnPerfiles == 'blue'){ // si el el boton está habilitado 
            if(await setButtonIniciando($(this))){ //deshabilita el boton, lo pasa a amarillo con el mensaje inicar
                console.log("presionaste Perfiles 2")
                let run = await schedule('twago-perfiles', limite);   //Inicia la araña correspondiente    
                if(run.status == 'ok'){ //si la araña inicio correctamente
                    await setButtonRed($(this)) === true ? colorButtons.btnPerfiles = 'red' : colorButtons.btnPerfiles = 'blue';
                    console.log("presionaste Perfiles 3")
                    valProgPerfiles = 0
                    setBarraProgress(barraPerfiles, 0); //retea la barra de progreso
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                    await iniciarCheckProgress(); //inicia el monitoreo del progreso de descarga
                }
            }
        }
        else if(colorButtons.btnPerfiles == 'red') {
            if( await setButtonCancelando($(this)) ){ // deshabilita el boton y lo coloca en amarillo
                let borrarTrabajos = await deleteJobs('twago-perfiles')
                if(borrarTrabajos){
                    setButtonBlue($(this));
                }
                /*
                 *
                 */
            }
        }
    });


    btnConcursa.click( async function (event) {
        event.preventDefault();
        var limite = $('#inConcursa').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        if( !colorButtons.btnConcursa ){ // si el array colorButtons no tiene activo al este boton
            if(await setButtonIniciando($(this))){
                let run = await schedule('concursa-ofertas', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    await setButtonRed($(this)) === true ? colorButtons.btnConcursa = true : colorButtons.btnConcursa = false;
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
                                    colorButtons.btnConcursa = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    colorButtons.btnConcursa = true;
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
                                    colorButtons.btnConcursa = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    colorButtons.btnConcursa = true;
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
        if( !colorButtons.btnBuscojob ){ // si el array colorButtons no tiene activo al este boton
            if(await setButtonIniciando($(this))){
                let run = await schedule('uybuscojob-ofertas', limite);       //Inicia la araña correspondiente    
                if(run.status === 'ok'){ //si la araña inicio correctamente
                    await setButtonRed($(this)) === true ? colorButtons.btnBuscojob = true : colorButtons.btnBuscojob = false;
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
                                    colorButtons.btnBuscojob = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    colorButtons.btnBuscojob = true;
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
                                    colorButtons.btnBuscojob = false;
                                    alert("Se ha cancelado el trabajo id: " + jobId);
                                }else{
                                    colorButtons.btnBuscojob = true;
                                    console.error("No se pudo poner el boton de btnBuscojob en azul")
                                }
                            }
                        }
                    }
                }
            }
        }
    });



});




