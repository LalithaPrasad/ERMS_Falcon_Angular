var app=angular.module("ermsapp",["ngRoute"]);
app.directive('autoFocus', function($timeout) {
    return {
        restrict: 'AC',
        link: function(_scope, _element) {
            $timeout(function(){
                _element[0].focus();
            }, 0);
        }
    };
});
app.config(['$routeProvider','$locationProvider',function($routeProvider,$locationProvider){
    $routeProvider
    .when("/",{
        templateUrl:"/static/html/login.html",
        controller:"Login_Ctrl"
    })
    .when("/logout",{
        template:"",
        controller:"Logout_Ctrl"
    })
    .when("/signup",{
        templateUrl:"/static/html/signup.html",
        controller:"Signup_Ctrl"
    })
    .when("/employee_menu",{
        templateUrl:"/static/html/employee_menu.html",
    })
    .when("/add_employee",{
        templateUrl:"/static/html/add_employee.html",
        controller:"Add_Employee_Ctrl"
    })
    .when("/delete_employee",{
        templateUrl:"/static/html/delete_employee.html",
        controller:"Delete_Employee_Ctrl"
    })
    .when("/modify_employee",{
        templateUrl:"/static/html/modify_employee.html",
        controller:"Modify_Employee_Ctrl"
    })
    .when("/display_employees",{
        templateUrl:"/static/html/display_employees.html",
        controller:"Display_Employees_Ctrl"
    })
    .otherwise({
        resirectTo:"/"
    });
    $locationProvider.html5Mode({enabled:true,requireBase:false});
}]);
app.controller("Login_Ctrl",
    ["$rootScope","$scope","$location","$http","$window",function($rootScope,$scope,$location,$http,$window){
    $scope.submit_login_form=function(){
        var un=$scope.username;
        var pw=$scope.password;
        var url="http://localhost:8000/token";
        $http.get(url,{params:{"username":un,"password":pw}})
        .then(function(response){
            if(response.data.message=="NoData"){
                $window.alert("No data was passed");
                $location.path("/logout");
            }
            else if(response.data.message=="InvalidUser"){
                $window.alert("Invalid user");
                $location.path("/logout");
            }
            else{
                $rootScope.token=response.data.token;
                $location.path("/employee_menu");
            }
        },function(response){
            $window.alert(response.statusText);
        });
    };
}]);
app.controller("Signup_Ctrl",
    ["$scope","$http","$window","$location", function($scope,$http,$window,$location){
    $scope.submit_signup_form=function(){
        var un=$scope.username;
        var pw=$scope.password;
        var pw2=$scope.password2;
        if(pw!=pw2){
            $window.alert("Passwords don't match");
        }
        else{
            var url="http://localhost:8000/admin";
            $http.post(url,{"username":un,"password":pw})
            .then(function(response){
                if(response.data.message=="NoData"){
                    $window.alert("No data was passed");
                    $location.path("/logout");
                }
                else if(response.data.message=="AdminExists"){
                    $window.alert("Admin aleready created");
                    $location.path("/logout");
                }
                else{
                    $window.alert(response.data.message);
                    $location.path("/logout");
                }
            },function(response){
                $window.alert(response.statusText);
            });
        };
    };
}]);
app.controller("Add_Employee_Ctrl",
    ["$rootScope","$scope","$http","$window","$location", function($rootScope,$scope,$http,$window,$location){
    $scope.submit_add_employee_form=function(){
        var n=$scope.name;
        var a=$scope.age;
        var e=$scope.ed;
        var r=$scope.role;
        var data={"name":n,"age":a,"ed":e,"role":r}
        var url="http://localhost:8000/employee";
        $http.post(url, JSON.stringify(data), {headers:{"token":$rootScope.token}})
        .then(function(response){
            if(response.data.message=="NoData"){
                $window.alert("No data was passed");
                $location.path("/employee_menu");
            }
            else if(response.data.message=="InvalidToken"){
                $window.alert("Invalid credentials");
                $location.path("/logout");
            }
            else{
                $window.alert(response.data.message);
                $location.path("/employee_menu");
            }
        },function(response){
            $window.alert(response.statusText);
        });
    };
}]);
app.controller("Delete_Employee_Ctrl",
    ["$rootScope","$scope","$http","$window","$location", function($rootScope,$scope,$http,$window,$location){
    $scope.submit_delete_employee_form=function(){
        var config={params:{"id":$scope.id},headers:{"token":$rootScope.token}};
        var url="http://localhost:8000/employee";
        $http.delete(url,config)
        .then(function(response){
            if(response.data.message=="NoData"){
                $window.alert("No data was passed");
                $location.path("/employee_menu");
            }
            else if(response.data.message=="InvalidToken"){
                $window.alert("Invalid credentials");
                $location.path("/logout");
            }
            else{
                $window.alert(response.data.message);
                $location.path("/employee_menu");
            }
        },function(response){
            $window.aler(response.statusText);
        });
    };
}]);
app.controller("Modify_Employee_Ctrl",
    ["$rootScope","$scope","$http","$window","$location", function($rootScope,$scope,$http,$window,$location){
    $scope.submit_modify_employee_form=function(){
        data={};
        data.id=$scope.id;
        if($scope.ed)data.ed=$scope.ed;
        if($scope.role)data.role=$scope.role;
        var url="http://localhost:8000/employee";
        $http.put(url,data,{headers:{"token":$rootScope.token}})
        .then(function(response){
            if(response.data.message=="NoData"){
                $window.alert("No data was passed");
                $location.path("/employee_menu");
            }
            else if(response.data.message=="InvalidToken"){
                $window.alert("Invalid credentials");
                $location.path("/logout");
            }
            else{
                $window.alert(response.data.message);
                $location.path("/employee_menu");
            }
        },function(response){
            $window.alert(response.statusText);
        });
    };
}]);
app.controller("Display_Employees_Ctrl",
    ["$rootScope","$scope","$http",function($rootScope,$scope,$http){
    var url="http://localhost:8000/employee";
    $http.get(url,{headers:{"token":$rootScope.token}})
    .then(function(response){
        if(response.data.message=="EmployeeDBEmpty"){
            $scope.nodata=true;
        }
        else{
            $scope.nodata=false;
            $scope.employees=response.data;
        }
    },function(reponse){
        $window.alert(response.statusText);
    });
}]);
app.controller("Logout_Ctrl",
    ["$http","$window","$location",function($http,$window,$location){
    var url="http://localhost:8000/token";
    $http.put(url)
    .then(function(response){
        $location.path("/");
    },function(response){
        $window.alert(response.statusText)
    });
}]);
