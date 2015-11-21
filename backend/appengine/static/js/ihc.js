//<![CDATA[ 
$(window).load(function(){
var botao = 0;
first = true;
var containerm = $("#containerm");
indice = '';
selecionar(botao);
function retornar(first, botao){
    first = true;
    botao = botao;
    selecionar(botao)
};
function selecionar(botao){
    $('#containerm').empty();
    containerm.appendTo('body');
    var a = [];
var b = {};
var pop = [41281631,10426160,201032714,17248450,45925397,15007343,953605,221500,7356789,28674757,560157,3424595,28892735];
var are = [2780400,1098581,8515767,756950,1138914,256370,214970,83846,406752,1285220,163821,176215,916445];
var pa = [pop[0]/are[0],pop[1]/are[1],pop[2]/are[2],pop[3]/are[3],pop[4]/are[4],pop[5]/are[5],pop[6]/are[6],pop[7]/are[7],pop[8]/are[8],pop[9]/are[9],pop[10]/are[10],pop[11]/are[11],pop[12]/are[12]];
    while (botao > 3){
        botao-=3;
    }
        while (botao < 1 && !first){
        botao+=3;
    }
    switch (botao)
{
    case 0:
        titulo="América do Sul";
        criarMapa(b);
        criarGrafico(titulo, '');
        first = false;
        break;        
    case 1:
        titulo="Índice de Desenvolvimento Humano";
       a=[0.811,0.675,0.733,0.819,0.719,0.724,0.728,0.862,0.741,0.741,0.684,0.792,0.748];
       b= { ARG: {fillKey: 'HIGH',}, 
            BOL: {fillKey: 'LOW',},
            BRA: {fillKey: 'MED',},
            CHL: {fillKey: 'HIGH',},
            COL: {fillKey: 'MED',},
            ECU: {fillKey: 'MED',},
            GUY: {fillKey: 'MED',},
            FGU: {fillKey: 'HIGH',},
            PRY: {fillKey: 'MED',},                     
            PER: {fillKey: 'MED',},
            SUR: {fillKey: 'LOW',},                     
            URY: {fillKey: 'HIGH',},                     
            VEN: {fillKey: 'MED',}     } ;
        criarMapa(b)
        criarGrafico(titulo, a);
        break;
    case 2:
        titulo="Produto Interno Bruto (per capita)";
        a=[17376,5099,12118,20114,10248,10055,5728,12165,7326,11148,9500,17466,13634];
        b= {ARG: {fillKey: 'MED',}, 
            BOL: {fillKey: 'LOW',},
            BRA: {fillKey: 'MED',},
            CHL: {fillKey: 'HIGH',},
            COL: {fillKey: 'MED',},
            ECU: {fillKey: 'MED',},
            GUY: {fillKey: 'LOW',},
            FGU: {fillKey: 'MED',},
            PRY: {fillKey: 'LOW',},                     
            PER: {fillKey: 'MED',},
            SUR: {fillKey: 'MED',},                     
            URY: {fillKey: 'MED',},                     
            VEN: {fillKey: 'MED',}     } ;
        criarMapa(b)
        criarGrafico(titulo, a);
        break;
    case 3:
        titulo="População por Km²";
        a=pa;
        b= {ARG: {fillKey: 'LOW',}, 
            BOL: {fillKey: 'LOW',},
            BRA: {fillKey: 'MED',},
            CHL: {fillKey: 'MED',},
            COL: {fillKey: 'HIGH',},
            ECU: {fillKey: 'HIGH',},
            GUY: {fillKey: 'LOW',},
            FGU: {fillKey: 'LOW',},
            PRY: {fillKey: 'MED',},                     
            PER: {fillKey: 'MED',},
            SUR: {fillKey: 'LOW',},                     
            URY: {fillKey: 'MED',},                     
            VEN: {fillKey: 'LOW',}     } ;
        criarMapa(b)
        criarGrafico(titulo, a);
        break;       
}
  
};
function criarMapa(b){
    var map = new Datamap({
        scope: 'world',
        element: document.getElementById('containerm'),
            fills: {
            HIGH: 'rgba(0,153,0,0.8)',
            MED:  'rgba(255,200,0,0.8)',  
            LOW: 'rgba(255,0,0,0.8)',
            defaultFill: 'rgba(13,13,255,0.8)'
        },                
            setProjection: function(element, b) {
            var projection = d3.geo.equirectangular()
              .center([-53.8, -21.5])
              .rotate([4.4, 0])
              .scale(500)
              .translate([element.offsetWidth / 2, element.offsetHeight / 2]);
            var path = d3.geo.path()
              .projection(projection);
            return {path: path, projection: projection};
        },
    data : b,                                   
    
        geographyConfig: {
            popupTemplate: function(geo, data) {
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
         done: function(datamap) {
        datamap.svg.selectAll('.datamaps-subunit').on('click', function (e) {
    $("#nome").html(e.properties.name);
    $("#pop").html('<i class="icon-user"></i>   População: ' + e.properties.populacao);
    $("#cap").html('<i class="icon-home"></i>   Capital: ' + e.properties.capital);
    $("#pib").html('<i class="icon-usd"></i>   PIB: US$ ' + e.properties.pib);
    $("#idh").html('<i class="icon-signal"></i>   IDH: ' + e.properties.idh);
    $("#area").html('<i class="icon-globe"></i>   Área Geográfica: ' + e.properties.area + ' km²'); 
    $("#pt1").html('<a title="' + e.properties.pt1t + '"><img src="' + e.properties.pt1 + '" alt="' + e.properties.pt1t + 'title="' + e.properties.pt1t + '">');
    $("#pt1t").html(e.properties.pt1t);
    $("#pt1x").html(e.properties.pt1x);
    $("#pt2").html('<a title="' + e.properties.pt2t + '"><img src="' + e.properties.pt2 + '" alt="' + e.properties.pt2t + 'title="' + e.properties.pt2t + '">');
    $("#pt2t").html(e.properties.pt2t);
    $("#pt2x").html(e.properties.pt2x);
    $("#pt3").html('<a title="' + e.properties.pt3t + '"><img src="' + e.properties.pt3 + '" alt="' + e.properties.pt3t + 'title="' + e.properties.pt3t + '">');
    $("#pt3t").html(e.properties.pt3t);
    $("#pt3x").html(e.properties.pt3x);
    $('#confirm')
        .modal({ backdrop: 'static', keyboard: false })
        .one('click', '[data-value]', function (e) {
        });
});
    },
    });
};
$('.box').hide();

    $('.voice').click(function(botao, first) {

  if ('webkitSpeechRecognition' in window) {
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
   recognition.onstart = function( e ) {
      console.log( e );

  };
  final_transcript = '';
  recognition.onresult = function( event ) {
    final_transcript = '';
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } 
    }
    document.getElementById( 'speech' ).value = final_transcript;
      if(final_transcript == 'i d h' || final_transcript == 'idh' || final_transcript == 'desenvolvimento humano' || final_transcript == 'índice de desenvolvimento humano'){
          botao = 1;
          selecionar(botao);
          recognition.stop();
      }
      else if(final_transcript == 'pib' || final_transcript == 'produto interno bruto'){
          botao = 2;
          selecionar(botao);
          recognition.stop();
      }
      else if(final_transcript == 'pop' || final_transcript == 'população' || final_transcript == 'população por quilômetro quadrado'){
          botao = 3;
          selecionar(botao);
          recognition.stop();
      }
  };
  recognition.start();
};
});

$('.clickme').each(function() {
    $(this).show(0).on('click', function(e) {
        e.preventDefault();
        $(this).next('.box').slideToggle('fast');
    });
});

        function criarGrafico(titulo, a){
        
$("#titulo").html(titulo);
            if (a != ''){
                $("#gra").html('<canvas id="myChart" width="550" height="400""></canvas>');
var data = {
	labels : ['Argentina', 'Bolívia', 'Brasil', 'Chile', 'Colômbia', 'Equador', 'Guiana', 'Guiana Francesa', 'Paraguai', 'Peru', 'Suriname', 'Uruguai', 'Venezuela'],
	datasets : [
		{
			fillColor : "rgba(13,13,255,0.8)",
			strokeColor : "rgba(60, 15, 250, 0.6)",
            data: a
        },
		
	]
}
options = {			
	scaleOverlay : false,
    scaleOverride : false,
	scaleSteps : null,
    scaleStepWidth : null,
	scaleStartValue : null,
	scaleLineColor : "rgba(0,0,0,.1)",
	scaleLineWidth : 1,
	scaleShowLabels : true,
	scaleLabel : "<%=value%>",
	scaleFontFamily : "'Arial'",
	scaleFontSize : 16,
    scaleFontStyle : "bold",
    scaleFontColor : "#000",	
	scaleShowGridLines : true,
	scaleGridLineColor : "rgba(0,0,0,.05)",
	scaleGridLineWidth : 1,	
	barShowStroke : true,
	barStrokeWidth : 2,
	barValueSpacing : 2,
	barDatasetSpacing : 2,
	animation : true,
	animationSteps : 60,
	animationEasing : "easeOutQuart",
	onAnimationComplete : null,
}
var ctx = document.getElementById("myChart").getContext("2d");
new Chart(ctx).Bar(data,options);
        };};
        
$('.bot').click(function() {
    botao = parseInt($(this).attr("value"));
        selecionar(botao);
});
        
document.addEventListener('DOMComponentsLoaded', function(){

    var deck = document.querySelector("#containerm");
    
    Hammer(deck).on("swipeleft", function () {
            botao++;
            selecionar(botao);
        });

    Hammer(deck).on("swiperight", function () {
            botao--;
            selecionar(botao);
        });
    
});	
        
document.addEventListener('DOMComponentsLoaded', function(){
        
    var buster = document.querySelector("#grafico");
    
    Hammer(buster).on("swipeleft", function () {
            botao++;
            selecionar(botao);
        });

    Hammer(buster).on("swiperight", function () {
            botao--;
            selecionar(botao);
        });
    
});	
});//]]>