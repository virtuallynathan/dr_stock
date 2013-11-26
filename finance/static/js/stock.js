var StockApp = angular.module('StockApp', ['Common', 'Chart', 'ngRoute']);


StockApp.config(function($routeProvider) {
  $routeProvider.
    when('/:ticker', {
      templateUrl: '/static/partials/index-view.html',
      controller: 'IndexParams'
    }).
    when('/:exchange/:ticker', {
      templateUrl: '/static/partials/stock-view.html',
      controller: 'StockParams'
    }).
    otherwise({
      redirectTo: '/FTSE'
    });
});


StockApp.controller('IndexParams', function($scope, $routeParams) {
  $scope.ticker = $routeParams.ticker;
});


StockApp.controller('StockParams', function($scope, $routeParams) {
  // Please someone teach me how to use Angular properly
  $scope.exchange = $routeParams.exchange;
  $scope.ticker = $routeParams.ticker;
});
