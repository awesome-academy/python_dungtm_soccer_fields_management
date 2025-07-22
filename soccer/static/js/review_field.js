$(".review-form").each(function() {
  var $stars = $('.star-rating label[data-value]');

  $stars.on('mouseover', function () {
    var n = Number($(this).data('value'));
    $stars.each(function() {
      var $span = $(this).find('span');
      if ($span.length) {
        $span.html(Number($(this).data('value')) <= n ? "&#9733;" : "&#9734;");
      }
    });
  });

  $stars.on('mouseout', function () {
    var $checked = $('.star-rating input:checked');
    var v = $checked.length ? Number($checked.val()) : 5;
    $stars.each(function() {
      var $span = $(this).find('span');
      if ($span.length) {
        $span.html(Number($(this).data('value')) <= v ? "&#9733;" : "&#9734;");
      }
    });
  });

  $stars.on('click', function () {
    var n = $(this).data('value');
    $('#star' + n).prop('checked', true).trigger('change');
  });

  var $checked = $('.star-rating input:checked');
  var v = $checked.length ? Number($checked.val()) : 5;
  $stars.each(function() {
    var $span = $(this).find('span');
    if ($span.length) {
      $span.html(Number($(this).data('value')) <= v ? "&#9733;" : "&#9734;");
    }
  });
});
