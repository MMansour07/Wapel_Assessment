"use strict";
var myDropzone4;
var KTDropzoneDemo = function () {
    // Private functions
    var InitFileUploader = function () {
        // set the dropzone container id
        var id = '#kt_dropzone_4';
        var $btnLabel = $(id + ' .dropzone-select');
        // set the preview element template
        var previewNode = $(id + " .dropzone-item");
        previewNode.id = "";
        var previewTemplate = previewNode.parent('.dropzone-items').html();
        previewNode.remove();

        myDropzone4 = new Dropzone(id, { // Make the whole body a dropzone
            url: "/ajax_file_upload_handler/", // Set the url for your upload script location
            parallelUploads: 20,
            maxFiles: 3,
            previewTemplate: previewTemplate,
            acceptedFiles: 'video/*',
            dictDuplicateFile: "Duplicate Files Cannot Be Uploaded",
            preventDuplicates: true,
            maxFilesize: 100, // Max filesize in MB
            autoQueue: false, // Make sure the files aren't queued until manually added
            previewsContainer: id + " .dropzone-items", // Define the container to display the previews
            clickable: id + " .dropzone-select" // Define the element that should be used as click trigger to select files.
        });

        myDropzone4.on("addedfile", function (file) {

            if (myDropzone4.getAcceptedFiles().length <= 3) {
                $(document).find(id + ' .dropzone-item').css('display', '');
                $(id + " .dropzone-items").append('<input type="text" id="' + file.name.replace(/[^a-zA-Z0-9]/g, '') + '" name="videoTitle" class="form-control form-control-sm mt-1 col" maxlength="30" placeholder="Title (Max 30 chars)">');
                $(id + " .dropzone-upload, " + id + " .dropzone-remove-all").css('display', 'inline-block');

                setTimeout(function () { $(id + " .progress-bar").css('opacity', '1') }, 100);

                var thisProgressBar = id + " .dz-complete";
                setTimeout(function () { $(thisProgressBar + " .progress-bar, " + thisProgressBar + " .progress, " + thisProgressBar + " .dropzone-start").css('opacity', '0') }, 1500);

                $btnLabel.text("Add more files");
                $('.val-cnt').css('display', 'none');
            }
        });

        // Setup the button for remove all files
        document.querySelector(id + " .dropzone-remove-all").onclick = function () {
            $(id + " .dropzone-upload, " + id + " .dropzone-remove-all").css('display', 'none');
            myDropzone4.removeAllFiles(true);
        };

        // On all files removed
        myDropzone4.on("removedfile", function (file) {
            $("#" + file.name.replace(/[^a-zA-Z0-9]/g,'')).remove();

            if (myDropzone4.files.length < 1) {
                $(id + " .dropzone-upload, " + id + " .dropzone-remove-all").css('display', 'none');
                $btnLabel.text("Attach files");
            }
        });
    }

    var _handlejobform = function () {
        var form = KTUtil.getById('kt_job');
        if (!form) {
            return;
        }

        var validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    Title: {
                        validators: {
                            notEmpty: {
                                message: 'Required Field'
                            }
                        }
                    },
                    Salary: {
                        validators: {
                            notEmpty: {
                                message: 'Required Field'
                            }
                        }
                    },
                    Experience: {
                        validators: {
                            notEmpty: {
                                message: 'Required Field'
                            }
                        }
                    },
                    Vacancies: {
                        validators: {
                            notEmpty: {
                                message: 'Required Field'
                            }
                        }
                    },
                    videoTitle: {
                        validators: {
                            callback: function (input) {
                                return true;
                            }
                        }
                    },
                    Description: {
                        validators: {
                            notEmpty: {
                                message: 'Required Field'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            });

        var VidelVal = function () {
            if (myDropzone4.getAcceptedFiles().length == 0)
                $('.val-cnt').css('display', '');
            else
                $('.val-cnt').css('display', 'none');
        }


        $("#kt_job").on("submit", function () {
            VidelVal();
            if (validator) {
                validator.validate().then(function (status) {
                    if (status == 'Valid' && myDropzone4.getAcceptedFiles().length > 0) {
                        KTApp.blockPage();
                        $.ajax({
                            url: "/job/CreateJob",
                            type: "POST",
                            contentType: false, // Not to set any content header
                            processData: false, // Not to process data 
                            data: getValues(),
                            success: function (response) {
                                KTApp.unblockPage();
                                if (response.Success) {
                                    KTUtil.scrollTop();
                                    window.location.href = '/user/land/';
                                }
                                else if (!response.Success) {
                                    alert(response.Message);
                                }
                                else {
                                    $("#job_container").html(response);
                                }
                            }
                        });
                    }
                });
            }
            return false;
        });
    }

    function getValues() {
        var jObject = JSON.parse('{"' + decodeURI(JSON.stringify($("#kt_job").serialize()).substring(1)).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g, '":"') + '"}');
        var Titles = new Array();
        for (var i = 0; i < myDropzone4.files.length; i++) {
            Titles.push($("#" + myDropzone4.files[i].name.replace(/[^a-zA-Z0-9]/g,'')).val());
        }
        delete jObject.videoTitle;
        /*var headers = { __RequestVerificationToken: jObject["__RequestVerificationToken"] };*/
        var formData = new FormData();

        for (var key in jObject) {
            formData.append(key, jObject[key]);
        }
        for (var i = 0; i < Titles.length; i++) {
            formData.append("Titles", (Titles[i] ? Titles[i] : myDropzone4.getAcceptedFiles()[i].name.replace(/[^a-zA-Z0-9]/g,'')));
        }
        for (var i = 0; i < myDropzone4.getAcceptedFiles().length; i++) {
            formData.append('Files', myDropzone4.getAcceptedFiles()[i]);
        }
        return formData;
    }
    return {
        // public functions
        init: function () {
            Dropzone.autoDiscover = false;
            InitFileUploader();
            _handlejobform();
        }
    };
}();
KTUtil.ready(function () {

    Dropzone.prototype.isFileExist = function (file) {
        var i;
        if (this.files.length > 0) {
            for (i = 0; i < this.files.length; i++) {
                if (this.files[i].name === file.name
                    && this.files[i].size === file.size
                    && this.files[i].lastModifiedDate.toString() === file.lastModifiedDate.toString()) {
                    return true;
                }
            }
        }
        return false;
    };

    Dropzone.prototype.addFile = function (file) {
        file.upload = {
            progress: 0,
            total: file.size,
            bytesSent: 0
        };
        if (this.options.preventDuplicates && this.isFileExist(file)) {
            alert(this.options.dictDuplicateFile);
            return;
        }
        this.files.push(file);
        file.status = Dropzone.ADDED;
        this.emit("addedfile", file);
        this._enqueueThumbnail(file);
        return this.accept(file, (function (_this) {
            return function (error) {
                if (error) {
                    file.accepted = false;
                    _this._errorProcessing([file], error);
                } else {
                    file.accepted = true;
                    if (_this.options.autoQueue) {
                        _this.enqueueFile(file);
                    }
                }
                return _this._updateMaxFilesReachedClass();
            };
        })(this));
    };

    KTDropzoneDemo.init();
});
