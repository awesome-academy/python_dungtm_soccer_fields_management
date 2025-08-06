$(document).ready(function() {
  const $gridView = $('#gridView');
  const $listView = $('#listView');
  const $fieldsGrid = $('#fieldsGrid');
  const $fieldsList = $('#fieldsList');
  
  if ($gridView.length && $listView.length && $fieldsGrid.length && $fieldsList.length) {
    $gridView.on('click', function() {
      $fieldsGrid.removeClass('d-none');
      $fieldsList.addClass('d-none');
      $gridView.addClass('active');
      $listView.removeClass('active');
      
      localStorage.setItem('preferredView', 'grid');
    });
    
    $listView.on('click', function() {
      $fieldsGrid.addClass('d-none');
      $fieldsList.removeClass('d-none');
      $gridView.removeClass('active');
      $listView.addClass('active');
      
      localStorage.setItem('preferredView', 'list');
    });
    
    const preferredView = localStorage.getItem('preferredView');
    if (preferredView === 'list') {
      $listView.trigger('click');
    }
  }
});