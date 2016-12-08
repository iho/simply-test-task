'use strict';
var url = window.location.hostname;
if (window.location.port) {
    url = url + ':' + window.location.port
}

var basicChat = angular.module('BasicChat', ['ngRoute']);
basicChat.config(function($routeProvider) {
    $routeProvider
        .when("/", {
            templateUrl: "/static/main.html",
            controller: "MainController"
        })
        .when("/chat/:roomId", {
            templateUrl: "/static/chat.html",
            controller: "ChatController"
        })
        .when("/rooms", {
            templateUrl: "/static/rooms.html",
            controller: "RoomsController"
        })
});

basicChat.controller('MainController', ['$scope', '$http', function($scope, $http) {
    $scope.Submit = function() {
        document.username = $scope.username;
        document.password = $scope.password;
        $http.get('http://' + url + '/admins').then(function(response) {
            if (response.data, response.data.indexOf($scope.username) > -1) {
                $scope.showEdit = true;
            }
            $http.get('http://' + url + '/room').then(function(response) {
                $scope.rooms = response.data;
            })
        })
    }
}])

basicChat.controller('ChatController', ['$routeParams', '$scope', '$http', function($routeParams, $scope, $http) {
    $http.get('http://' + url + '/admins').then(function(response) {
        $scope.admins = response.data;
    })
    $scope.checkIfAdmin = function(username) {
        if ($scope.admins.indexOf(username) > -1) {
            return true;
        }
        return false;
    }

    var username = document.username || 'username' + Math.floor((Math.random() * 10) + 1);
    var ws = new ReconnectingWebSocket('ws://' + url + '/ws');
    $http.get('http://' + url + '/message/' + $routeParams.roomId).then(function(response) {
        $scope.messages = response.data;
    });

    $scope.status = "";
    ws.onmessage = function(evt) {
        var message = JSON.parse(evt.data);
        if (message.room_id == $routeParams.roomId) {
            $scope.messages.push(message);
            setTimeout(function() {
                chatmessages.scrollTop = chatmessages.scrollHeight;
            }, 10);
        }
    };

    var chatmessages = document.querySelector(".chat-messages");

    $scope.send = function() {
        $http.post('http://' + url + '/message/' + $routeParams.roomId, {
            "username": username,
            "text": $scope.textbox
        })
        $scope.status = "sending";
        $scope.textbox = "";
        setTimeout(function() {
            $scope.status = ""
        }, 1200);
    };

}]);


basicChat.controller('RoomsController', ['$http', '$scope', function($http, $scope) {
    var password = document.password;

    var updateRooms = function() {
        $http.get('http://' + url + '/room').then(function(response) {
            $scope.rooms = response.data;
        });
    }

    updateRooms()
    $scope.addItem = function() {
        var room = {};
        room.name = $scope.name;
        room.theme = $scope.theme;
        room.password = password;
        $http.post('http://' + url + '/room', room).then(function() {
            $scope.name = '';
            $scope.theme = '';
            updateRooms()
        })
    }
    $scope.removeItem = function(id) {

        $http.delete('http://' + url + '/room/' + id, {
            'data': JSON.stringify({
                'password': password
            })
        }).then(function() {
            updateRooms()
        })
    }

}]);


