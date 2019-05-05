/*時計*/
$(function(){
	setInterval(function(){
		var now = new Date();
		var y = now.getFullYear();
		var m = now.getMonth() + 1;
		var d = now.getDate();
		var w = now.getDay();
		var wd = ['日', '月', '火', '水', '木', '金', '土'];
		var h = now.getHours();
		var mi = now.getMinutes();
		var s = now.getSeconds();
		var mm = ('0' + m).slice(-2);
		var dd = ('0' + d).slice(-2);
		var hh = ('0' + h).slice(-2);
		var mmi = ('0' + mi).slice(-2);
		var ss = ('0' + s).slice(-2);
	$('#time').text(y + '年' + mm + '月' + dd + '日' + hh + '時' + mmi + '分' + ss + '秒' + '（' + wd[w] + '）');
	}, 1000);
	});


/*detail.htmlの表示・非表示*/
$("#morning_list ul li").each(function(){
	if($(".morning_hide").html().match(/None/g)){
		$(this).parent("ul").hide();
	}
});
$("#evening_list ul li").each(function(){
	if($(".evening_hide").html().match(/None/g)){
		$(this).parent("ul").hide();
	}
});


/*datatables*/
jQuery(function($){
		$.extend( $.fn.dataTable.defaults, { 
        language: {
            url: "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Japanese.json"
        } 
    }); 

        $("#data-table").DataTable({
        	"columnDefs": [{ className: "dt-nowrap", "targets": [ '_all' ]}],
        	"order": [[ 0, "desc" ]],
        });
    });

jQuery(function($){
		$.extend( $.fn.dataTable.defaults, { 
        language: {
            url: "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Japanese.json"
        } 
    }); 

        $("#data-table1").DataTable({
        	"columnDefs": [{ className: "dt-nowrap", "targets": [ '_all' ]}],
        	"order": [[ 0, "desc" ]],
        });
    });
jQuery(function($){
		$.extend( $.fn.dataTable.defaults, { 
        language: {
            url: "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Japanese.json"
        } 
    }); 

        $("#data-table2").DataTable({
        	"columnDefs": [{ className: "dt-nowrap", "targets": [ '_all' ]}],
        	"order": [[ 0, "desc" ]],
        });
    });
jQuery(function($){
		$.extend( $.fn.dataTable.defaults, { 
        language: {
            url: "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Japanese.json"
        } 
    }); 

        $("#data-table3").DataTable({
        	"columnDefs": [{ className: "dt-nowrap", "targets": [ '_all' ]}],
        	"order": [[ 0, "desc" ]],
        });
    });
jQuery(function($){
		$.extend( $.fn.dataTable.defaults, { 
        language: {
            url: "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Japanese.json"
        } 
    }); 

        $("#data-table4").DataTable({
        	"columnDefs": [{ className: "dt-nowrap", "targets": [ '_all' ]}],
        	"order": [[ 0, "desc" ]],
        });
    });


