$(document).ready(function () {
    console.log("helo");
    $('.increment-btn').click(function (e) { 

        e.preventDefault();
        console.log("jithu")
        var inc_value=$(this).closest('.product_data').find('.quantity-imput').val();
        console.log(inc_value);
        var value = parseInt(inc_value, 10);
        value = isNaN(value)? 0: value;
        if (value<10)
        {
            value ++;
            $(this).closest('.product_data').find('.quantity-imput').val(value);
        }
    });
});