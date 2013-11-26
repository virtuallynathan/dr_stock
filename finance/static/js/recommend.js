var RecommendApp = angular.module('RecommendApp', ['Common']);


RecommendApp.controller('RecommendCtrl', function($scope, $http, $timeout) {
  var getData = function () {
    $http.get('/recommendations/10/')
      .success(function(data) {
        for (var i = 0; i < data.length; i++) {
          data[i].rank = i + 1;
        }
        $scope.recommended = data;
        $timeout(getData, 1000 * 60 * 60);
      }).error(function(error) {
        $timeout(getData, 1000 * 60 * 60);
      })
  };
  getData();
});
