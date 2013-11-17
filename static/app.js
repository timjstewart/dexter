var app = angular.module('Dexter', []);

app.filter('escape', function() {
  return window.encodeURIComponent;
});
