"use strict";

function CriteriaChanged() {
    var selectedVal = document.getElementById("kt_select2").value;
    $.ajax({
        url: "/rating/GetTasksByCritriaId?TaskCriteridId=" + selectedVal,
        type: "GET",
        data: {},
        success: function (response) {
            KTApp.unblockPage();
            if (response.Success) {
                KTUtil.scrollTop();

                $('#kt_select')
                    .find('option')
                    .remove()
                    .end();

                var sel = $('#kt_select');
                $.each(response.Data, function (i, value) {
                    sel.append('<option value="' + value.Id + '" text = "' + value.Name + '" >' + value.Name + '</option>');
                });
            }
            else if (!response.Success) {
                //alert(response.Message);
            }
            else {
               // $("#job_container").html(response);
            }
        }
    });

}

var KTDropzoneDemo = function () {
    return {
        init: function () {
            CriteriaChanged();
        }
    };
}();
KTUtil.ready(function () {
    KTDropzoneDemo.init();
});
