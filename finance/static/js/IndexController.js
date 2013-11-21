var IndexApp = angular.module('IndexApp', []);

IndexApp.controller('StockListCtrl', function($scope, $http, $timeout) {
  (function refresh() {
    $http.get('/data/index/FTSE/').success(
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
