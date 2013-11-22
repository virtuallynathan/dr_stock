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


StockApp.directive('stockChart', function ($parse) {
    var directiveDefinitionObject = {
        restrict: 'E',
        replace: true,
        scope: {exchange: '@exchange', ticker: '@ticker',
                startDate: '@startDate', endDate: '@endDate'},
        template: '<div class="chart"></div>',
        controller: function ($scope, $http) {
          $scope.formatDate = d3.time.format("%Y-%m-%d");
          $scope.parseDate = $scope.formatDate.parse;

          $scope.processData = function(data) {
            for (index in data) {
              data[index].date = $scope.parseDate(data[index].date);
            }
            return data;
          }

          $scope.updateChart = function(data) {
            $scope.x.domain(d3.extent(data, function(d) { return d.date; }));
            $scope.y.domain(d3.extent(data, function(d) { return d.close; }));
            $scope.y.nice();

            $scope.svg.select(".x.axis").call($scope.xAxis);
            $scope.svg.select(".y.axis").call($scope.yAxis);
            $scope.svg.select(".x.grid").call($scope.xAxis.tickSize(-$scope.height, 0, 0).tickFormat(""));
            $scope.svg.select(".y.grid").call($scope.yAxis.tickSize(-$scope.width, 0, 0).tickFormat(""));
            $scope.svg.selectAll("path.area").datum(data).attr("d", $scope.area);
            $scope.svg.selectAll("path.line").datum(data).attr("d", $scope.line);
          }

          $scope.fetchData = function(exchange, ticker, startDate, endDate) {
            var startDateStr = $scope.formatDate(startDate);
            var endDateStr = $scope.formatDate(endDate);
            $http.get('/data/historical/' + exchange + '/' + ticker + '/' + startDateStr + '/' + endDateStr + '/')
              .success(function(data) {
                $scope.historical = $scope.processData(data.historical);
                $scope.updateChart($scope.historical);
              }).error(function(error) {
                console.log('you gone and fucked up again aintcha');
              });
          }

          var startDate = $scope.parseDate($scope.startDate);
          var endDate = $scope.parseDate($scope.endDate);
          $scope.fetchData($scope.exchange, $scope.ticker, startDate, endDate);
        },
        link: function (scope, element, attrs) {
          var margin = {top: 20, right: 20, bottom: 30, left: 50};
          scope.width = 960 - margin.left - margin.right;
          scope.height = 500 - margin.top - margin.bottom;

          scope.x = d3.time.scale().range([0, scope.width]);
          scope.y = d3.scale.linear().range([scope.height, 0]);

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

          scope.svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + scope.height + ")")

          scope.svg.append("g")
              .attr("class", "y axis")
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", ".71em")
              .style("text-anchor", "end")
              .text("Price");

          scope.svg.append("g")
              .attr("class", "x grid")
              .attr("transform", "translate(0," + scope.height + ")")

          scope.svg.append("g")
              .attr("class", "y grid")

          scope.svg.append("path").attr("class", "line");
          scope.svg.append("path").attr("class", "area");
        }
    };
    return directiveDefinitionObject;
});

