$().ready(function(){
   app = new Vue({
       el: '#vueroot',
       data: {
           logged_in: false,
           app_loaded: false,
           loginform: {
               login: undefined,
               password: undefined
           },
           userinfo: {
                login:""
           }
       },
       methods: {
           doLogin: function(){
               api_login(this.loginform.login, this.loginform.password).then(
                   (data) => {
                       this.checkLoggedIn();
                       //this.userinfo = data;
                   }
               )
           },
           doLogout: function(){
               api_logout().then(
                   (data) => {
                       this.checkLoggedIn();
                   }
               )
           },
           checkLoggedIn: function(){
               api_loggedin().then(
                   (data) => {
                       this.app_loaded = true;
                       this.logged_in = data.result;
                       if (this.logged_in){
                           this.userinfo = data.userinfo;
                       } else {
                           this.userinfo.login = '';
                       }
                   }
               )
           }
       }
   });
    app.checkLoggedIn();

});