$(document).ready(function(){


    function reply_click(element){
        document.getElementById('product_name').value = element.getAttribute('data-product-name');
    };   

    function HostSite(val,val2){
        document.getElementById("hs").value = val;
        document.getElementById("hsid".value = val2;
    };
            
    $(".clickableRow").click(function() {        
        window.document.location = $(this).attr("href");
    });

    $(".ppform").submit(function(e){
        var count = 1;
        $(".inval").each(function(){
            if($(this).val() > 0){
                $(".ppform").attr("target","_blank");
                $(".ppform").attr("action","https://www.paypal.com/cgi-bin/webscr");
                $(this).attr("name",$(this).attr("name") + "_" + count);
                $("."+$(this).attr("ref")).each(function(){
                    $(this).attr("name",$(this).attr("name") + "_" + count);
                });
                count++;
            }
        });
    });
});
