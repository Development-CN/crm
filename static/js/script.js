    var calendar;
    var Calendar = FullCalendar.Calendar;
    var events = [];
    $(function() {
        if (!!scheds) {
            var fechaActual = new Date();
            Object.keys(scheds).map(k => {
                var row = scheds[k]
                console.log("fechaActual")
                console.log(fechaActual)
                console.log(fechaEvento)
                console.log(row.start_datetime)
                var partesFecha = row.start_datetime.split(' ')[0].split('-');
                var partesHora = row.start_datetime.split(' ')[1].split(':');
                var year = parseInt(partesFecha[0]);
                var month = parseInt(partesFecha[1]) - 1; // Restar 1 ya que en JavaScript los meses van de 0 a 11
                var day = parseInt(partesFecha[2]);
                var hour = parseInt(partesHora[0]);
                var minute = parseInt(partesHora[1]);
                
                // Crear un objeto Date con las partes obtenidas
                var fechaEvento = new Date(year, month, day, hour, minute);
                if (row.cumplido == "Si"){
                    var color = "green";
                }
                else if (fechaEvento < fechaActual){
                    var color = "red";
                }
                else {
                    var color = "primary";
                }
                events.push({ id: row.id, title: row.title, start: row.start_datetime, end: row.end_datetime, color: color});
            })
        }
        var date = new Date()
        var d = date.getDate(),
            m = date.getMonth(),
            y = date.getFullYear()

        calendar = new Calendar(document.getElementById('calendar'), {
            initialView: 'dayGridMonth',
            locale: 'es', //Idioma Español FullCalendar
            headerToolbar: {
                left: 'prev,next today',
                right: 'dayGridMonth,dayGridWeek,list',
                center: 'title',
            },
            selectable: true,
            themeSystem: 'bootstrap',
            //Eventos predeterminados aleatorios
            events: events,
            eventClick: function(info) {
                var _details = $('#event-details-modal')
                var id = info.event.id
                if (!!scheds[id]) {
                    _details.find('#id_evento').text(scheds[id].id_evento)
                    _details.find('#title').text(scheds[id].title)
                    _details.find('#cliente').text(scheds[id].cliente)
                    _details.find('#asesor').text(scheds[id].asesor)
                    _details.find('#telefono').text(scheds[id].telefono)
                    _details.find('#tipo_evento').text(scheds[id].tipo_evento)
                    _details.find('#estado').text(scheds[id].estado)
                    _details.find('#cumplido').text(scheds[id].cumplido)
                    _details.find('#fecha_hora_cumplido').text(scheds[id].fecha_hora_cumplido)
                    _details.find('#tiempo_evento').text(scheds[id].tiempo_evento)
                    _details.find('#description').text(scheds[id].description)
                    _details.find('#start').text(scheds[id].sdate)
                    _details.find('#end').text(scheds[id].edate)
                    _details.find('#edit,#delete').attr('data-id', id)
                    _details.modal('show')
                    if (scheds[id].cumplido == "Si"){
                        document.getElementById("fechahoracumplido").hidden = false;
                        document.getElementById("fecha_hora_cumplido").hidden = false;
                        document.getElementById("btn_cumplir_evento").hidden = true;
                        document.getElementById("btn_editar_evento").hidden = true;
                        document.getElementById("btn_eliminar_evento").hidden = true;
                    }
                    else {
                        document.getElementById("fechahoracumplido").hidden = true;
                        document.getElementById("fecha_hora_cumplido").hidden = true;
                        document.getElementById("btn_cumplir_evento").hidden = false;
                        document.getElementById("btn_editar_evento").hidden = false;
                        document.getElementById("btn_eliminar_evento").hidden = false;
                    }
                } else {
                    alert("Event is undefined");
                }
            },
            eventDidMount: function(info) {
                // Hacer algo después de los eventos montados
            },
            editable: true
        });

        calendar.render();

        // listener de restablecimiento de formulario
        $('#schedule-form').on('reset', function() {
            $(this).find('input:hidden').val('')
            $(this).find('input:visible').first().focus()
        })

        // Botón Editar
        $('#edit').click(function() {
            var id = $(this).attr('data-id')
            if (!!scheds[id]) {
                var _form = $('#schedule-form')
                console.log(String(scheds[id].start_datetime), String(scheds[id].start_datetime).replace(" ", "\\t"))
                _form.find('[name="id"]').val(id)
                _form.find('[name="title"]').val(scheds[id].title)
                _form.find('[name="description"]').val(scheds[id].description)
                _form.find('[name="start_datetime"]').val(String(scheds[id].start_datetime).replace(" ", "T"))
                _form.find('[name="end_datetime"]').val(String(scheds[id].end_datetime).replace(" ", "T"))
                $('#event-details-modal').modal('hide')
                _form.find('[name="title"]').focus()
            } else {
                alert("Event is undefined");
            }
        })

        // Botón Eliminar / Eliminación de un evento
        $('#delete').click(function() {
            var id = $(this).attr('data-id')
            if (!!scheds[id]) {
                var _conf = confirm("¿Estás segura de eliminar este evento programado?");
                if (_conf === true) {
                    location.href = "./delete_schedule.php?id=" + id;
                }
            } else {
                alert("Event is undefined");
            }
        })
    })