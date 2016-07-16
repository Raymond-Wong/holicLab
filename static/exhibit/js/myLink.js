$(document).ready(function() {
  $('.myLink a').on('click', function() {
    var link = $(this).attr('href');
    window.location.href = link;
    return false;
  })
  $('.myLink').on('click', function() {
    var link = $(this).attr('href');
    window.location.href = link;
  });
});