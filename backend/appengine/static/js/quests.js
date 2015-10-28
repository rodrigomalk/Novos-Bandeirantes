angular.module('questApp', []).config(function($locationProvider, $interpolateProvider){
    $interpolateProvider.startSymbol("{_").endSymbol("_}");
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
}).controller("QuestController", function($scope, $window, $http, $location){
    $scope.quests = [];
    $scope.game_id = $location.search().game_id;
    $scope.show_add_quest = false;

    $window.onload = function(){
        // load quests
        $http.post("/rest/quests/all", {game_id: $scope.game_id}).success(function(response){
            $scope.quests = response || [];
        });
    }

    $scope.save_quest = function(){
        var quest = {
            question: $scope.new_question,
            answer: $scope.new_answer,
            game_id: $scope.game_id
        };

        $scope.quests.push(quest);

        $http.post("/rest/quests/add", quest);

        $scope.new_question = "";
        $scope.new_answer = "";
        $scope.show_add_quest = false;
    };

    $scope.edit_quest = function(){

    };

    $scope.new_quest = function(){
        $scope.show_add_quest = !$scope.show_add_quest;
    };

    $scope.remove_quest = function(index){
        var quest = $scope.quests.splice(index, 1);
        $http.post("/rest/quests/delete/", {quest_id: quest.id});
    };          

});

