let row_count = 1
let plus_clicked = 2

if (action == 'update'){
    row_count = parseInt(current_rows)
    plus_clicked = parseInt(current_rows) + 1
}

function increase_row(module){
    if (module == 'purchase'){

        let next_row = plus_clicked // ie. td id = row_2, row_3, row_4 etc..

        let html = `

            <tr id="row_${next_row}">

                <td class="span3 manufacturer">
                    <select name="medicine_name[]" class="form-control available_medicine"
                     id="medicine_id_${next_row}" data-row="${next_row}">
                        <option>Select Medicine</option>
                    </select>
                </td>

                <td>
                    <input type="text" name="batch_id[]" id="batch_id_${next_row}"
                           class="form-control text-right" tabindex="7"
                         placeholder="Batch Id">
                </td>

                <td>
                    <input type="text" name="expire_date[]" id="expire_date_${next_row}"
                           class="form-control datepicker"
                           tabindex="8" placeholder="Expiry Date"
                           onchange="validate_date()" required>
                </td>

                <td class="wt">
                    <input type="text" id="available_quantity_${next_row}"
                           class="form-control text-right "
                           placeholder="0.00" readonly="">
                </td>

                <td>
                    <select name="leaf_type[]"  class="form-control" id="leaf_type_${next_row}"
                        required="" onchange="calculate_line_total('select', this.id, this.value)"

                        <option value="default" selected="selected"
                                data-select2-id="select2-data-8-1uob">Select Leaf Type
                        </option>



                    </select>

                </td>

                <td class="text-right">
                    <input type="text" name="box_quantity[]" id="box_quantity_${next_row}"
                           class="form-control text-right valid_number" 
                           onkeyup="calculate_line_total('input', this.id, this.value)"
                           onchange=""
                           placeholder="0.00" value="" min="0" tabindex="10"
                           required="required">
                </td>

                <td class="text-right">
                    <input type="text" name="product_quantity[]" id="quantity_${next_row}"
                           class="form-control text-right store_cal_1"
                           onkeyup=""
                           onchange=""
                           placeholder="0.00" value="" min="0" required="required"
                           readonly="">
                    <input type="hidden" name="unit_qty[]" id="unit_qty_1">
                </td>

                <td class="test">
                    <input type="text" name="product_rate[]"
                           onkeyup=""
                           onchange=""
                           id="product_rate_${next_row}"
                           class="form-control product_rate text-right valid_number"
                           placeholder="0.00" value="" min="0" tabindex="11"
                           required="required">
                </td>

                <td>
                   <input type="text" class="form-control mrp"
                   name="mrp[]" id="mrp_${next_row}" required="" tabindex="12">
                </td>

                <td class="text-right">
                    <input class="form-control total_price text-right" type="text"
                           name="total_price[]" id="total_price_${next_row}" value="0.00"
                           readonly="readonly">
                </td>
                
                <td class="test">
                    <input type="text" name="line_vat"
                           id="line_vat_${next_row}"
                           class="form-control line_vat text-right valid_number"
                           placeholder="0" value="" min="0" tabindex="11" readonly>
                </td>

                <td>
                   <button onclick="remove_rows('purchase',  this.id)" type="button" class="btn btn-danger fa fa-trash-alt" tabindex="13" id="${next_row}">
                        </button>
                </td>

            </tr>

        `

        row_count += 1  // If the plus button is clicked, total rows count will be increased by one.

        $("#addPurchaseItem").append(html)
        $("#leaf_type_"+next_row).html(leaf_html)
        $("#medicine_id_"+next_row).html(medicine_list)

        plus_clicked += 1

    }

    // For Invoice Module.
    if(module == 'invoice'){

        let next_row = plus_clicked // ie. td id = row_2, row_3, row_4 etc..

        let html = `

                <tr id="row_${next_row}">

                    <td id="product_field_${next_row}">
                        <select name="medicine_id[]" id="selected_medicine_${next_row}" 
                        data-row="${next_row}" class="form-control all_medicines">
                            <option value="default" selected>Select Medicine</option>                      
                        </select>
                    </td>                            

                    <td>
                        <select class="form-control select2 batches" data-row="${next_row}"
                                id="batch_id_${next_row}" name="batch_id[]" 
                                onchange=""
                                tabindex="-1"
                                aria-hidden="true">
                            <option>Select Batch</option>
                        </select>
                    </td>

                    <td>
                        <input type="text" name="available_quantity[]"
                        class="form-control text-right available_quantity_1"
                        value="0" readonly="" id="available_quantity_${next_row}">
                    </td>

                    <td>
                          <p id="expire_date_${next_row}" style="color: red"></p>                                 
                    </td>

                    <td>
                        <input name="" id="unit_${next_row}"
                               class="form-control text-right unit_1 valid" value="None"
                               readonly="" aria-invalid="false" type="text">
                    </td>

                    <td>
                        <input type="text" name="product_quantity[]"                     
                               onkeyup="calculate_total(this.id)"
                               class="total_qntt_1 form-control text-right total_quantity valid_number"
                               id="total_qntt_${next_row}" placeholder="0.00" min="0" tabindex="7"
                               required="">
                    </td>

                    <td class="invoice_fields">
                        <input type="text" name="product_rate[]" id="price_item_${next_row}"
                               class="price_item1 price_item form-control text-right valid_number"
                               tabindex="8" required=""                           
                               onkeyup="calculate_total(this.id)"
                               placeholder="0.00" min="0">
                    </td>

                    <td>
                        <input type="text" name="discount[]"
                               onkeyup="calculate_total(this.id)"
                               id="discount_${next_row}"
                               class="form-control text-right line_discount valid_number" min="0"
                               tabindex="9" placeholder="0.00">

                    </td>

                    <td class="invoice_fields">
                        <input class="total_price form-control text-right" type="text"
                               name="total_price[]" id="total_price_${next_row}" value="0.00"
                               readonly="readonly">
                    </td>

                    <td>

                        <button type="button" class="btn btn-danger btn-sm" id="${next_row}"
                                tabindex="10"
                                onclick="remove_rows('invoice',  this.id)">
                            <i class="far fa-trash-alt"></i></button>
                    </td>
                </tr>

        `

        $("#addInvoiceItem").append(html);
        $("#selected_medicine_"+next_row).html(all_medicines)

        if (action == 'update'){
            $("#selected_medicine_"+next_row).html(all_medicines).val('default')
        }

        row_count += 1  // If the plus button is clicked, total rows count will be increased by one.

        plus_clicked += 1

    }


}



