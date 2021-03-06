var HomeApp = angular.module('HomeApp', ['Common']);


HomeApp.controller('HomeCtrl', function($scope, $http, $timeout) {
  $scope.getBarHeight = function(datas, index, id, capOrChange) {

    var val = (capOrChange ? datas[index].price.market_cap : Math.abs(datas[index].price.change));
    var max_val = -1;
    var min_val = -1;

    for (var i = 0; i < datas.length; i++) {
      var this_val = (capOrChange ? datas[i].price.market_cap : Math.abs(datas[i].price.change));

      if (this_val > max_val || max_val == -1) max_val = this_val;
      if (this_val < min_val || min_val == -1) min_val = this_val;
    }

    var range = max_val - min_val;
    var raw_percent = 100*(val - min_val)/range;

    //scale it arbitrarily to look better
    var percent = ((raw_percent*0.7) + 15) + "%";
    $("#"+id).find('.value').animate({height:percent}, 2000, function() {});

    return percent;
  };

  (function refresh() {
    $http.get('/data/indexes/10/').success(
      function(data) {
        $scope.indexes = data;
        $timeout(refresh, 1000 * 60 * 5);
      }).error(
        function(error) {
          $timeout(refresh, 1000 * 60 * 5);
        }
    );})();
  (function refresh() {
    $http.get('/data/risers/3/').success(
      function(data) {
        $scope.risers = data;
        $timeout(refresh, 1000 * 60 * 5);
      }).error(
        function(error) {
          $timeout(refresh, 1000 * 60 * 5);
        }
    );})();
  (function refresh() {
    $http.get('/data/fallers/3/').success(
      function(data) {
        $scope.fallers = data;
        $timeout(refresh, 1000 * 60 * 5);
      }).error(
        function(error) {
          $timeout(refresh, 1000 * 60 * 5);
        }
    );})();
  (function refresh() {
    $http.get('/data/biggest/3/').success(
      function(data) {
        $scope.biggest = data;
        $timeout(refresh, 1000 * 60 * 5);
      }).error(
        function(error) {
          $timeout(refresh, 1000 * 60 * 5);
        }
    );})();
});
