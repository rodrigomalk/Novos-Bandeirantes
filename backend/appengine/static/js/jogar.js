angular.module("jogarApp", ['answer_service']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol("{_").endSymbol("_}");
}).controller('jogarCtrl', function($scope, $window, AnswerService) {

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
                criarGrafico(titulo, '');
                first = false;
                break;
        }

    };
    $scope.game = g_game;
    $scope.results = [];
    //$scope.game_id = $location.search().game_id;
    $scope.quests_count = 1;
    $scope.quests = g_quest_list;
    $scope.actual_quest = $scope.quests[0];
    $scope.tries = 0;
    $scope.medal = true;
    $scope.points = 0;
    $scope.resposta = "Sua resposta esta errada!";
    now = new Date;
    $scope.time = now.getMilliseconds();
    $scope.save_result = function(points, medal, game_id) {
        result_to_save = {
            points: points,
            date: now.getDate,
            medal: medal,
            game_id: game_id,
        };
        $scope.results.push(result_to_save);
        delete result_to_save.viewing_mode;
        $http.post("/rest/results/add", result_to_save).success(function () {
            if (result) {
                $scope.set_viewing_mode(result, true);
            };
            $scope.set_viewing_mode(result_to_save, true);
        });
    };

    $scope.answer = function(answer){
        $scope.tries += 1;
        AnswerService.answer(answer, $scope.tries, $scope.actual_quest.id).success(function(result){
            if (now.getMilliseconds() - $scope.time > 120000) $scope.medal = false;
            if (result.right){
                $scope.points++;
                $scope.resposta = "Sua resposta esta certa!";
                if ($scope.quests_count  < $scope.quests.length){
                    $scope.actual_quest =  $scope.quests[$scope.quests_count++];
                    $scope.tries = 0;
                }else{
                    $scope.save_result($scope.points, $scope.medal, $scope.game_id);
                    window.location.href = "/jogos";
                }
            }else{

                $scope.resposta = "Sua resposta esta errada!";
                if (!result.can_try_again){
                    if ($scope.quests_count  == $scope.quests.length){
                        $scope.save_result($scope.points, $scope.medal, $scope.game_id);
                        window.location.href = "/jogos";
                    }else {
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
                highlightOnHover: true,
                popupOnHover: true,
                highlightFillColor: 'a(6)',
                highlightBorderColor: 'rgba(60, 15, 250, 0.6)',
                highlightBorderWidth: 6
            },
            done: function (datamap) {
                datamap.svg.selectAll('.datamaps-subunit').on('click', function (e) {
                    $scope.answer(e.properties.name);
                    $("#nome").html(e.properties.name);
                    $("#resposta").html($scope.resposta);
                    $('#confirm')
                        .modal({ backdrop: 'static', keyboard: false })
                        .one('click', '[data-value]', function (e) {
                    });
                });
            },
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
                        fillColor: "rgba(13,13,255,0.8)",
                        strokeColor: "rgba(60, 15, 250, 0.6)",
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
