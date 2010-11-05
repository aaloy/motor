/* Script para el buscador de disponibilidad
 */
$(function(){
  $("#id_fecha_inicio").datepicker({
        showOn: 'button', 
        buttonImage: MEDIA_URL+'img/calendar.gif',
        buttonImageOnly: true, dateFormat: 'dd/mm/yy',
        minDate: +1,
        maxDate: '+11M',
        defaultDate: +1,
        onSelect: function(dateText, inst){
            min_date = $.datepicker.parseDate('dd/mm/yy', dateText);
            min_date.setDate(min_date.getDate()+1);
            $("#id_fecha_salida").datepicker('option', 'minDate', min_date);
            $("#id_fecha_salida").datepicker('setDate', min_date);
        }
    });

   $("#id_fecha").datepicker({
        showOn: 'button', 
        buttonImage: MEDIA_URL+'img/calendar.gif',
        buttonImageOnly: true, dateFormat: 'dd/mm/yy',
        minDate: +1,
        maxDate: '+11M',
        defaultDate: +1,
        onSelect: function(dateText, inst){
            min_date = $.datepicker.parseDate('dd/mm/yy', dateText);
            min_date.setDate(min_date.getDate()+1);
            $("#id_fecha_salida").datepicker('option', 'minDate', min_date);
            $("#id_fecha_salida").datepicker('setDate', min_date);
        }
    });

   $("#id_fecha_fin").datepicker({
        showOn: 'button',
        buttonImage: MEDIA_URL+'img/calendar.gif',
        maxDate: '+12M',
        buttonImageOnly: true,
        dateFormat: 'dd/mm/yy',
        defaultDate: +365
        });

  });

