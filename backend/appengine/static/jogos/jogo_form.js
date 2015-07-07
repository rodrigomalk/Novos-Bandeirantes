var jogoModulo = angular.module('jogoModulo', [])

jogoModulo.directive('jogoform', function(){
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/jogos/novo.html',
        scope:{
            game: '=',
            games: "=",
            isEditing: "=?",
            editOrCreate: "=?",
            formOnOff: "&"
        },
        controller:function($scope, $http){
            $scope.salvando = false;
           var save_or_edit_url =  '/jogos/rest/new';
            $scope.salvar = function(){
                $scope.salvando = true;
              if ($scope.isEditing){
                save_or_edit_url = '/jogos/rest/edit';
                $scope.game.jogo_id = $scope.game.id;
              }
              else{
                save_or_edit_url = '/jogos/rest/new';
                  $scope.games.push($scope.game);
              }
              $http.post(save_or_edit_url, $scope.game).success(function(game){
                  console.log(game);

                  $scope.salvando = false
                  $scope.formOnOff();
              }).error(function(errors){
                  $scope.errors=errors;
                  console.log(errors);
                  $scope.salvando = false;
              });
          };
        }
    };
});
