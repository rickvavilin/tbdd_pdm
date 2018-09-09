DEFAULT_USER =  {
                'login': "",
                'display_name': "",
                'password': "",
                'password_confirmation': ""
            };
Vue.component('view-users', {
    template: '#view-users-template',
    data: function(){
        return {
            users: this.users==undefined ? [] : this.users,
            user_filter: this.user_filter,
            showmodal: this.showmodal,
            showedituser: this.showedituser,
            showchangepassword: this.showchangepassword,
            showdeleteconfirm: this.showdeleteconfirm==undefined ? false : this.showdeleteconfirm,
            current_user: this.current_user==undefined ? Object.assign({}, DEFAULT_USER) : this.current_user,
            messages: this.messages==undefined ? [] : this.messages,
        }
    },
    props: {
        userinfo : {}
    },
    mounted: function(){
        this.loadData();
    },
    methods: {
        havePermission: function(name){
            if ((this.userinfo==undefined) || (this.userinfo.user_permissions == undefined)){
                return false
            } else {
                return this.userinfo.user_permissions.indexOf(name)>=0
            }

        },

        loadData: function(){
            let params = {};
            if (this.user_filter) {
                params.simple_filter = this.user_filter;
            }
            api_fetch_json(['users'], {}, params).then(
                (data) => {
                    this.users = data.data;
                }
            )
        },
        saveNewUser: function(){
            if (this.current_user.password!=this.current_user.password_confirmation){
                this.messages.push('Пароль и подтверждение не совпадают');
                return
            }
            this.showmodal = false;
            api_post_json(['users'], this.current_user, {}).then(
                (data) =>{
                    this.loadData()
                }
            )
        },
        saveEditedUser: function(){
            this.showedituser = false;
            api_post_json(['users', this.current_user.login], this.current_user, {}).then(
                (data) =>{
                    this.loadData()
                }
            )
        },
        deleteUser: function(user){
            this.showdeleteconfirm = false;
            api_delete_json(['users', user.login], {}).then(
                (data) => {
                    this.loadData()
                }
            )
        },
        deleteUserConfirm: function(user){
            this.current_user = user;
            this.showdeleteconfirm = true;
        },
        editUser: function(user){
            this.showedituser = true;
            this.current_user = Object.assign({}, user);
        },
        addUser: function(){
            this.showmodal=true;
            this.current_user = Object.assign({}, DEFAULT_USER);
        },
        changePassword: function (user) {
            this.showchangepassword=true;
            this.messages = [];
            this.current_user = Object.assign({}, user);
        },
        saveChangedPassword: function(){
            if (this.current_user.password!=this.current_user.password_confirmation){
                this.messages.push('Пароль и подтверждение не совпадают');
                return
            }

            this.showchangepassword = false;
            let data = {

            };
            api_post_json(['users', 'password', this.current_user.login], this.current_user, {}).then(
                (data) =>{
                    this.loadData()
                }
            )

        }

    }
});