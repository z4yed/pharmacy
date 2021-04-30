
$(document).ready(function (){

    jQuery.validator.addMethod("letters_only", function(value, element) {
    return this.optional(element) || /^[A-Za-z\.\s]+$/i.test(value);
    }, "Only Space & Alphabetical characters Allowed. ");

     $.validator.addMethod("valueNotEquals", function(value, element, arg){
          return arg !== value;
     }, "Please Select an option");

    $('form').each(function (){
        console.log("Form Initialized. ")

        $(this).validate({
        errorClass: "error",  // error class is defined in css
        rules:{
            customer_name: {
                required: true,
                letters_only: true,
            },
            customer_mobile: {
                required: true,
                minlength: 11,
                maxlength: 11,
                number: true,
            },
            manufacturer_name:{
                letters_only: true,
                required: true,
            },
            manufacturer_mobile:{
                required: true,
                minlength: 11,
                maxlength: 11,
                number: true,
            },
            first_email:{
                email: true,
            },
            second_email:{
                email:true,
            },
            phone:{
                minlength: 11,
                maxlength: 11,
                required: false,
                number: true,
            },
            previous_balance:{
                number: true,
                required: true,
            },
            leaf_type:{
                required: true,
            },
            total_box:{
                maxlength: 3,
                required:true,
            },

            //  Medicine Form

            barcode_id:{
                required: true,
                minlength: 7,
            },

            medicine_name:{
                required: true,
            },

            box_size:{
                required: true,
                valueNotEquals: 'default',
            },
            unit:{
                required:true,
                valueNotEquals: 'default',
            },
            category_id:{
                required:true,
                valueNotEquals: 'default',
            },

            manufacturer_id:{
                required: true,
                valueNotEquals: 'default',
            },
            price:{
                required: true,
            },
            manufacturer_price:{
                required: true,
            },
            tax0:{
                number: true,
            },
            tax1:{
                number: true,
            },

            // Purchase

            manufacturer_id:{
              required: true,
              valueNotEquals: 'default',
            },

            // 'leaf_type[]':{
            //     required: true,
            //     valueNotEquals: 'default',
            // }
            invoice_no:{
                required:true,
            },
            date:{
                required:true,
            },

            /// Employee Module
            rate_type:{
                required: true,
                valueNotEquals: 'default',
            },
            designation_id:{
                required: true,
                valueNotEquals: 'default',
            },
            firstname:{
                required: true,
                letters_only: true,
            },
            lastname:{
                required: true,
                letters_only:true,
            },
            emp_phone:{
                required: true,
                minlength: 11,
                maxlength: 11,
            },
            hrate:{
              required: true,
              numbers: true,
            },


            //expense
            expense_type:{
                required: true,
                valueNotEquals: 'default',
            },

        }
    });

    })


})