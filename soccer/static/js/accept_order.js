$(document).ready(function() {
  $('#btn-accept-order').on('click', function() {
    var acceptUrl = $(this).data('accept-url');
    $.ajax({
      url: acceptUrl,
      type: 'POST',
      headers: {
        'X-CSRFToken': window.CSRF_TOKEN,
        'X-Requested-With': 'XMLHttpRequest'
      },
      success: function(data) {
        if (data.success) {
          location.reload();
        } else {
          alert(data.error || "Accept failed!");
        }
      },
      error: function(xhr, status, error) {
        alert("Accept failed! " + (xhr.responseText || ""));
      }
    });
  });
});
