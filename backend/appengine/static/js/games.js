

var jogoApp = angular.module('jogoApp', ['jogoModulo']).config(function($interpolateProvider){
  $interpolateProvider.startSymbol("{_");
  $interpolateProvider.endSymbol("_}");
}).controller("JogoController", function($scope, $http, $window){
    $scope.game={};
    $scope.mostra=false;
    $scope.games = [];
    $scope.is_editing = false;

    $scope.list_games = function(){
      $http.post("/jogos/rest/index").success(function(result){
        $scope.games = result;
      });
    };

    $window.onload = $scope.list_games;

    $scope.remove = function(game_id, index){
      $http.post("/jogos/rest/delete", {jogo_id: game_id}).success(function(){
        $scope.games.splice(index, 1);
      });
    };

    $scope.edit = function(game){
      delete game.creation;
      $scope.game = game;
      $scope.formOnOff();
      $scope.is_editing = true;
      $scope.edit_or_create = 'Editar';

    };

    $scope.new = function(){
      $scope.formOnOff();
      $scope.is_editing = false;
      $scope.edit_or_create = 'Criar';
    };

    $scope.formOnOff=function(){
        $scope.mostra=!$scope.mostra;

    };

});