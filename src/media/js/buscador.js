/* Script para el buscador de disponibilidad
 */
$(function(){
  $("#id_fecha_llegada").datepicker({
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

    $("#id_fecha_salida").datepicker({
        showOn: 'button',
        buttonImage: MEDIA_URL+'img/calendar.gif',
        maxDate: '+12M',
        buttonImageOnly: true,
        dateFormat: 'dd/mm/yy',
        defaultDate: +2
        });

   var MAX_NINS = 4;
      $('#id_habitaciones').change(function(){
          var selected = $("#id_habitaciones option:selected");
          var num_habitaciones = parseInt(selected.text());
          /* Ocultamos las habitaciones */
          for (distri=num_habitaciones+1; distri<4; distri++) {
            $('#id_adultos_d'+distri).val("1");
            for (j=1; j<4; j++) {
                $('#id_edad_nin'+j+"_d"+distri).val("0");
              }
             $('#id_nins_d'+distri).val("0");
             $('#distri_'+distri).hide();
             $('#edad_nin_d'+distri).hide();
           }
          for (i=1; i<=num_habitaciones; i++){
            $(' #distri_'+i).show();
          }
          });

        function update_child_distribution(selected) {
           var id = selected[0].id;
            var distri = id.split('_')[2];
            var num_nins = parseInt(selected.val());
            if (num_nins > 0) {
              $('#edad_nin_'+distri).show();
              // Mostramos los selectores
              for (i=1; i<=num_nins; i++) {
                $('#id_edad_nin'+i+"_"+distri).show();
              }
              // ocultamos el resto
              for (i=num_nins+1; i<MAX_NINS; i++) {
                 var control ="#id_edad_nin"+i+"_"+distri;
                 $(control).val("0");
                 $(control).hide();
              }
            } else {
              $('#edad_nin_'+distri).hide()
              for (i=1; i<MAX_NINS; i++) {
                 var control ="#id_edad_nin"+i+"_d"+distri;
                 $(control).val("0");
                 $(control).hide();
              }
           } 
        }
        $('.nins').change(function(){
            var selected = $(this);
            update_child_distribution(selected);
        });
        /* establecemos la visualizacion inicial */
        var actual = $('#id_nins_d1')
        update_child_distribution(actual);
  });

