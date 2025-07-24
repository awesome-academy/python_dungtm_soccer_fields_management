function toggleFieldRequestSections() {
  const value = $('#id_type').val();
  $('#field-selector').toggle(value === 'update' || value === 'delete');
  $('#field-details').toggle(value === 'add' || value === 'update');
}

$(document).ready(function () {
  toggleFieldRequestSections();
  $('#id_type').change(toggleFieldRequestSections);
});
