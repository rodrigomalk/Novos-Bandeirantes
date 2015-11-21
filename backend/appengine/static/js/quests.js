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

    var _set_all_quest_view_mode = function(quests, mode){
        for (var i = 0; i < quests.length; i++){
            quests[i].viewing_mode = mode;
        }
    };

    $window.onload = function(){
        // load quests
        $http.post("/rest/quests/all", {game_id: $scope.game_id}).success(function(response){
            $scope.quests = response || [];
            _set_all_quest_view_mode($scope.quests, true);
        });
    };

    $scope.set_viewing_mode = function(quest, mode){
      quest.viewing_mode = mode;
    };


    $scope.save_quest = function(quest){

        if (quest === undefined) {
            quest_to_save = {
                question: $scope.new_question,
                answer: $scope.new_answer,
                game_id: $scope.game_id
            };
            $scope.quests.push(quest_to_save);
        }else{
            var quest_to_save = {
                game_id: $scope.game_id,
                question: quest.question,
                answer: quest.answer,
                id: quest.id
            };

        }
        delete quest_to_save.viewing_mode;
        $http.post("/rest/quests/add", quest_to_save).success(function(){
            if (quest){
                $scope.set_viewing_mode(quest, true);
            };
            $scope.set_viewing_mode(quest_to_save, true);
        });
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
        var quest = $scope.quests.splice(index, 1)[0];
        $http.post("/rest/quests/delete/", {quest_id: quest.id});
    };

    $scope.validate_fields = function(){
      if (!$scope.new_answer || !$scope.new_question){
          $scope.error_message = "Por favor. Preencha todos os campos.";
          return false;
      }
        return true;
    };



});

