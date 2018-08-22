Vue.component('view-details', {
    template: '#view-details-template',
    data: function () {
        return  {
            details: this.details
        }
    },
    methods: {
        loadData:function(){
            api_fetch_json(['details'], {}).then(
                (data) => {
                    this.details = data.data;
                }
            )

        }
    }
});