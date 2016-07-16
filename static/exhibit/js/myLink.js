$(document).ready(function() {
  $('.myLink a').click(function() {
    var link = $(this).attr('href');
    window.location.href = link;
    return false;
  })
  $('.myLink').click(function() {
    var link = $(this).attr('href');
    window.location.href = link;
  });
});