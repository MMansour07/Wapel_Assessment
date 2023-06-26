"use strict";
var datatable;

String.prototype.replaceAll = function (str1, str2, ignore) {
    return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g, "\\$&"), (ignore ? "gi" : "g")), (typeof (str2) == "string") ? str2.replace(/\$/g, "$$$$") : str2);
}

var KTDatatableRecordSelectionDemo = function () {

    var options = {
        data: {
            type: 'remote',
            source: {
                read: {
                    method: 'GET',
                    url: '/rating/ratinglst/',
                    timeout: 1000000,
                },
            },
            pageSize: 8,
            serverPaging: false,
            serverFiltering: false,
            serverSorting: false,
            saveState: { cookie: false }
        },
        layout: {
            footer: false
        },
        sortable: true,
        pagination: true
    };
    // basic demo
    var localSelectorDemo = function () {
        options.search = {
            input: $('#kt_datatable_search_query'),
            delay: 1000,
            key: 'generalSearch'
        };

        options.columns = [
                {
                    field: '',
                    title: '#',
                    width: 50,
                    template: function (row, index) {
                        return index + 1;
                    }
                },
                {
                    field: 'User',
                    title: 'User',
                    width: 150,
                },
                {
                    field: 'Task.Name',
                    title: 'Task',
                    sortable: 'desc',
                    width: 100,
                },
                {
                    field: 'TotalScore',
                    title: 'Total Score',
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

                        return '\<a onclick="Details(/' + row.Id + '/)" class="btn btn-sm btn-clean btn-icon mr-2" title="Edit details">\
	                        <span class="svg-icon svg-icon-primary svg-icon-2x">\
                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">\
                                <g stroke = "none" stroke - width="1" fill = "none" fill - rule="evenodd" >\
                                        <rect x="0" y="0" width="24" height="24"/>\
                                        <circle fill="#000000" opacity="0.3" cx="12" cy="12" r="10"/>\
                                        <rect fill="#000000" x="11" y="10" width="2" height="7" rx="1"/>\
                                        <rect fill="#000000" x="11" y="7" width="2" height="2" rx="1"/>\
                                    </g>\
                            </svg>\
                            </span >\
	                        </a>\
	                    ';
                    }
                }]


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



function Details(Id) {
    window.location.href = "/Rating/Details?Id=" + Id.toString().replaceAll("/", "") + "&isgeneral="+ true;
}
