$(document).ready(function() {
  loading();
});

var loading = function() {
  try {
    // 如果存在这个变量，那么当变量为真时结束加载
    if (FINISHED_LOADING) {
      finishLoading();
    } else {
      setTimeout(loading, 100);
    }
  } catch (e) {
    // 如果不存在这个变量，则直接结束加载
    finishLoading();
  }
}

var finishLoading = function() {
  $('#loadingContainer').remove();
}