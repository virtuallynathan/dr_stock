var StockApp = angular.module('StockApp', ['ngRoute']);


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


StockApp.controller('StockParams', function($scope, $routeParams) {
  // Please someone teach how to use Angular properly
  $scope.exchange = $routeParams.exchange;
  $scope.ticker = $routeParams.ticker;
});

StockApp.controller('StockFavorite', function($scope) {
  $scope.favorite = function() {
    $scope.value = "Favorited"
  }
  $scope.unfavorite = function() {
    $scope.value = "Favorite"
  }

});


StockApp.controller('StockDataCtrl', function($scope, $http, $timeout) {

  var abbreviateNumber = function(n) {
    with (Math) {
      var base = floor(log(abs(n)) / log(1000));
      var suffix = 'kmb'[base - 1];
      return suffix ? (n / pow(1000, base)).toPrecision(3) + suffix : '' + n;
    }
  };

  var fetchData = function() {
    $http.get('/data/stock/' + $scope.exchange + '/' + $scope.ticker + '/')
      .success(function(data) {
        $scope.stock = data;
        $scope.volume = abbreviateNumber($scope.stock.price.volume);
        $timeout(fetchData, 1000 * 60 * 5);
      })
      .error(function(error) {
        $timeout(fetchData, 1000 * 60 * 5);
      });
  };
  fetchData();
});


StockApp.controller('IndexParams', function($scope, $routeParams) {
  $scope.ticker = $routeParams.ticker;
});


StockApp.controller('IndexDataCtrl', function($scope, $http, $timeout) {
  var indexChange = function(index) {
    var ratio = index.price.price / index.price.last_close;
    return ((ratio - 1) * 100).toFixed(3);;
  };

  var indexStyle = function(change) {
    if (change > 0) {
      return 'border-color: #bdea74';
    } else if (change < 0) {
      return 'border-color: #ff5454';
    } else {
      return 'border-color: #36a9e1';
    }
  };

  var fetchData = function() {
    $http.get('/data/index/' + $scope.ticker + '/')
      .success(function(data) {
        $scope.index = data;

        var change = indexChange($scope.index);
        $scope.index_change = change + "%";
        $scope.index_change_colour = indexStyle(change);
        $timeout(fetchData, 1000 * 60 * 5);
      })
      .error(function(error) {
        $timeout(fetchData, 1000 * 60 * 5);
      });
  };

  fetchData();
});


