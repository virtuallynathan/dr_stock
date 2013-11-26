var RecommendApp = angular.module('RecommendApp', ['Common']);


RecommendApp.controller('RecommendCtrl', function($scope, $http, $timeout) {
  var getData = function () {
    $http.get('/recommendations/10/')
      .success(function(data) {
        $scope.recommended = data;
        $timeout(getData, 1000 * 60 * 60);
      }).error(function(error) {
        $timeout(getData, 1000 * 60 * 60);
      })
  };
  getData();
});
