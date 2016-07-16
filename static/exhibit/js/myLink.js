$(document).ready(function() {
  $('.myLink a').on('tap', function() {
    var link = $(this).attr('href');
    window.location.href = link;
    return false;
  })
  $('.myLink').on('tap', function() {
    var link = $(this).attr('href');
    window.location.href = link;
  });
});