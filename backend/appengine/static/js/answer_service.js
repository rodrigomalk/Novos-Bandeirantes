angular.module("answer_service", []).factory('AnswerService', function($http){

    var answer_url = '/rest/answer/answer_question';
    var api = {};
    api.answer = function(answer, tries, quest_id){
        return $http.post(answer_url, {answer: answer, tries: tries, quest_id: quest_id})
    };

    return api;
});