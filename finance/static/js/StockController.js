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
/*
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
*/
StockApp.directive('stockChart', function ($parse) {
    var directiveDefinitionObject = {
        restrict: 'E',
        replace: true,
        scope: {exchange: '@exchange', ticker: '@ticker'},
        template: '<div class="chart"></div>',
        controller: function ($scope, $http) {
          function processData(data) {
            for (index in data) {
              var datum = data[index];
              datum.date = $scope.parseDate(datum.date);
            }
            return data;
          }

          $http.get('/data/historical/' + $scope.exchange + '/' + $scope.ticker + '/2012-01-21/2012-05-21/')
            .success(function(data) {
              console.log($scope.historical);
              console.log('going to set');
              $scope.historical = processData(data.historical);
              $scope.x.domain(d3.extent($scope.historical, function(d) { return d.date; }));
              $scope.y.domain(d3.extent($scope.historical, function(d) { return d.close; }));

              $scope.svg.select(".x.axis").call($scope.xAxis);
              $scope.svg.select(".y.axis").call($scope.yAxis);

              $scope.svg.selectAll("path.line").data([$scope.historical]).attr("d", $scope.line);
              console.log($scope.historical);
            }).error(function(error) {
              console.log('you gone and fucked up again aintcha');
            });
        },
        link: function (scope, element, attrs) {
          scope.historical = [];
          scope.parseDate = d3.time.format("%Y-%m-%d").parse;
          
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;
          scope.x = d3.time.scale().range([0, width]);
          scope.y = d3.scale.linear().range([height, 0]);

          scope.xAxis = d3.svg.axis().scale(scope.x).orient("bottom");
          scope.yAxis = d3.svg.axis().scale(scope.y).orient("left");

          scope.line = d3.svg.line()
              .x(function(d) { return scope.x(d.date); })
              .y(function(d) { return scope.y(d.close); });

          scope.svg = d3.select(element[0]).append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
            .append("g")
              .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          scope.x.domain(d3.extent(scope.historical, function(d) { return d.date; }));
          scope.y.domain(d3.extent(scope.historical, function(d) { return d.close; }));

          scope.svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")

          scope.svg.append("g")
              .attr("class", "y axis")
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", ".71em")
              .style("text-anchor", "end")
              .text("Price");

          scope.svg.append("path")
              .data([scope.historical])
              .attr("class", "line")
              .attr("d", scope.line)
        }
    };
    return directiveDefinitionObject;
});

function Ctrl($scope) {
    $scope.data = [10,20,30,40,60, 80, 20, 50];
}
