
$(function () {

    var jobs;
    var status;
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
    var btnBuscojob = $('#btnBuscojob');
    var barraPerfiles = $("#barraPerfiles");
    var barraTwago = $("#barraTwago");
    var barraConcursa = $("#barraConcursa")
    var barraBuscojob = $("#barraBuscojob");
    var txtProgPerfiles = $("#txtProgPerfiles");
    var txtProgTwago = $("#txtProgTwago");
    var txtProgConcursa = $("#txtProgConcursa");
    var txtProgBuscojob = $("#txtProgBuscojob");
    var bandera = 'verde';


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


    async function actualizarBotones() {
        //await updateColorButtons(jobs);
        if( monitorJobs === false || bandera == 'rojo'){
            jobs = await listJobs();
        }
        let pending = jobs.pending;
        let running = jobs.running;
        // chequea todos los que están running
        //debugger;
        if( typeof running !== 'undefined'){
            for(var i = 0; i < running.length; i++){
                if( running[i].spider === "twago-ofertas" ){ //si twago-perfiles está en running lo agrega a la lista de botones en rojo
                    if( await setButtonRed(btnTwago) ){ //cambia a rojo el boton btnTwago
                        colorButtons.btnTwago = 'red';
                    }else{
                        colorButtons.btnTwago = 'blue';
                    }
                }

                if( running[i].spider === "twago-perfiles" ){ //si twago-perfiles está en running lo agrega a la lista de botones en rojo
                    if( await setButtonRed(btnPerfiles) ){ //cambia a rojo el boton btnPerfiles
                        colorButtons.btnPerfiles = 'red';
                    }else{

                        colorButtons.btnPerfiles = 'blue';
                    }
                }
                if( running[i].spider === "concursa-ofertas" ){ //si concursa-ofertas está en running lo agrega a la lista de botones en rojo
                    if( await setButtonRed(btnConcursa) ){ //cambia a rojo el boton btnConcursa
                        colorButtons.btnConcursa = 'red';
                    }else{
                        colorButtons.btnConcursa = 'blue';
                    }
                }
                if( running[i].spider === "uybuscojob-ofertas" ){ //si uybuscojob-ofertas está en running lo agrega a la lista de botones en rojo
                    if( await setButtonRed(btnBuscojob) ){ //cambia a rojo el boton btnBuscojob
                        colorButtons.btnBuscojob = 'red';
                    }else{
                        colorButtons.btnBuscojob = 'blue';
                    }
                }
                if( running[i].spider == "twago-ofertas" ){ //si twago-perfiles está en running lo agrega a la lista de botones en rojo
                    if( await setButtonRed(btnTwago) ){ //cabia a rojo el boton btnTwago
                        colorButtons.btnTwago = 'red';
                    }else{
                        colorButtons.btnTwago = 'blue';
                    }
                }
            }
        }


        // chequea todos los que están pending
        if( typeof pending !== 'undefined' ){
            if(pending.length > 0){
                for(var i = 0; i < pending.length; i++){
                    if( pending[i].spider == "twago-ofertas" ){ //si twago-perfiles está en pending lo agrega a la lista de botones en rojo
                        if( await setButtonRed(btnTwago) ){ //cabia a rojo el boton btnTwago
                            colorButtons.btnTwago = 'red';
                        }else{
                            colorButtons.btnTwago = 'blue';
                        }
                    }

                    if( pending[i].spider == "twago-perfiles" ){ //si twago-perfiles está en pending lo agrega a la lista de botones en rojo
                        if( await setButtonRed(btnPerfiles) ){ //cabia a rojo el boton btnPerfiles
                            colorButtons.btnPerfiles = 'red';
                        }else{
                            colorButtons.btnPerfiles = 'blue';
                        }
                    }
                    if( pending[i].spider == "concursa-ofertas" ){ //si concursa-ofertas está en pending lo agrega a la lista de botones en rojo
                        if( await setButtonRed(btnConcursa) ){ //cabia a rojo el boton btnConcursa
                            colorButtons.btnConcursa = 'red';
                        }else{
                            colorButtons.btnConcursa = 'blue';
                        }
                    }
                    if( pending[i].spider == "uybuscojob-ofertas" ){ //si uybuscojob-ofertas está en pending lo agrega a la lista de botones en rojo
                        if( await setButtonRed(btnBuscojob) ){ //cabia a rojo el boton btnBuscojob
                            colorButtons.btnBuscojob = 'red';
                        }else{
                            colorButtons.btnBuscojob = 'blue';
                        }
                    }
                    if( pending[i].spider == "twago-ofertas" ){ //si twago-perfiles está en pending lo agrega a la lista de botones en rojo
                        if( await setButtonRed(btnTwago) ){ //cabia a rojo el boton btnTwago
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

    async function updateTableJobsRunning() {
        var tbody = $("#tbodyRunning");
        tbody.empty(); //Vacía la tabla
        //debugger
        let running = await jobs.running;
        if( typeof running !== 'undefined' ){
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
    }

    async function updateTableJobsPending() {
        var tbody = $("#tbodyPending");
        tbody.empty(); //Vacía la tabla
        let pending = await jobs.pending;
        if( typeof pending !== 'undefined' ){
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
    }

    async function updateTableJobsFinished() {
        var tbody = $("#tbodyFinished");
        tbody.empty(); //Vacía la tabla
        let finished = await jobs.finished;
        if( typeof finished !== 'undefined' ){
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
        //debugger;
        resetBuscojob = await setButtonBlue( $(btnBuscojob) );
        if( !resetBuscojob ){
            console.error("no se pudo resetear buscojob")
        }
        resetConcursa = await setButtonBlue($(btnConcursa));
        if( !resetConcursa ){
            console.error("no se pudo resetear Concursa")
        }
        resetTwago = await setButtonBlue($(btnTwago));
        if( !resetTwago ){
            console.error("no se pudo resetear Twago")
        }
        resetPerfiles = await setButtonBlue($(btnPerfiles));
        if( !resetPerfiles ){
            console.error("no se pudo resetear Perfiles")
        }
    }
    
    async function iniciarCheckProgress() {
        //console.log('======= Se inició checkProgress ========')
        if( monitorProgres === false ){
            progIntervId = setInterval(checkProgress, 2000);
            monitorProgres = true;
        }   
    }

    async function setTextCancel(barraProgress){
        let texto = "";
        if( barraProgress.attr("id") === 'barraPerfiles'  ){
            porcentaje = valProgPerfiles;
            valProgPerfiles = 0;
            if(porcentaje < 100 ){
                texto = "Descarga cancelada en " + porcentaje +"% ";
                txtProgPerfiles.text( texto )
                if( txtProgPerfiles.hasClass("text-primary") ) txtProgPerfiles.removeClass("text-primary");
                txtProgPerfiles.addClass("text-danger");
            }
        } 

        return true;
    }

    async function setTextoProgress(barraProgress, porcentaje){
        let texto = "";
        if( porcentaje < 1 ) texto = "";
        if( barraProgress.attr("id") === 'barraPerfiles'  ){
            if(porcentaje < 100 && colorButtons.btnPerfiles == 'red'){
                texto = "Descargando perfiles desde www.twago.es. Estado de la descarga " + porcentaje +"%, aguarde por favor.";
                txtProgPerfiles.text( texto )
                if( txtProgPerfiles.hasClass("text-success") ) txtProgPerfiles.removeClass("text-success");
                if( txtProgPerfiles.hasClass("text-danger") ) txtProgPerfiles.removeClass("text-danger");
                txtProgPerfiles.addClass("text-primary");
            } 
            if(porcentaje >= 100 ){// Si la descarga se completa correctamente
                texto = "La descarga se ha completado con éxito.";
                txtProgPerfiles.text( texto )
                if( txtProgPerfiles.hasClass("text-primary") ) txtProgPerfiles.removeClass("text-primary");
                if( txtProgPerfiles.hasClass("text-danger") ) txtProgPerfiles.removeClass("text-danger");
                txtProgPerfiles.addClass("text-success");
            } 
        }
        if( barraProgress.attr("id") === 'barraTwago'  ){
            if(porcentaje < 100 && colorButtons.btnTwago == 'red'){
                texto = "Descargando ofertas desde www.twago.es. Estado de la descarga " + porcentaje +"%, aguarde por favor.";
                txtProgTwago.text( texto )
                if( txtProgTwago.hasClass("text-success") ) txtProgTwago.removeClass("text-success");
                if( txtProgTwago.hasClass("text-danger") ) txtProgTwago.removeClass("text-danger");
                txtProgTwago.addClass("text-primary");
            } 
            if(porcentaje >= 100 ){// Si la descarga se completa correctamente
                texto = "La descarga se ha completado con éxito.";
                txtProgTwago.text( texto )
                if( txtProgTwago.hasClass("text-primary") ) txtProgTwago.removeClass("text-primary");
                if( txtProgTwago.hasClass("text-danger") ) txtProgTwago.removeClass("text-danger");
                txtProgTwago.addClass("text-success");
            } 
        }
        if( barraProgress.attr("id") === 'barraConcursa'  ){
            if(porcentaje < 100 && colorButtons.btnConcursa == 'red'){
                texto = "Descargando ofertas desde www.uruguayconcursa.gub.uy. Estado de la descarga " + porcentaje +"%, aguarde por favor.";
                txtProgConcursa.text( texto )
                if( txtProgConcursa.hasClass("text-success") ) txtProgConcursa.removeClass("text-success");
                if( txtProgConcursa.hasClass("text-danger") ) txtProgConcursa.removeClass("text-danger");
                txtProgConcursa.addClass("text-primary");
            } 
            if(porcentaje >= 100 ){// Si la descarga se completa correctamente
                texto = "La descarga se ha completado con éxito.";
                txtProgConcursa.text( texto )
                if( txtProgConcursa.hasClass("text-primary") ) txtProgConcursa.removeClass("text-primary");
                if( txtProgConcursa.hasClass("text-danger") ) txtProgConcursa.removeClass("text-danger");
                txtProgConcursa.addClass("text-success");
            } 
        }
        if( barraProgress.attr("id") === 'barraBuscojob'  ){
            if(porcentaje < 100 && colorButtons.btnBuscojob == 'red'){
                texto = "Descargando ofertas desde www.buscojobs.com.uy. Estado de la descarga " + porcentaje +"%, aguarde por favor.";
                txtProgBuscojob.text( texto )
                if( txtProgBuscojob.hasClass("text-success") ) txtProgBuscojob.removeClass("text-success");
                if( txtProgBuscojob.hasClass("text-danger") ) txtProgBuscojob.removeClass("text-danger");
                txtProgBuscojob.addClass("text-primary");
            } 
            if(porcentaje >= 100 ){// Si la descarga se completa correctamente
                texto = "La descarga se ha completado con éxito.";
                txtProgBuscojob.text( texto )
                if( txtProgBuscojob.hasClass("text-primary") ) txtProgBuscojob.removeClass("text-primary");
                if( txtProgBuscojob.hasClass("text-danger") ) txtProgBuscojob.removeClass("text-danger");
                txtProgBuscojob.addClass("text-success");
            } 
        }
    }


    //pinta en la barra que le passen el porcentaje recibido
    async function setBarraProgress(barraProgress, porcentaje, cancel){
        let texto = porcentaje + '%';
        barraProgress.text(texto);
        barraProgress.width(texto);
        if(porcentaje < 100 && cancel === false ){
            if( barraProgress.hasClass("bg-success") ) barraProgress.removeClass("bg-success"); //si esta en verd le quita la clase bg-success
            if( barraProgress.hasClass("bg-danger") ) barraProgress.removeClass("bg-danger"); //si esta en rojo le quita la clase bg-danger
            barraProgress.addClass("bg-primary");//la cambia a azul agregando la clase bg-primary
            barraProgress.addClass("progress-bar-animated");//agrega la animación a la barra
            setTextoProgress(barraProgress, porcentaje);
        }else if( porcentaje >= 100 && cancel === false ){
            if( barraProgress.hasClass("bg-danger") ) barraProgress.removeClass("bg-danger"); //si esta en rojo le quita la clase bg-danger
            if( barraProgress.hasClass("bg-primary") ) barraProgress.removeClass("bg-primary"); //si esta en azul le quita la clase bg-primary
            if( barraProgress.hasClass("progress-bar-animated") ) barraProgress.removeClass("progress-bar-animated");//quita la animación
            barraProgress.addClass("bg-success");//la cambia a verde agregando la clase bg-success
            setTextoProgress(barraProgress, porcentaje);
        }else if( cancel === true ){
            if( barraProgress.hasClass("bg-primary") ) barraProgress.removeClass("bg-primary"); //si esta en azul le quita la clase bg-primary
            if( barraProgress.hasClass("bg-success") ) barraProgress.removeClass("bg-success"); //si esta en verd le quita la clase bg-success
            if( barraProgress.hasClass("progress-bar-animated") ) barraProgress.removeClass("progress-bar-animated");//quita la animación
            barraProgress.addClass("bg-danger");//la cambia a rojo agregando la clase bg-danger
        }
    }

    async function checkProgress() {
        // si perfiles está en rojo actualiza su barra
        if( colorButtons.btnPerfiles === 'red' ){
            let res = await progressSpider('twago-perfiles');
            let progress = res["twago-perfiles"];
            //console.info("progress: " + progress)
            if(valProgPerfiles < progress ){
                valProgPerfiles = progress
            }
            setBarraProgress(barraPerfiles, valProgPerfiles, false);
        }
        // si twago ofertas está en rojo actualiza su barra
        else if( colorButtons.btnTwago === 'red' ){
            let res = await progressSpider('twago-ofertas');
            let progress = res["twago-ofertas"];
            //console.info("progress: " + progress)
            if(valProgTwago < progress ){
                valProgTwago = progress
            }
            setBarraProgress(barraTwago, valProgTwago, false);
        }
        // si concursa ofertas está en rojo actualiza su barra
        else if( colorButtons.btnConcursa === 'red' ){
            let res = await progressSpider('concursa-ofertas');
            let progress = res["concursa-ofertas"];
            //console.info("progress: " + progress)
            if(valProgConcursa < progress ){
                valProgConcursa = progress
            }
            setBarraProgress(barraConcursa, valProgConcursa, false);
        }
        // si buscojob ofertas está en rojo actualiza su barra
        else if( colorButtons.btnBuscojob === 'red' ){
            let res = await progressSpider('uybuscojob-ofertas');
            let progress = res["uybuscojob-ofertas"];
            //console.info("progress: " + progress)
            if(valProgBuscojob < progress ){
                valProgBuscojob = progress
            }
            setBarraProgress(barraBuscojob, valProgBuscojob, false);
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
            jobs = await listJobs();
            nIntervId = setInterval(checkJobs, 5000);
        }
    }

    async function checkJobs() {
        if( bandera == 'verde' ){
            status = await daemonStatus();
            await updateTableStatus(status);
            // consulta el estado del servicio
            if (status.status === 'ok') {
                jobs = await listJobs();
                //Actualiza las tres tablas
                await updateTableJobsRunning();
                await updateTableJobsPending();
                await updateTableJobsFinished();
                await actualizarBotones(); //actualiza la lista de colores y cambia los botones al color que corresponda
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
            jobs = await listJobs();
            await updateTableJobsRunning();
        }
    });

    // actualiza y muestra la tabla de trabajos pendientes
    $('#aJobsPending').click(async function (event) {
        event.preventDefault();
        var jobsPendingIsShow = $("#collapse3").hasClass("show");
        if (jobsPendingIsShow == false) {
            jobs = await listJobs();
            await updateTableJobsPending();
        }
    });

    // actualiza y muestra la tabla de trabajos finalizados
    $('#aJobsFinished').click(async function (event) {
        event.preventDefault();
        var jobsFinishedIsShow = $("#collapse4").hasClass("show");
        if (jobsFinishedIsShow == false) {
            jobs = await listJobs();
            await updateTableJobsFinished();
        }
    });

    async function deleteJobs(name_spider){
        haveJobs = true;
        //var countJobs = 0;
        //var jobs;
        while(haveJobs === true){
            //jobs = [];
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
                            console.log('Eliminando (pending), jobId: ' + jobId)
                        }else{
                            console.error('Error eliminar (pending), jobid: ' + jobid)
                            return false;
                        }
                    }
                }

                for(var i = 0; i < running.length; i++){//busca si trabajo corriendo perteneciente a esta araña
        //debugger
                    if(running[i].spider == name_spider){ //Si corriendo uno de esta araña lo manda a detener
                        let jobId = running[i].id;        //obtiene el id
                        res = await cancelSpider(jobId);
                        //console.log("se mando a cancelar el id: " + jobId);
                        if( res.status === 'ok' ){
                            console.log('Eliminando (running), jobId: ' + jobId)
                        }else{
                            console.error('Error eliminar (running), jobId: ' + jobId)
                            return false;
                        }
                    }
                }
                
                /*Cosulta nuevamente y chequea que no quedenden trabajos pendientes*/
                jobs = await listJobs();
                running = jobs.running;
                pending = jobs.pending;
                //debugger
                if( running.length > 0 ){
                    for(var i=0; i < running.length; i ++){
                        if(running[i].spider === name_spider){
                            haveJobs = true
                        }else{
                            haveJobs = false;
                        }
                    }
                }else{ 
                    haveJobs = false
                }
                if( pending.length === 0 && haveJobs === false){
                    return true;
                }
                if( pending.length > 0 ){ 
                    for(var i=0; i < pending.length; i ++){
                        if(pending[i].spider !== name_spider && haveJobs === false){
                            haveJobs = true;
                        }else{
                            haveJobs = false;
                        }
                    }
                }
            }
        }
        return true;
    }


    btnTwago.click( async function (event) {
        event.preventDefault();
        var limite = $('#inTwagoOfertas').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        bandera = 'rojo'
        if(colorButtons.btnTwago == 'blue'){ // si el el boton está habilitado 
            if(await setButtonIniciando($(this))){ //deshabilita el boton, lo pasa a amarillo con el mensaje inicar
                let run = await schedule('twago-ofertas', limite);   //Inicia la araña correspondiente    
                if(run.status == 'ok'){ //si la araña inicio correctamente
                    console.log("Iniando jobId: "+ run.jobid);
                    await actualizarBotones();
                    valProgTwago = 0
                    setBarraProgress(barraTwago, 0, false); //resetea la barra de progreso
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                    await iniciarCheckProgress(); //inicia el monitoreo del progreso de descarga
                }else{
                    alert("Error al iniciar la araña.");
                    bandera = 'verde';
                    await actualizarBotones();
                }
            }
        }
        else if(colorButtons.btnTwago == 'red') {
            //debugger;
            if( await setButtonCancelando($(this)) ){ // deshabilita el boton y lo coloca en amarillo
                let borrarTrabajos = await deleteJobs('twago-ofertas')
                if(borrarTrabajos){
                    await actualizarBotones();
                    valProgTwago < 101 ? porcentaje = valProgTwago : porcentaje = 100;
                    setBarraProgress(barraTwago, porcentaje, true);
                    setTextCancel(barraTwago);
                }
            }
        }
        bandera = 'verde';
    });


    btnPerfiles.click( async function (event) {
        event.preventDefault();
        var limite = $('#inTwagoPerfiles').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        bandera = 'rojo'
        if(colorButtons.btnPerfiles == 'blue'){ // si el el boton está habilitado 
            if(await setButtonIniciando($(this))){ //deshabilita el boton, lo pasa a amarillo con el mensaje inicar
                let run = await schedule('twago-perfiles', limite);   //Inicia la araña correspondiente    
                if(run.status == 'ok'){ //si la araña inicio correctamente
                    console.log("Iniando jobId: "+ run.jobid);
                    await actualizarBotones();
                    //debugger;
                    valProgPerfiles = 0;
                    setBarraProgress(barraPerfiles, 0, false); //resetea la barra de progreso
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                    await iniciarCheckProgress(); //inicia el monitoreo del progreso de descarga
                }else{
                    alert("Error al iniciar la araña.");
                    bandera = 'verde';
                    await actualizarBotones();
                }
            }
        }
        else if(colorButtons.btnPerfiles == 'red') {
            //debugger;
            if( await setButtonCancelando($(this)) ){ // deshabilita el boton y lo coloca en amarillo
                let borrarTrabajos = await deleteJobs('twago-perfiles')
                if(borrarTrabajos){
                    await actualizarBotones();
                    //debugger
                    valProgPerfiles < 101 ? porcentaje = valProgPerfiles : porcentaje = 100;
                    setBarraProgress(barraPerfiles, porcentaje, true);
                    setTextCancel(barraPerfiles);
                }
            }
        }
        bandera = 'verde';
    });


    btnConcursa.click( async function (event) {
        event.preventDefault();
        var limite = $('#inConcursa').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        bandera = 'rojo'
        if(colorButtons.btnConcursa == 'blue'){ // si el el boton está habilitado 
            if(await setButtonIniciando($(this))){ //deshabilita el boton, lo pasa a amarillo con el mensaje inicar
                let run = await schedule('concursa-ofertas', limite);   //Inicia la araña correspondiente    
                if(run.status == 'ok'){ //si la araña inicio correctamente
                    console.log("Iniando jobId: "+ run.jobid);
                    await actualizarBotones();
                    valProgConcursa = 0
                    setBarraProgress(barraConcursa, 0, false); //resetea la barra de progreso
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                    await iniciarCheckProgress(); //inicia el monitoreo del progreso de descarga
                }else{
                    alert("Error al iniciar la araña.");
                    bandera = 'verde';
                    await actualizarBotones();
                }
            }
        }
        else if(colorButtons.btnConcursa == 'red') {
            //debugger;
            if( await setButtonCancelando($(this)) ){ // deshabilita el boton y lo coloca en amarillo
                let borrarTrabajos = await deleteJobs('concursa-ofertas')
                if(borrarTrabajos){
                    await actualizarBotones();
                    valProgConcursa < 101 ? porcentaje = valProgConcursa : porcentaje = 100;
                    setBarraProgress(barraConcursa, porcentaje, true);
                    setTextCancel(barraConcursa);
                }
            }
        }
        bandera = 'verde';
    });


    btnBuscojob.click( async function (event) {
        event.preventDefault();
        var limite = $('#inBuscoJob').val(); //toma el limite de elementos a raspar desde el cuadro de texto
        bandera = 'rojo'
        if(colorButtons.btnBuscojob == 'blue'){ // si el el boton está habilitado 
            if(await setButtonIniciando($(this))){ //deshabilita el boton, lo pasa a amarillo con el mensaje inicar
                let run = await schedule('uybuscojob-ofertas', limite);   //Inicia la araña correspondiente    
                if(run.status == 'ok'){ //si la araña inicio correctamente
                    console.log("Iniciando jobId: "+ run.jobid);
                    await actualizarBotones();
                    valProgBuscojob = 0
                    setBarraProgress(barraBuscojob, 0, false); //resetea la barra de progreso
                    await iniciarCheckJobs(); //inicia el monitoreo del estado del servor
                    await iniciarCheckProgress(); //inicia el monitoreo del progreso de descarga
                }else{
                    alert("Error al iniciar la araña.");
                    bandera = 'verde';
                    await actualizarBotones();
                }
            }
        }
        else if(colorButtons.btnBuscojob == 'red') {
            //debugger;
            if( await setButtonCancelando($(this)) ){ // deshabilita el boton y lo coloca en amarillo
                let borrarTrabajos = await deleteJobs('uybuscojob-ofertas')
                if(borrarTrabajos){
                    await actualizarBotones();
                    valProgBuscojob < 101 ? porcentaje = valProgBuscojob : porcentaje = 100;
                    setBarraProgress(barraBuscojob, porcentaje, true);
                    setTextCancel(barraBuscojob);
                }
            }
        }
        bandera = 'verde';
    });



});




