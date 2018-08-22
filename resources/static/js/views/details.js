const DEFAULT_DETAIL = {
                id: undefined,
                code: "",
                name: "",
                description: "",
                is_standard: false
            };
Vue.component('view-details', {
    template: '#view-details-template',
    data: function () {
        return  {
            details: this.details==undefined ? [] : this.details,
            showmodal: this.showmodal==undefined ? false : this.showmodal,
            current_detail: this.current_detail==undefined ? Object.assign({}, DEFAULT_DETAIL) : this.current_detail //TODO: copy object DEFAULT_DETAIL
        }
    },
    mounted: function(){
        this.loadData()
    },
    methods: {
        loadData: function(){
            api_fetch_json(['details'], {}).then(
                (data) => {
                    this.details = data.data;
                }
            )
        },
        addDetail: function(){
            this.current_detail = Object.assign({}, DEFAULT_DETAIL); //TODO: copy object
            this.showmodal = true;
        },
        editDetail: function(detail){
            this.current_detail = Object.assign({}, detail);
            this.showmodal = true;
        },
        deleteDetail: function(detail){
            api_delete_json(['details', detail.id], {}).then(
                (data) => {
                    this.loadData()
                }
            )
        },
        saveCurrent: function(){
            var url_elements = ['details'];
            if (this.current_detail.id!=undefined){
                url_elements.push(this.current_detail.id)
            }
            api_post_json(url_elements, this.current_detail, {}).then(
                (data) => {
                    this.showmodal = false;
                    this.loadData()
                }
            )

        }
    }
});