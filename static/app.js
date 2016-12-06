'use strict';

var basicChat = angular.module('BasicChat', ['chat', 'ngRoute']);
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
        $http.get('http://0.0.0.0:8080/admins').then(function(response) {
            if (response.data, response.data.indexOf($scope.username) > -1) {
                $scope.showEdit = true;
            }
            $http.get('http://0.0.0.0:8080/room').then(function(response) {
                $scope.rooms = response.data;
            })
        })
    }
}])

basicChat.controller('ChatController', ['$routeParams', '$scope', '$http', function($routeParams, $scope, $http) {
    console.log($routeParams, $routeParams.roomId, document.username);
    $http.get('http://0.0.0.0:8080/admins').then(function(response) {
        $scope.admins = response.data;
    })
    $scope.checkIfAdmin = function(username) {
        if ($scope.admins.indexOf(username) > -1) {
            console.log(username, $scope.admins.indexOf(username) > -1);
            return true;
        }
        return false;
    }

    var username = document.username || 'username' + Math.floor((Math.random() * 10) + 1);
    var ws = new ReconnectingWebSocket('ws://0.0.0.0:8080/ws');
    $http.get('http://0.0.0.0:8080/message/' + $routeParams.roomId).then(function(response) {
        $scope.messages = response.data;
    });

    $scope.status = "";
    ws.onmessage = function(evt) {
        $scope.messages.push(JSON.parse(evt.data));
        setTimeout(function() {
            chatmessages.scrollTop = chatmessages.scrollHeight;
        }, 10);
    };

    var chatmessages = document.querySelector(".chat-messages");

    $scope.send = function() {
        $http.post('http://0.0.0.0:8080/message/' + $routeParams.roomId, {
                "username": username,
                "text": $scope.textbox
            })
            .then(function(response) {
                console.log('message sent')
            })

        $scope.status = "sending";
        $scope.textbox = "";
        setTimeout(function() {
            $scope.status = ""
        }, 1200);
    };

}]);


basicChat.controller('RoomsController', ['$http', '$scope', function($http, $scope) {

    var updateRooms = function() {
        $http.get('http://0.0.0.0:8080/room').then(function(response) {
            $scope.rooms = response.data;
        });
    }

    updateRooms()
    $scope.addItem = function() {
        var room = {};
        room.name = $scope.name;
        room.theme = $scope.theme;
        room.password = 'password' // TODO
        console.log(room);
        $http.post('http://0.0.0.0:8080/room', room).then(function() {
            $scope.name = '';
            $scope.theme = '';
            updateRooms()
        })
    }
    $scope.removeItem = function(id) {

        $http.delete('http://0.0.0.0:8080/room/' + id, {
            'data': JSON.stringify({
                'password': 'password'
            })
        }).then(function() {
            updateRooms()
        })
    }

}]);
