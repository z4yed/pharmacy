$(".numberField").keypress(function(e){
    if ((e.which < 48 || e.which > 57)) {
      return false;
    }
});

$('body').on('focus',".datepicker", function(){
    $(this).datepicker({
        dateFormat: "M d, yy",
        changeMonth: true,
        changeYear: true,
    }).keyup(function(e) {
        $.datepicker._clearDate(this);
    });

    // User Input will not be accepted.

});  // create datepicker to dynamically added textbox.


function validate_date(){
    console.log("This is coming from Custom.js File. ")
}



