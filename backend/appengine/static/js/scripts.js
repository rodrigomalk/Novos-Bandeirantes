angular.module("app", []);
angular.module("app").factory("FacebookApi", function($http, $timeout){
	
	var api = {};

	api.logged = true;

	api.login = function(){
		FB.login(function(response){
			api.logged = true;
			FB.api("/me", function(response){
				$http.post("/rest/login/facebook",
				 {name: response.name, id: response.id});
			});
		});

	};

	api.logout = function(){
		FB.getLoginStatus(function(response){
			if(response.status === 'connected'){
				FB.logout(function(response){
					api.logged = false;
				});
			}
		});
	};

	api.is_logged = function(){
		FB.getLoginStatus(function(response){
			if(response.status === 'connected'){
				api.logged = true;
			}else{
				api.logged = false;
			}
		});

	};
	return api;
});
angular.module("app").controller("BaseController", function($scope, $window, FacebookApi){
	$scope.FacebookApi = FacebookApi;

	$window.onload = function(){
		FacebookApi.is_logged();
		$scope.$digest();
	};
	
	$scope.login = function(){
		FacebookApi.login();
	};

	$scope.logout = function(){
		FacebookApi.logout();	
	}
});