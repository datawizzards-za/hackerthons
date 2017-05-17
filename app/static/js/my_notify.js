
    /* table tag 1*/
$(document).ready(function() {
    $("#table_vivio").DataTable();
    $("#search_id").append($("#table_vivio_filter"));
    $("#search_id").attr('placeholder','Search Here');
    $("#table_vivio_length").remove();
    
    $("#table_vivioj").DataTable();
    $("#searchj_id").append($("#table_vivioj_filter"));
    $("input").attr('placeholder','Search Here');
    $("#table_vivioj_length").remove();
    
    $("#table_vivio3").DataTable();
    $("#search3_id").append($("#table_vivio3_filter"));
    $("input").attr('placeholder','Search Here');
    $("#table_vivio3_length").remove();
    
    $("#table_vivio4").DataTable();
    $("#search4_id").append($("#table_vivio4_filter"));
    $("input").attr('placeholder','Search Here');
    $("#table_vivio4_length").remove();
});