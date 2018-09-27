$().ready(function(){
   app = new Vue({
       el: '#vueroot',
       data: {
           current_view: undefined,
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
                       this.loginform.login = '';
                       this.loginform.password = '';
                       this.checkLoggedIn();
                       //this.userinfo = data;
                   }
               )
           },
           doLogout: function(){
               $('#logoutModal').modal('hide');
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
           },
           parseHash: function(){
               this.current_view = window.location.hash.substr(1);
           }

       }
   });
    app.checkLoggedIn();
    app.parseHash();
    window.onhashchange = app.parseHash;

});