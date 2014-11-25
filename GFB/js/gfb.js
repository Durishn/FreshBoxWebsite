$(document).ready(function(){
    $(".ppform").submit(function(e){
        var count = 1;
        $(".inval").each(function(){
            if($(this).val() > 0){
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

