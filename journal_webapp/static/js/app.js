var app = angular.module('app',['angularUtils.directives.dirPagination']);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

app.controller("AppCtrl", function($scope, $http){
    var app = this;

    $http.get("/api/journal").success(function (data) {
        app.journals = data.objects;
    })

    app.addJournal = function () {
        $http.post("/api/journal",{"body":form.journal.data, "nb":2})
            .success(function (data) {
                app.journals.push(data);
            })
    }
    app.deleteJournal = function (journal) {
        $http.delete("/api/journal/" + journal.id).success(function(response) {
            app.journals.splice(app.journals.indexOf(journal),1)
        })
    }

});

