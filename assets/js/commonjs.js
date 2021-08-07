$(document).ready(function() {
    $('#num_page').on('change', function() {
        document.forms["myFormItemsPerPage"].submit();
    });


    $("#right-button").click(function() {
        event.preventDefault();
        $(".table-responsive").animate({
                scrollLeft: "+=300px"
            },
            "slow"
        );
    });

    $("#left-button").click(function() {
        event.preventDefault();
        $(".table-responsive").animate({
                scrollLeft: "-=300px"
            },
            "slow"
        );
    });

     $("#getcurrloc_btn").click(function() { //user clicks button
        if ("geolocation" in navigator) { //check geolocation available 
            //try to get user current location using getCurrentPosition() method
            navigator.geolocation.getCurrentPosition(function(position) {
                $('#id_ill_cust_address_lat').val(position.coords.latitude);
                $('#id_ill_cust_address_long').val(position.coords.longitude);

            });
        } else {
            console.log("Browser doesn't support geolocation!");
        }
    });

    $('#showlatlongmap').click(function() {
        var connlat = $('#id_ill_cust_address_lat').val();
        var connlong = $('#id_ill_cust_address_long').val();
        var newlatlong = connlat + "+" + connlong;
        newUrl = "https://www.google.com/maps/search/latlong".replace('latlong', newlatlong);
        $(this).attr("href", newUrl); // Set herf value
        //window.open(newUrl, "_blank", "width=0,height=0");
    });
});
