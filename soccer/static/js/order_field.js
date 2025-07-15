$(function() {
  var pricePerHour = parseFloat($('#order-field-root').data('price'));
  var $durationEl = $('[name="duration"]');
  var $voucherEl = $('#voucher-select');
  var $totalPriceEl = $('#total-price');

  function formatMoney(n) {
    return n.toLocaleString('en-US');
  }

  function calcTotalPrice() {
    var duration = parseInt($durationEl.val()) || 0;
    var $selectedOption = $voucherEl.find('option:selected');
    var discountPercent = parseInt($selectedOption.data('discount')) || 0;
    var total = pricePerHour * (duration / 60);
    if (discountPercent > 0) {
      total = total * (1 - discountPercent / 100);
    }
    console.log(total);
    $totalPriceEl.text(formatMoney(Math.round(total)) + ' VND');
  }

  if ($durationEl.length && $voucherEl.length && $totalPriceEl.length) {
    $durationEl.on('change', calcTotalPrice);
    $voucherEl.on('change', calcTotalPrice);
    calcTotalPrice();
  }
});
