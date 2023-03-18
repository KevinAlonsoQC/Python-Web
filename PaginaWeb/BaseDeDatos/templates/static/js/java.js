var alertax = document.getElementById('alerta1')

function alert2(message, type, campo) {

  var wrapper = document.createElement('div')
  wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert"><b>' + message + '</b><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'

  campo.append(wrapper)
}

if (alertax) {

  alert2('¡Registrate para obtener beneficios asombrosos!', 'success', alertax)
}
else{
  alert2('¡Registrate para obtener beneficios asombrosos!', 'success', alertax)
}

function toggleInputState(el){
  var i = $('#input1');
  i.prop('disabled', !$(el).is(':checked'));
}

function noCierre(){
  $('.d-menu').on('click', function (e) {
    e.stopPropagation();
  });

  $('.dropdown-toggle').on('click', function (e) {
    e.stopPropagation();
  });
}

$(function() {
  $('.d-menu').on('click', function (e) {
    e.stopPropagation();
  });
});

$(document).ready(function() {

  $("#cargar").click(function() {
      $.get("https://api.gael.cloud/general/public/clima",
          function(data) {
              $("#temp").val(data[1].Estacion)
          });
  });


  $("#enviar").click(function() {
      $.get("https://api.gael.cloud/general/public/clima",
          function(data) {
              $.each(data, function(i, item) {
                  $("#clima").append("<tr><td>" + item.Estacion +
                      "</td><td>" + item.Temp +
                      "</td><td>" + item.Estado + "</td></tr>");
              });
          });
  });
})