function remove_rows(module, row_id){
    if (module == 'purchase'){
        if (row_count == 1){
            alert("Last Row Can't be Removed. ")
        }
        else{
            // alert(event.srcElement.id) Another way of getting  id of clicked button.

            let item_id = $("#batch_"+row_id).val()

            if (item_id != undefined){
                let data = {
                    item_id: item_id,
                }
                if (confirm('Are you sure to remove the Item ? ')){

                    $.ajax({
                       url:  '/purchase/remove-purchase-item', //  Hardcoded url because of JS file.
                       data: data,
                       method: 'get',
                       success: function (data){
                           if(data['deleted'] == 'Successful'){
                               alert("Batch Removed Successfully. ")
                           }
                       },
                       error: function (error){
                           console.log("Error Occurred. ");
                           console.log(error);
                       }
                    });

                    $("#row_"+row_id).remove()
                    row_count -= 1
                    calculate_subtotal();
                }

            }
            else{

                $("#row_"+row_id).remove()
                row_count -= 1
                calculate_subtotal();

            }

        }



    }
    if(module == 'invoice'){
        if (row_count == 1){
            alert("Last Row Can't be Removed. ");
        }
        else{

            let item_id = $("#item_id_"+row_id).val()

            if (item_id != undefined){

                let data = {
                    item_id: item_id,
                }

                if(confirm('Are you sure to remove the Item ?')){
                    $.ajax({
                        url: '/invoice/remove-invoice-item',
                        data: data,
                        method: "get",
                        success: function(data){
                            if(data['deleted']=='Successful') {
                                alert("Item Removed Successfully. ")
                            }
                        },
                        error: function (error){
                            console.log("An Error Occurred. ")
                            console.log(error)
                        },
                    });

                    $("#row_"+row_id).remove();
                    row_count -= 1;
                    calculate_total_discount();

                }

            }
            else{
                $("#row_"+row_id).remove();
                row_count -= 1;
                calculate_total_discount();
            }

        }
    }
}

function full_pay(){
    let grand_total = $("#grandTotal").val() || 0
    $("#paid_amount").val(grand_total);
    $("#due_amount").val('0.00');
}


