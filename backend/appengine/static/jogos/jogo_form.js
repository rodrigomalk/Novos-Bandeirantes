var jogoModulo=angular.module('jogoModulo', [])

jogoModulo.directive('jogoform', function(){
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/jogos/novo.html',
        scope:{
            game: '='
        },
        controller:function($scope, $http){
            $scope.salvar=function(){
                $http.post('/jogos/rest/new',$scope.game).success(function(course){
                    console.log(game);
                }).error(function(erros){
                    console.log(erros)
                });
            }
        }

    };
});