$(document).ready(function (){

    /*=== CONTACT US FORM ===*/
    $(document).on("submit", "#contact-form-ajax", function(e){
        e.preventDefault()
        console.log("Form Submitted......");


        let full_name = $("#firstname").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let subject = $("#sender-subject").val()
        let message = $("#sender-msg").val()

        console.log("Name :", full_name);
        console.log("Email :", email);
        console.log("Phone :", phone);
        console.log("Subject :", subject);
        console.log("Message :", message);

        $.ajax({
            url: "/ajax-contact-form",
            data: {
                "full_name": full_name,
                "email":email,
                "phone":phone,
                "subject": subject,
                "message":message,
            },
            dataType:"json",
            beforeSend: function(){
                console.log("Sending Data To Server...");    
            },
            success: function(res){
                console.log("Sent Data to Server!!!!");
            }
        })

    });


    
    /*---===== REVEAL TRANSFER POP UP  =====---*/
    document.getElementById("pin-confirmation-button").addEventListener("Click", function() {
        document.getElementById("pin-confirmation-modal").style.display = "block";
    });



})



/*---=====  JAVASCRIPT FOR POP UP  =====---*/












/*---===== CLOSE POP UP  =====---*/
document.querySelector(".popup .close-btn").addEventListener("click", function(){
    document.body.classList.remove("active-popup");
});



