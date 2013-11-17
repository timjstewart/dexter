app.controller('SearchController', function ($scope, $http) {
    $scope.query='';
    $scope.message='';
    $scope.search_type = 'title_and_text';

    $scope.search = function() {
        $scope.message='';
        
        if ($scope.search_type == 'title_only') {
            $http.get("/search/title?q="+ $scope.query)
                .success(function(data, status, headers, config) {
                    $scope.hits=data;
                    if ($scope.hits.length === 0) {
                        $scope.message = "No matching documents";
                    }
                });
        }
        else {
            $http.get("/search/text?q="+ $scope.query)
                .success(function(data, status, headers, config) {
                    $scope.hits=data;
                    if ($scope.hits.length === 0) {
                        $scope.message = "No matching documents";
                    }
                });
        }
    }

    $scope.hits = [];
});
