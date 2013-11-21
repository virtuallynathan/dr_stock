var IndexApp = angular.module('IndexApp', []);

IndexApp.controller('IndexListCtrl', function($scope, $http, $timeout) {

  $scope.getExchangeChanges = function(stocks, circ_id) {
    if (stocks == null) return "";
    var val = ((stocks.price.price / stocks.price.last_close - 1) * 100).toFixed(3);

    if (val > 0) {
      $("#"+circ_id).css('border-color', '#bdea74');
    } else if (val < 0) {
      $("#"+circ_id).css('border-color', '#ff5454');
    } else {
      $("#"+circ_id).css('border-color', '#36a9e1');
    }
    return val + "%";
  }

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
