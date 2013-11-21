var StockApp = angular.module('StockApp', []);

StockApp.controller('StockListCtrl', function($scope, $http, $timeout) {
  (function refresh() {
    $http.get('/data/stock/' + exchange + '/' + ticker + '/').success(
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

StockApp.controller('HistoricalCtrl', function($scope, $http, $timeout) {
  function processData(data) {
    for (index in data) {
      datum = data[index];
      datum.date = parseDate(datum.date)
    }
  }
  (function refresh() {
    $http.get('/data/historical/' + exchange + '/' + ticker + '/2013-10-21/2013-11-21/').success(
      function(data) {
        $scope.historical = processData(data);
      }).error(
        function(error) {
          $scope.stocks = ['everythings fucked'];
          $timeout(refresh, 1000 * 60 * 5);
        }
    );})();
});
