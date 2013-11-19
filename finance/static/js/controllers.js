var stockApp = angular.module('stockApp', []);

stockApp.controller('StockListCtrl', function ($scope, $http) {
  $http.get('/data/index/FTSE/').success(function(data) {
    $scope.stocks = data;
  });
});
