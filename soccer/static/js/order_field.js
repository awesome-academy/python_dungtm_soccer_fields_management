$(function() {
  const pricePerHour = parseFloat($('#order-field-root').data('price'));
  const $durationEl = $('[name="duration"]');
  const $voucherEl = $('#voucher-select');
  const $totalPriceEl = $('#total-price');
  const $voucherDetail = $('#voucher-detail');
  const $voucherFields = {
    description: $('#voucher-description'),
    discount: $('#voucher-discount'),
    validFrom: $('#voucher-validfrom'),
    validTo: $('#voucher-validto'),
    minPrice: $('#voucher-minprice'),
    maxDiscount: $('#voucher-maxdiscount'),
    rest: $('#voucher-rest')
  };
  
  function formatMoney(amount) {
    return amount.toLocaleString('en-US');
  }
  
  function calculateTotalPrice() {
    const duration = parseInt($durationEl.val()) || 0;
    const $selectedOption = $voucherEl.find('option:selected');
    const discountPercent = parseInt($selectedOption.data('discount')) || 0;
    const minPrice = parseFloat($selectedOption.data('minprice')) || 0;
    const maxDiscountAmount = parseFloat($selectedOption.data('maxdiscount')) || 0;
    
    let basePrice = pricePerHour * (duration / 60);
    let discountAmount = 0;
    let finalPrice = basePrice;
    
    const isVoucherSelected = $selectedOption.val() !== '';
    const meetsMinPrice = basePrice >= minPrice;
    
    if (isVoucherSelected && discountPercent > 0 && meetsMinPrice) {
      discountAmount = basePrice * (discountPercent / 100);
      
      if (maxDiscountAmount > 0 && discountAmount > maxDiscountAmount) {
        discountAmount = maxDiscountAmount;
      }
      
      finalPrice = basePrice - discountAmount;
    }
    
    const $priceElement = $totalPriceEl;
    $priceElement.fadeOut(200, function() {
      $(this).text(formatMoney(Math.round(finalPrice)) + ' VND').fadeIn(200);
    });
    
    if (discountAmount > 0) {
      $priceElement.addClass('text-success');
    } else {
      $priceElement.removeClass('text-success');
    }
  }
  
  function updateVoucherDetails() {
    const $selectedOption = $voucherEl.find('option:selected');
    
    if ($selectedOption.val()) {
      $voucherFields.description.text($selectedOption.data('description') || '-');
      $voucherFields.discount.text($selectedOption.data('discount'));
      $voucherFields.validFrom.text($selectedOption.data('validfrom'));
      $voucherFields.validTo.text($selectedOption.data('validto'));
      $voucherFields.minPrice.text(formatMoney($selectedOption.data('minprice')) + ' VND');
      $voucherFields.maxDiscount.text(formatMoney($selectedOption.data('maxdiscount')) + ' VND');
      $voucherFields.rest.text($selectedOption.data('rest'));
      
      $voucherDetail.removeClass('hidden').hide().slideDown(300);
    } else {
      $voucherDetail.slideUp(300, function() {
        $(this).addClass('hidden');
      });
    }
  }
  
  if ($durationEl.length && $voucherEl.length && $totalPriceEl.length) {
    $durationEl.on('change', calculateTotalPrice);
    
    $voucherEl.on('change', function() {
      updateVoucherDetails();
      calculateTotalPrice();
    });
    
    updateVoucherDetails();
    calculateTotalPrice();
  }
});
