const DEFAULT_DETAIL = {
                id: undefined,
                code: "",
                name: "",
                description: "",
                is_standard: false,
                files: []
            };
Vue.component('view-details', {
    template: '#view-details-template',
    data: function () {
        return  {
            details: this.details==undefined ? [] : this.details,
            showmodal: this.showmodal==undefined ? false : this.showmodal,
            showdeleteconfirm: this.showdeleteconfirm==undefined ? false : this.showdeleteconfirm,
            current_detail: this.current_detail==undefined ? Object.assign({}, DEFAULT_DETAIL) : this.current_detail,
            messages: this.messages==undefined ? [] : this.messages,
            detail_filter: this.detail_filter
        }
    },
    mounted: function(){
        var self = this;
        window.addEventListener("dragenter", function (e) {
            self.filedraggedon = true;
        });

        window.addEventListener("dragleave", function (e) {
          e.preventDefault();
            self.filedraggedon = false;
        });

        window.addEventListener("dragover", function (e) {
          e.preventDefault();
            self.filedraggedon = true;
        });

        window.addEventListener("drop", function (e) {
            e.preventDefault();
            var files = e.dataTransfer.files;
            console.log("Drop files:", files);

            for (var file of files){
                self.uploadFile(file);
                self.files_to_upload.push(file);
            }
        });
        this.loadData()
    },
    methods: {
        uploadFile: function(file){
            let formData = new FormData();
            formData.append(file.name, file);
            api_fetch(['details', this.current_detail.id, 'files'], {
                method: "POST",
                body: formData
            }).then(
                (response) => {
                    if ((response.status>=200) && (response.status<300)) {
                        return response.json()
                    } else {
                        throw response.json()
                    }
                }
            ).then((data) => {
                this.editDetail(this.current_detail);
            }).catch((e) => {
                e.then(
                    (data) => {
                        this.messages.push({
                           text: data.result
                        });
                    }
                )
            })
        },
        deleteFile: function(file){
            api_delete_json(['details', this.current_detail.id, 'files', file.name], {}).then(
                (data) =>{
                    this.editDetail(this.current_detail);
                }
            )
        },
        loadData: function(){
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
        addDetail: function(){
            this.current_detail = Object.assign({}, DEFAULT_DETAIL);
            this.showmodal = true;
        },
        editDetail: function(detail){
            api_fetch_json(['details', detail.id], {}).then(
            (data) => {
                this.current_detail = data;
                this.showmodal = true;
            });
        },
        deleteDetail: function(detail){
            this.showdeleteconfirm = false;
            api_delete_json(['details', detail.id], {}).then(
                (data) => {
                    this.loadData()
                }
            )
        },
        deleteDetailConfirm: function(detail){
            this.current_detail = detail;
            this.showdeleteconfirm = true;
        },
        saveCurrent: function(close_modal){
            var url_elements = ['details'];
            if (this.current_detail.id!=undefined){
                url_elements.push(this.current_detail.id)
            }
            api_post_json(url_elements, this.current_detail, {}).then(
                (data) => {
                    this.showmodal = !close_modal;
                    this.current_detail = data;
                    this.loadData()
                }
            )

        }
    }
});