function calculate_total(row_id){
    row_id = parseInt(row_id.replace(/[^0-9.]/g, "")) // extracting number from string.
    let medicine  = $("#selected_medicine_"+row_id).val()
    if (medicine){
        let available_qntt = parseInt($("#available_quantity_"+row_id).val())
        let total_qntt = 0
        let batch_id = $("#batch_id_"+row_id).val()

        /// Counting total selected items of same batch.
        let loop_row_id = undefined
        $(".total_quantity").each(function (){
            loop_row_id = parseInt($(this).attr('id').replace(/[^0-9.]/g, ""))
            if($("#batch_id_"+loop_row_id).val()==batch_id){
                total_qntt += parseInt($(this).val())
            }
        })


        if(action == 'add'){
            if (total_qntt>available_qntt){
                alert("You can't sell more than "+available_qntt+ " of selected item.")
                $("#total_qntt_"+row_id).val('')
                $("#total_price_"+row_id).val('')

            }
            else{
                no_error(row_id);
            }
        }

        if (action == 'update' && row_id <= current_rows){

            let total_available_qntt = available_qntt + parseInt($("#sold_quantity_"+row_id).val())
            if (total_qntt>total_available_qntt){
                alert("You can't sell more than "+ total_available_qntt + " of selected item.")
                $("#total_qntt_"+row_id).val('')
                $("#total_price_"+row_id).val('')

            }
            else{
                 no_error(row_id)
            }

        }

        if (action == 'update' && row_id > current_rows){

           if (total_qntt>available_qntt){
                alert("You can't sell more than "+available_qntt+ " of selected item.")
                $("#total_qntt_"+row_id).val('')
                $("#total_price_"+row_id).val('')

            }
           else{
               no_error(row_id);
           }
        }

    }
    else{
        alert("Please Select Medicine First. ")
        $("#total_qntt_"+row_id).val('')
    }

}

function no_error(row_id){
    let discount = parseFloat($("#discount_"+row_id).val()) || 0

    if (discount > 100){
        alert("Discount can't be more than 100%. ")
        $("#discount_"+row_id).val('0.00')
        discount = 0
    }


    let line_qntt = parseInt($("#total_qntt_"+row_id).val()) || 0
    let price_of_one = $("#price_item_"+row_id).val() || 0
    let line_price = parseFloat(price_of_one) * parseFloat(line_qntt);
    line_price -= line_price* parseFloat(discount) / 100;
    $("#total_price_"+row_id).val(line_price.toFixed(2))

    calculate_total_discount();
}


function calculate_total_discount(){
    let discount = 0
    $('.line_discount').each(function (){

        let row_id = this.id
        row_id = parseInt(row_id.replace(/[^0-9.]/g, "")) // extracting number from string.

        let quantity = parseFloat($("#total_qntt_"+row_id).val()) || 0
        let price_one = parseFloat($("#price_item_"+row_id).val()) || 0

        let total_price = quantity * price_one
        let discounted_total = parseFloat($("#total_price_"+row_id).val()) ||0

        let l_discount = total_price - discounted_total  // Calculating Discount with percentage of each row
        discount += l_discount

    })

    discount += parseFloat($("#invdcount").val()) || 0


    $("#total_discount_amount").val(discount.toFixed(2));

    calculate_grand_total();

}


function calculate_grand_total(){
    let total = 0
    $(".total_price").each(function (){
        total += parseFloat($(this).val())
    });

    total -= parseFloat($("#invdcount").val()) || 0

    $("#grandTotal").val(total.toFixed(2));

    calculate_net_total();

}


function calculate_net_total(){
    let grandTotal = parseFloat(($("#grandTotal").val())) || 0
    let previous = parseFloat($("#previous").val()) || 0

    let net_total = grandTotal + previous

    $("#n_total").val(net_total.toFixed(2))

    calculate_due_total();
}

function calculate_due_total(){

    let netTotal = parseFloat($("#n_total").val()) || 0
    let paidAmount = parseFloat($("#paidAmount").val()) || 0

    let due = netTotal - paidAmount

    if (due  < 0){
        $("#dueAmount").val(0.00)
        let change = due * -1
        $("#change").val(change.toFixed(2))
    }
    else
    {
        $("#dueAmount").val(due.toFixed(2))
        $("#change").val('0.00')
    }
}

function full_paid_invoice(){
    let netTotal = parseFloat($("#n_total").val()) || 0
    $("#paidAmount").val(netTotal.toFixed(2));
    $("#dueAmount").val('0.00');
    $("#change").val('0.00');
}
