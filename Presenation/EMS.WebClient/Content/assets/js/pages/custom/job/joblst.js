"use strict";
var datatable;

var KTDatatableRecordSelectionDemo = function () {
    var options = {
        data: {
            type: 'remote',
            source: {
                read: {
                    method: 'POST',
                    url: '/job/joblst/',
                    map: function (raw) {
                        var dataSet = raw;
                        if (typeof raw.data !== 'undefined') {
                            dataSet = raw.data;
                        }
                        return dataSet;
                    },
                    timeout: 1000000,
                },
            },
            pageSize: 8,
            serverPaging: true,
            serverFiltering: true,
            serverSorting: true,
            saveState: { cookie: false } 
        },
        layout: {
            footer: false
        },
        sortable: true,
        pagination: true
    };

    var localSelectorDemo = function () {
        options.search = {
            input: $('#kt_datatable_search_query'),
            delay: 1000,
            key: 'generalSearch'
        };

        if (IsAdmin) {
            options.columns =
                [
                    {
                        field: '',
                        title: '#',
                        width: 20,
                        template: function (row, index) {
                            return index + 1;
                        }
                    },
                    {
                        field: 'Title',
                        title: 'Job Title',
                        width: 180,
                        template: function (row) {
                            var stateNo = KTUtil.getRandomInt(0, 7);
                            var states = [
                                'success',
                                'primary',
                                'danger',
                                'success',
                                'warning',
                                'dark',
                                'primary',
                                'info'];
                            var state = states[stateNo];

                            return '<div class="d-flex align-items-center">\
								<div class="symbol symbol-40 symbol-'+ state + ' flex-shrink-0">\
									<div class="symbol-label">' + row.Title.substring(0, 1) + '</div>\
								</div>\
								<div class="ml-2">\
									<div class="text-dark-75 font-weight-bold line-height-sm"></div>\
									<a href="#" class="font-size-sm text-dark-50 text-hover-primary">' + row.Title + '</a>\
								</div>\
							</div>';
                        }
                    },
                    {
                        field: 'Salary',
                        width: 75,
                        title: 'Salary',
                        template: function (row) {
                            return '<span> $ ' + row.Salary + '</span>';
                        }
                    },
                    {
                        field: 'Experience',
                        title: 'Exper.',
                        width: 80,
                    },
                    {
                        field: 'Vacancies',
                        title: '#Vacancies',
                        width: 110
                    },
                    {
                        field: 'CreatedDate',
                        title: 'Created On',
                        sortable: 'desc',
                        width: 110,
                        template: function (row) {
                            if (row.CreatedDate) {
                                var temp = convertToJavaScriptDate(new Date(parseInt(row.CreatedDate.replace(/[^0-9]/g, "")))).split(" ");
                                return '<span class="navi-text" style= "float:left; clear:left;">' + temp[0] + '</span>\
                                <span class="navi-text" style= "float:left; clear:left;">' + temp[1] + ' ' + temp[2] + '</span>';
                            }
                            else {
                                return '<span class="navi-text" style= "float:left; clear:left;">NA</span>\
                                <span class="navi-text" style= "float:left; clear:left;">NA</span>';
                            }

                        }
                    },
                    {
                        field: 'Actions',
                        title: 'Actions',
                        width: 120,
                        sortable: false,
                        overflow: 'visible',
                        textAlign: 'left',
                        autoHide: false,
                        template: function (row) {
                            if (IsAdmin) {
                                return '\<a onclick="Edit(' + row.Id + ')" class="btn btn-sm btn-clean btn-icon mr-2" title="Edit details">\
	                            <span class="svg-icon svg-icon-md">\
	                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">\
	                                    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">\
	                                        <rect x="0" y="0" width="24" height="24"/>\
	                                        <path d="M8,17.9148182 L8,5.96685884 C8,5.56391781 8.16211443,5.17792052 8.44982609,4.89581508 L10.965708,2.42895648 C11.5426798,1.86322723 12.4640974,1.85620921 13.0496196,2.41308426 L15.5337377,4.77566479 C15.8314604,5.0588212 16,5.45170806 16,5.86258077 L16,17.9148182 C16,18.7432453 15.3284271,19.4148182 14.5,19.4148182 L9.5,19.4148182 C8.67157288,19.4148182 8,18.7432453 8,17.9148182 Z" fill="#000000" fill-rule="nonzero"\ transform="translate(12.000000, 10.707409) rotate(-135.000000) translate(-12.000000, -10.707409) "/>\
	                                        <rect fill="#000000" opacity="0.3" x="5" y="20" width="15" height="2" rx="1"/>\
	                                    </g>\
	                                </svg>\
	                            </span>\
	                        </a>\
	                        <a onclick="Delete(' + row.Id + ')" class="btn btn-sm btn-clean btn-icon" title="Delete">\
	                            <span class="svg-icon svg-icon-md">\
	                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">\
	                                    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">\
	                                        <rect x="0" y="0" width="24" height="24"/>\
	                                        <path d="M6,8 L6,20.5 C6,21.3284271 6.67157288,22 7.5,22 L16.5,22 C17.3284271,22 18,21.3284271 18,20.5 L18,8 L6,8 Z" fill="#000000" fill-rule="nonzero"/>\
	                                        <path d="M14,4.5 L14,4 C14,3.44771525 13.5522847,3 13,3 L11,3 C10.4477153,3 10,3.44771525 10,4 L10,4.5 L5.5,4.5 C5.22385763,4.5 5,4.72385763 5,5 L5,5.5 C5,5.77614237 5.22385763,6 5.5,6 L18.5,6 C18.7761424,6 19,5.77614237 19,5.5 L19,5 C19,4.72385763 18.7761424,4.5 18.5,4.5 L14,4.5 Z" fill="#000000" opacity="0.3"/>\
	                                    </g>\
	                                </svg>\
	                            </span>\
	                        </a>\
	                    ';
                            }
                            else
                                return '';
                        }
                    }]
        }
        else {
            options.columns =
                [
                    {
                        field: '',
                        title: '#',
                        width: 20,
                        template: function (row, index) {
                            return index + 1;
                        }
                    },
                    {
                        field: 'Title',
                        title: 'Job Title',
                        width: 180,
                        template: function (row) {
                            var stateNo = KTUtil.getRandomInt(0, 7);
                            var states = [
                                'success',
                                'primary',
                                'danger',
                                'success',
                                'warning',
                                'dark',
                                'primary',
                                'info'];
                            var state = states[stateNo];

                            return '<div class="d-flex align-items-center">\
								<div class="symbol symbol-40 symbol-'+ state + ' flex-shrink-0">\
									<div class="symbol-label">' + row.Title.substring(0, 1) + '</div>\
								</div>\
								<div class="ml-2">\
									<div class="text-dark-75 font-weight-bold line-height-sm"></div>\
									<a href="#" class="font-size-sm text-dark-50 text-hover-primary">' + row.Title + '</a>\
								</div>\
							</div>';
                        }
                    },
                    {
                        field: 'Salary',
                        width: 100,
                        title: 'Salary',
                        template: function (row) {
                            return '<span> $ ' + row.Salary + '</span>';
                        }
                    },
                    {
                        field: 'Experience',
                        title: 'Exper.',
                        width: 110,
                    },
                    {
                        field: 'Vacancies',
                        title: '#Vacancies',
                        width: 110
                    },
                    {
                        field: 'CreatedDate',
                        title: 'Created On',
                        sortable: 'desc',
                        width: 200,
                        template: function (row) {
                            if (row.CreatedDate) {
                                var temp = convertToJavaScriptDate(new Date(parseInt(row.CreatedDate.replace(/[^0-9]/g, "")))).split(" ");
                                return '<span class="navi-text" style= "float:left; clear:left;">' + temp[0] + '</span>\
                                <span class="navi-text" style= "float:left; clear:left;">' + temp[1] + ' ' + temp[2] + '</span>';
                            }
                            else {
                                return '<span class="navi-text" style= "float:left; clear:left;">NA</span>\
                                <span class="navi-text" style= "float:left; clear:left;">NA</span>';
                            }

                        }
                }
            ]
        }

        datatable = $('#kt_datatable').KTDatatable(options);

        $('#kt_datatable_search_status').on('change', function () {
            datatable.search($(this).val(), 'status');
        });

        $('#kt_datatable_search_status, #kt_datatable_search_type').selectpicker();

        datatable.on('datatable-on-check datatable-on-uncheck', function (e) {
            var checkedNodes = datatable.rows('.datatable-row-active').nodes();
            var count = checkedNodes.length;
        });

        datatable.on('click', '[data-record-id]', function () {
            localStorage.clear();
        });
    };

    return {
        // public functions
        init: function () {
            localSelectorDemo();
        },
    };
}();
jQuery(document).ready(function () {
    localStorage.clear();
    KTDatatableRecordSelectionDemo.init();
});
function convertToJavaScriptDate(value) {
    var dt = value;
    var hours = dt.getHours();
    var minutes = dt.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' + minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return ((dt.getMonth()) + 1) + "/" + dt.getDate() + "/" + dt.getFullYear() + " " + strTime;
}
function Edit(Id) {
    window.location.href = "/Job/Edit?Id=" + Id;
}
function Delete(Id) {
    Swal.fire({
        title: "Are you sure you want delete this Job ?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "No, cancel!",
        reverseButtons: true
    }).then(function (result) {
        if (result.value) {
            KTApp.blockPage();
            $.ajax({
                url: "/job/deletejob?Id=" + Id,
                type: "GET",
                dataType: 'json',
                contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
                success: function (response) {
                    KTApp.unblockPage();
                    if (response.Success) {
                        datatable.reload();
                        KTUtil.scrollTop();
                        toastr.options = {
                            "closeButton": false,
                            "debug": false,
                            "newestOnTop": true,
                            "progressBar": false,
                            "positionClass": "toast-bottom-left",
                            "preventDuplicates": false,
                            "onclick": null,
                            "showDuration": "300",
                            "hideDuration": "1000",
                            "timeOut": "5000",
                            "extendedTimeOut": "1000",
                            "showEasing": "swing",
                            "hideEasing": "linear",
                            "showMethod": "fadeIn",
                            "hideMethod": "fadeOut"
                        };

                        toastr.success("Job has been deleted successfully!");
                    }
                    else {
                        toastr.options = {
                            "closeButton": false,
                            "debug": false,
                            "newestOnTop": true,
                            "progressBar": false,
                            "positionClass": "toast-bottom-left",
                            "preventDuplicates": false,
                            "onclick": null,
                            "showDuration": "300",
                            "hideDuration": "1000",
                            "timeOut": "5000",
                            "extendedTimeOut": "1000",
                            "showEasing": "swing",
                            "hideEasing": "linear",
                            "showMethod": "fadeIn",
                            "hideMethod": "fadeOut"
                        };

                        toastr.error("Something went wrong!");
                    }
                }
            });
        }
    });
}
function DeleteAll() {
    Swal.fire({
        title: "Are you sure you want delete all jobs ?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "No, cancel!",
        reverseButtons: true
    }).then(function (result) {
        if (result.value) {
            KTApp.blockPage();
            $.ajax({
                url: "/Job/DeleteAll/",
                type: "DELETE",
                success: function (response) {
                    KTApp.unblockPage();
                    if (response.Success) {
                        datatable.reload();
                        KTUtil.scrollTop();
                        toastr.options = {
                            "closeButton": false,
                            "debug": false,
                            "newestOnTop": true,
                            "progressBar": false,
                            "positionClass": "toast-bottom-left",
                            "preventDuplicates": false,
                            "onclick": null,
                            "showDuration": "300",
                            "hideDuration": "1000",
                            "timeOut": "5000",
                            "extendedTimeOut": "1000",
                            "showEasing": "swing",
                            "hideEasing": "linear",
                            "showMethod": "fadeIn",
                            "hideMethod": "fadeOut"
                        };

                        toastr.success("Job has been deleted successfully!");
                    }
                    else {
                        toastr.options = {
                            "closeButton": false,
                            "debug": false,
                            "newestOnTop": true,
                            "progressBar": false,
                            "positionClass": "toast-bottom-left",
                            "preventDuplicates": false,
                            "onclick": null,
                            "showDuration": "300",
                            "hideDuration": "1000",
                            "timeOut": "5000",
                            "extendedTimeOut": "1000",
                            "showEasing": "swing",
                            "hideEasing": "linear",
                            "showMethod": "fadeIn",
                            "hideMethod": "fadeOut"
                        };

                        toastr.error("Something went wrong!");
                    }
                }
            });
        }
    });
}