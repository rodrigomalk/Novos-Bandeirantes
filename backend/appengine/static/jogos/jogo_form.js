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
            formOnOff: "&",
            crudService: "="
        },
        controller:function($scope, $http){
            $scope.salvando = false;
            var save_or_edit_url =  '/jogos/rest/new';
            $scope.salvar = function(){
                $scope.salvando = true;
              if ($scope.isEditing){
                $scope.game.jogo_id = $scope.game.id;
                $scope.save_or_edit_url = '/jogos/rest/edit';

              }
              else{
                save_or_edit_url = '/jogos/rest/new';
              }
              $http.post(save_or_edit_url, $scope.game).success(function(game){
                  $scope.salvando = false;
                  $scope.formOnOff();
                  if (save_or_edit_url == '/jogos/rest/new')
                    $scope.games.push(game);
              }).error(function(errors){
                  $scope.errors=errors;
                  console.log(errors);
                  $scope.salvando = false;
              });
          };
        }
    };
});
