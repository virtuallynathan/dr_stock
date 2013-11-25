var Common = angular.module('Common', []);


Common.filter('priceChangeColour', function() {
  return function(priceChange) {
    if (priceChange > 0) {
      return '#bdea74';
    } else if (priceChange < 0) {
      return '#ff5454';
    } else {
      return '#36a9e1';
    }
  };
});


Common.filter('abbreviateNumber', function() {
  return function(n) {
    with (Math) {
      var base = floor(log(abs(n)) / log(1000));
      var suffix = 'kmb'[base - 1];
      return suffix ? (n / pow(1000, base)).toPrecision(3) + suffix : '' + n;
    }
  };
});


Common.controller("LoggedInCtrl", function($scope, $window) {
  $scope.logged_in = $window.logged_in;
});


Common.controller('PortfolioCtrl', function($scope, $http) {
  var stockKey = function(stock) {
    return stock.exchange + stock.ticker;
  };

  $scope.inInitialPortfolio = function(stock) {
    return $scope.portfolio && stockKey(stock) in $scope.portfolio;
  };

  $scope.portfolio = null;
  $scope.portfolioList = [];
  $http.get('/accounts/favourites/')
    .success(function(data) {
      $scope.portfolioList = data;
      $scope.portfolio = {};
      for (var index in data) {
        var stock = data[index];
        $scope.portfolio[stockKey(stock)] = stock;
      }
    })
    .error(function(error) {
      $scope.portfolioList = [];
      $scope.portfolio = null;
    });
});


Common.controller('PortfolioStockCtrl', function($scope, $http) {
  $scope.portfoliod = null;

  $scope.inPortfolio = function() {
    if ($scope.portfoliod === null) {
      return $scope.inInitialPortfolio($scope.stock);
    } else {
      return $scope.portfoliod;
    }
  }

  var addToPortfolio = function() {
    $http.get('/accounts/favourite/' + $scope.stock.exchange + '/' + $scope.stock.ticker + '/')
      .success(function(data) {
        $scope.portfoliod = true;
      })
      .error(function(error) {
        $scope.portfoliod = undefined;
      });
  };

  var removeFromPortfolio = function() {
    $http.get('/accounts/unfavourite/' + $scope.stock.exchange + '/' + $scope.stock.ticker + '/')
      .success(function(data) {
        $scope.portfoliod = false;
      })
      .error(function(error) {
        $scope.portfoliod = undefined;
      });
  };

  $scope.portfolio = function() {
    if ($scope.inPortfolio()) {
      removeFromPortfolio();
    } else {
      addToPortfolio();
    }
  };
});


Common.controller('StockDataCtrl', function($scope, $http, $timeout) {
  var fetchData = function() {
    $http.get('/data/stock/' + $scope.exchange + '/' + $scope.ticker + '/')
      .success(function(data) {
        $scope.stock = data;
        $timeout(fetchData, 1000 * 60 * 5);
      })
      .error(function(error) {
        $timeout(fetchData, 1000 * 60 * 5);
      });
  };
  fetchData();
});


Common.controller('IndexDataCtrl', function($scope, $http, $timeout) {
  var fetchData = function() {
    $http.get('/data/index/' + $scope.ticker + '/')
      .success(function(data) {
        $scope.index = data;
        $timeout(fetchData, 1000 * 60 * 5);
      })
      .error(function(error) {
        $timeout(fetchData, 1000 * 60 * 5);
      });
  };
  fetchData();
});