StockApp.directive('stockChart', function ($parse) {
    var directiveDefinitionObject = {
        restrict: 'E',
        replace: true,
        scope: {exchange: '@exchange', ticker: '@ticker'},
        template: '<div class="chart"></div>',
        controller: function ($scope, $http) {
          $scope.formatDate = d3.time.format("%Y-%m-%d");
          $scope.parseDate = $scope.formatDate.parse;

          $scope.fixupDomain = function() {
            var range = $scope.x.domain();
            range[0] = Math.max(range[0], $scope.lowestDate);
            range[1] = Math.min(range[1], $scope.highestDate);
            $scope.x.domain(range);
          }

          $scope.redraw = function() {
            $scope.fixupDomain();
            $scope.newDataRange();
            $scope.svg.select(".x.axis").call($scope.xAxis.tickSize(6).tickFormat(null));
            $scope.svg.select(".y.axis").call($scope.yAxis.tickSize(6).tickFormat(null));
            $scope.svg.select(".x.grid").call($scope.xAxis.tickSize(-$scope.height, 0, 0).tickFormat(""));
            $scope.svg.select(".y.grid").call($scope.yAxis.tickSize(-$scope.width, 0, 0).tickFormat(""));
            $scope.svg.select("path.area").attr("d", $scope.area);
            $scope.svg.select("path.line").attr("d", $scope.line);
          }

          $scope.updateChart = function(data) {
            data.sort(function (d1, d2) {
              d1 = d1.date;
              d2 = d2.date;
              return d1 < d2 ? -1 : (d1 > d2 ? 1 : 0);
            });

            $scope.lowestDate = data[0].date;
            $scope.highestDate = data[data.length - 1].date;

            $scope.y.domain(d3.extent(data, function(d) { return d.close; }));
            $scope.y.nice();
            $scope.svg.select("path.area").datum(data);
            $scope.svg.select("path.line").datum(data);
            $scope.zoom.x($scope.x);
            $scope.redraw();
          }

          $scope.newDataRange = function() {
            var currentRange = $scope.x.domain();
            var period = currentRange[1].getTime() - currentRange[0].getTime();
            var requiredMin = new Date(currentRange[0].getTime() - period);
            if (requiredMin < $scope.currentMin) {
              var newMin = new Date(requiredMin.getTime() - 2 * period);
              $scope.fetchData($scope.exchange, $scope.ticker, newMin, $scope.currentMin);
              $scope.currentMin = newMin;
            }
          }

          $scope.fetchData = function(exchange, ticker, startDate, endDate) {
            var startDateStr = $scope.formatDate(startDate);
            var endDateStr = $scope.formatDate(endDate);
            $http.get('/data/historical/' + exchange + '/' + ticker + '/' + startDateStr + '/' + endDateStr + '/')
              .success(function(data) {
                for (var index in data.historical) {
                  var datum = data.historical[index];
                  var dateStr = datum.date;
                  datum.date = $scope.parseDate(dateStr);
                  $scope.historical.set(dateStr, datum);
                }
                $scope.updateChart($scope.historical.values());
              }).error(function(error) {
                console.log('you gone and fucked up again aintcha');
              });
          }

          $scope.historical = d3.map();
          var margin = {top: 20, right: 20, bottom: 30, left: 50};
          $scope.width = 960 - margin.left - margin.right;
          $scope.height = 500 - margin.top - margin.bottom;

          $scope.x = d3.time.scale().range([0, $scope.width]);
          $scope.y = d3.scale.linear().range([$scope.height, 0]);

          var endDate = new Date();
          var startDate = new Date();
          startDate.setMonth(startDate.getMonth() - 9);

          $scope.currentMin = new Date(startDate.getTime() - 2 * (endDate.getTime() - startDate.getTime()))
          $scope.x.domain([startDate, endDate]);
          $scope.fetchData($scope.exchange, $scope.ticker, $scope.currentMin, endDate);
        },
        link: function (scope, element, attrs) {
          var margin = {top: 20, right: 20, bottom: 30, left: 50};
          scope.xAxis = d3.svg.axis().scale(scope.x).orient("bottom");
          scope.yAxis = d3.svg.axis().scale(scope.y).orient("left");

          scope.line = d3.svg.line()
              .x(function(d) { return scope.x(d.date); })
              .y(function(d) { return scope.y(d.close); });

          scope.area = d3.svg.area()
              .x(function(d) { return scope.x(d.date); })
              .y0(scope.height)
              .y1(function(d) { return scope.y(d.close); });

          scope.svg = d3.select(element[0]).append("svg")
              .attr("width", scope.width + margin.left + margin.right)
              .attr("height", scope.height + margin.top + margin.bottom)
            .append("g")
              .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          // X and Y axes
          scope.svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + scope.height + ")")

          scope.svg.append("g")
              .attr("class", "y axis")

          // X and Y grids (axes with ticks that span the whole graph)
          scope.svg.append("g")
              .attr("class", "x grid")
              .attr("transform", "translate(0," + scope.height + ")")

          scope.svg.append("g")
              .attr("class", "y grid")

          // Two paths - one for the line, one for the shaded area
          scope.svg.append("path").attr("class", "line").attr("clip-path", "url(#clip)");
          scope.svg.append("path").attr("class", "area").attr("clip-path", "url(#clip)");

          // Zoom pane and behaviour
		      scope.zoom = d3.behavior.zoom().on("zoom", scope.redraw);
          scope.svg.append("rect").attr("class", "pane")
              .attr("width", scope.width)
              .attr("height", scope.height)
              .call(scope.zoom)

          scope.svg.append("clipPath")
              .attr("id", "clip")
            .append("rect")
              .attr("x", 0)
              .attr("y", 0)
              .attr("width", scope.width)
              .attr("height", scope.height);
        }
    };
    return directiveDefinitionObject;
});
