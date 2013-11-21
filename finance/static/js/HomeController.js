var IndexApp = angular.module('HomeApp', []);

HomeApp.controller('homeCtrl', function($scope, $http, $timeout) {
  (function refresh() {
    $http.get('/data/biggest/10/').success(
      function(data) {
        $scope.stocks = data;
        $timeout(refresh, 1000 * 60 * 5);
      }).error(
        function(error) {
          $scope.stocks = ['everythings fucked'];
          $timeout(refresh, 1000 * 60 * 5);
        }
    );})();
});
