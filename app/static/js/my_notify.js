/** $(document).ready(function() { }); **/

function showSuccess(){
    $.notify.defaults({ className: "success" });
    
    $.notify("Done!", { position:"right middle"});
}