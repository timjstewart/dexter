app.controller('SearchController', function ($scope, $http) {
    $scope.query=""

    $scope.search = function() {
        $http.get("/search/title?q="+ $scope.query)
           .success(function(data, status, headers, config) {
               $scope.hits=data;
           });
    }

    $scope.hits = [];
});
