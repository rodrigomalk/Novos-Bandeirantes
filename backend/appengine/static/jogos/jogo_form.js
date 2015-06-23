var jogoModulo=angular.module('jogoModulo', []).directive('jogoform', function(){
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/jogos/novo.html',
        scope:{
            game: '='
        },

    };
});