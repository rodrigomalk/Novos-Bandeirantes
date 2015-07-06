var jogoModulo = angular.module('jogoModulo', [])

jogoModulo.directive('jogoform', function(){
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/jogos/novo.html',
        scope:{
            game: '=',
            isEditing: "=?",
            editOrCreate: "=?",
            formOnOff: "&"
        },
        controller:function($scope, $http){
           var save_or_edit_url =  '/jogos/rest/new';
            $scope.salvar = function(){
              if ($scope.isEditing){
                save_or_edit_url = '/jogos/rest/edit';
                $scope.game.jogo_id = $scope.game.id;
              }
              else{
                save_or_edit_url = '/jogos/rest/new';
              }
              $http.post(save_or_edit_url, $scope.game).success(function(game){
                  console.log(game);
              }).error(function(errors){
                  console.log(errors);
              });
          };
        }
    };
});
