$(document).ready(function() {
  var activePage = $('#sideNav').attr('active');
  $('.sideNavItem[name="' + activePage + '"]').addClass('active');
})