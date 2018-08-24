Vue.component('assembly-item', {
    template: "#assembly-item-template",
    computed: {
        plusClassObject: function(){
            return this.assembly.children.length>0 ? (this.expanded ? 'far fa-minus-square': 'far fa-plus-square'): 'fas fa-cog'
        }
    },
    data: function (){
        return {
            expanded: this.expanded==undefined ? false : this.expanded
        }
    },
    props: {
        assembly: Object,
        selected_assembly: undefined
    },
    methods: {
        clickSelect: function() {
            this.$emit('select', this.assembly);
        },
        selectChild: function(data){
            this.$emit('select', data);
        }
    }
});
Vue.component('view-assembly', {
    template: '#view-assembly-template',
    data: function () {
        return {
            assembly: this.assembly==undefined ? [] : this.assembly,
            assembly_filter: "",
            current_assembly: undefined,
            selected_assembly: undefined,
            details_list_visible: this.details_list_visible,
            details: this.details==undefined ? [] : this.details,
            detail_filter: ""
        }
    },
    props: {
        userinfo : {}
    },
    mounted: function(){
        this.loadData();
        this.loadDetails();
    },
    methods: {
        havePermission: function(name){
            if ((this.userinfo==undefined) || (this.userinfo.user_permissions == undefined)){
                return false
            } else {
                return this.userinfo.user_permissions.indexOf(name)>=0
            }

        },
        editAssembly: function(assembly){
            api_fetch_json(['assembly', 'tree', assembly.id], {}).then(
                (data) => {
                    this.current_assembly = data;
                }
            );

        },
        loadData: function(){
            let params = {};
            if (this.assembly_filter) {
                params.simple_filter = this.assembly_filter;
            }
            api_fetch_json(['assembly'], {}, params).then(
                (data) => {
                    this.assembly = data.data;
                }
            )
        },
        loadDetails: function(){
            let params = {};
            if (this.detail_filter) {
                params.simple_filter = this.detail_filter;
            }
            api_fetch_json(['details'], {}, params).then(
                (data) => {
                    this.details = data.data;
                }
            )
        },
        addDetailToAssembly: function (detail) {
            api_fetch_json([])
        },
        selectItem: function(data){
            console.log(data);
            this.selected_assembly = data;
        }
    }

});
