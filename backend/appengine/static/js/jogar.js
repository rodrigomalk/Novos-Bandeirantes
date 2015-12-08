angular.module("jogarApp", ['answer_service']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol("{_").endSymbol("_}");
}).controller('jogarCtrl', function($location, $scope, $http, $window, $timeout, AnswerService) {

    var selecionar = function (botao, containerm) {
        $('#containerm').empty();
        containerm.appendTo('body');
        var a = [];
        var b = {};
        var pop = [41281631, 10426160, 201032714, 17248450, 45925397, 15007343, 953605, 221500, 7356789, 28674757, 560157, 3424595, 28892735];
        var are = [2780400, 1098581, 8515767, 756950, 1138914, 256370, 214970, 83846, 406752, 1285220, 163821, 176215, 916445];
        var pa = [pop[0] / are[0], pop[1] / are[1], pop[2] / are[2], pop[3] / are[3], pop[4] / are[4], pop[5] / are[5], pop[6] / are[6], pop[7] / are[7], pop[8] / are[8], pop[9] / are[9], pop[10] / are[10], pop[11] / are[11], pop[12] / are[12]];
        while (botao > 3) {
            botao -= 3;
        }
        while (botao < 1 && !first) {
            botao += 3;
        }
        switch (botao) {
            case 0:
                criarMapa(b);
                criarGrafico(g_game.tit, '');
                first = false;
                break;
        }

    };
    $scope.game = g_game;
    var results = [];
    $scope.quests_count = 1;
    $scope.quests = g_quest_list;
    $scope.actual_quest = $scope.quests[0];
    $scope.previous_quest = $scope.actual_quest;
    $scope.tries = 0;
    $scope.won_medal = false;
    $scope.medal = true;
    $scope.points = 0;
    $scope.resposta_mensagem = "Sua resposta está errada!";
    var before = new Date();
    var ellapsed_seconds = 0;

    var start_count_time = function(){
        setTimeout(function(){
            start_count_time();
            ellapsed_seconds += 1;
            if(g_game.tmp != 0){
                if (ellapsed_seconds > g_game.tmp) {
                    save_results($scope.points, g_game.id, $scope.won_medal, ellapsed_seconds, $scope.quests.length);
                    $scope.go_to_games_index();
                }
            }
        }, 1000);
    };
    start_count_time();

    var save_results = function(points, game_id, won_medal, ellapsed_seconds, quests_length) {

        var data = {
            points: points,
            game_id: game_id,
            won_medal: won_medal,
            duration: ellapsed_seconds,
            size: quests_length
        };
        $http.post("/rest/results/add", data);
    };

    $scope.go_to_games_index = function(){
        setTimeout(function(){ ($window.location.href = "/jogos"); }, 3000);
    };

    $scope.show_modal = function(){
        $('#confirm')
            .modal({ backdrop: 'static', keyboard: false })
            .one('click');
    };

    $scope.close_modal = function(){
        $scope.show_modal = false;
    };

    $scope.answer = function(answer){
        $scope.tries += 1;
        AnswerService.answer(answer, $scope.tries, $scope.actual_quest.id).success(function(result){
           if (ellapsed_seconds > 60){
             $scope.medal = false;
           }
            if (result.right){
                $scope.points++;
                $scope.resposta_mensagem = "Sua resposta está certa!";
                $scope.show_modal();
                $scope.previous_quest = $scope.actual_quest;
                // proxima pergunta
                if ($scope.quests_count  < $scope.quests.length){
                    $scope.actual_quest =  $scope.quests[$scope.quests_count++];
                    $scope.tries = 0;
                }else{
                    if($scope.medal == true){
                        $scope.won_medal = true;
                    }
                    save_results($scope.points, g_game.id, $scope.won_medal, ellapsed_seconds, $scope.quests.length);
                    $scope.go_to_games_index();
                }
            }else{
                $scope.medal = false;
                $scope.resposta_mensagem = "Sua resposta esta errada!";
                $scope.show_modal();
                $scope.previous_quest = $scope.actual_quest;
                if (!result.can_try_again){
                    // cabou o jogo
                    if ($scope.quests_count  == $scope.quests.length){
                       save_results($scope.points, g_game.id, $scope.won_medal, ellapsed_seconds, $scope.quests.length);
                        $scope.go_to_games_index();
                    }else {
                        // proxima pergunta
                        $scope.actual_quest = $scope.quests[$scope.quests_count++];
                        $scope.tries = 0;
                    }
                }
            }
            }).error(function(error){
                console.log(error);
            });
    };
    var criarMapa = function (b) {
        var map = new Datamap({
            scope: 'world',
            element: document.getElementById('containerm'),
            fills: {
                HIGH: 'rgba(0,153,0,0.8)',
                MED: 'rgba(255,200,0,0.8)',
                LOW: 'rgba(255,0,0,0.8)',
                defaultFill: 'rgba(13,13,255,0.8)'
            },
            setProjection: function (element, b) {
                var projection = d3.geo.equirectangular()
                    .center([-53.8, -21.5])
                    .rotate([4.4, 0])
                    .scale(500)
                    .translate([element.offsetWidth / 2, element.offsetHeight / 2]);
                var path = d3.geo.path()
                    .projection(projection);
                return {path: path, projection: projection};
            },
            data: b,

            geographyConfig: {
                popupTemplate: function (geo, data) {
                    return ['<div class="hoverinfo"><strong>',
                        geo.properties.name,
                        '</strong></div>'].join('');
                },
                borderColor: 'rgba(0, 0, 0, 0.6)',
                highlightOnHover: true,
                popupOnHover: true,
                highlightFillColor: 'rgba(13,255,13,0.8)',
                highlightBorderColor: 'rgba(255, 13, 13, 0.6)',
                highlightBorderWidth: 6
            },
            done: function (datamap) {
                datamap.svg.selectAll('.datamaps-subunit').on('click', function (e) {
                    $scope.answer(e.properties.name);
                });
            }
        });
    };


    var criarGrafico = function (titulo, a) {

        $("#titulo").html(titulo);
        if (a != '') {
            $("#gra").html('<canvas id="myChart" width="550" height="400""></canvas>');
            var data = {
                labels: ['Argentina', 'Bolívia', 'Brasil', 'Chile', 'Colômbia', 'Equador', 'Guiana', 'Guiana Francesa', 'Paraguai', 'Peru', 'Suriname', 'Uruguai', 'Venezuela'],
                datasets: [
                    {
                        fillColor: "rgba(255,255,255,0.8)",
                        strokeColor: "rgba(255, 255, 255, 0.6)",
                        data: a
                    }
                ]
            };
            options = {
                scaleOverlay: false,
                scaleOverride: false,
                scaleSteps: null,
                scaleStepWidth: null,
                scaleStartValue: null,
                scaleLineColor: "rgba(0,0,0,.1)",
                scaleLineWidth: 1,
                scaleShowLabels: true,
                scaleLabel: "<%=value%>",
                scaleFontFamily: "'Arial'",
                scaleFontSize: 16,
                scaleFontStyle: "bold",
                scaleFontColor: "#000",
                scaleShowGridLines: true,
                scaleGridLineColor: "rgba(0,0,0,.05)",
                scaleGridLineWidth: 1,
                barShowStroke: true,
                barStrokeWidth: 2,
                barValueSpacing: 2,
                barDatasetSpacing: 2,
                animation: true,
                animationSteps: 60,
                animationEasing: "easeOutQuart",
                onAnimationComplete: null,
            };
            var ctx = document.getElementById("myChart").getContext("2d");
            new Chart(ctx).Bar(data, options);
        }
    };

    $window.onload = function () {
        var botao = 0;
        first = true;
        var containerm = $("#containerm");
        indice = '';
        selecionar(botao, containerm);

    $('.bot').click(function () {
        botao = parseInt($(this).attr("value"));
        selecionar(botao);
    });
};
});
