var homeApp = angular.module('homeApp', []);

homeApp.controller('homeCtrl', function($scope, $http, $timeout) {
  (function refresh() {
    $http.get('/data/risers/3/').success(
      function(data) {
        $scope.risers = data;
        $timeout(refresh, 1000 * 60 * 5);
      }).error(
        function(error) {
          $timeout(refresh, 1000 * 60 * 5);
        }
    );})();
  (function refresh() {
    $http.get('/data/fallers/3/').success(
      function(data) {
        $scope.fallers = data;
        $timeout(refresh, 1000 * 60 * 5);
      }).error(
        function(error) {
          $timeout(refresh, 1000 * 60 * 5);
        }
    );})();
  (function refresh() {
    $http.get('/data/biggest/3/').success(
      function(data) {
        $scope.biggest = data;
        $timeout(refresh, 1000 * 60 * 5);
      }).error(
        function(error) {
          $timeout(refresh, 1000 * 60 * 5);
        }
    );})();
});
