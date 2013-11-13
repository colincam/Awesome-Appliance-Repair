/*======================================
* copyright, Opscode Inc. 
* Apache License
* Version 2.0, January 2004
* http://www.apache.org/licenses/
*=======================================
*/
 
function formReset() {
    document.getElementById("update-form").reset();
    $("#update").hide();
}

function validateDate(input) {
    var sdate = input.split('-');
    if (!/^\d{4}$/.test(sdate[0]) || !/^\d{2}$/.test(sdate[1]) || !/^\d{2}$/.test(sdate[2])) {
        alert('not valid date pattern, please use yyyy-mm-dd');
        return false;
    } else {
        var yearfield = sdate[0];
        var monthfield = sdate[1];
        var dayfield = sdate[2];
        var dayobj = new Date(yearfield, monthfield - 1, dayfield);
        
        if ((dayobj.getMonth() + 1 != monthfield) || (dayobj.getDate() != dayfield) || (dayobj.getFullYear() != yearfield)) {
            alert("Invalid Day, Month, or Year range detected. Please correct and submit again.");
            return false;
        } else {
            return true;
        }
    }
}

function updateValidate() {
    var valid = true;
    var field = $("#update-form input[name='new_value']").val();
    if (field.toUpperCase() === 'NONE' || field.toUpperCase() === 'NULL' || validateDate(field)) {
        valid = true;
    } else {
        valid = false;
    }

    if (valid === false) {
        alert("please enter a date in the form yyyy-mm-dd \n or the string 'null' or 'none'");
        return false;
    }
}

function validateForm() {
    $(".request-dialog").remove();
    var valid = true;
    $("#request-form input[type='text'], textarea").each(function() {
        var $this = $(this);
        if ($this.val() === null || $this.val() === '') {
            valid = false;
        }
    });

    if (valid === false) {
        $("#request-form-div").append("<div class='request-dialog'><img class='request-closeme' src='static/images/close.png' /><p id='request-dialog-inner'>Please fill out all of the fields above before clicking the Submit button.</p></div>");
        $(".request-closeme").on('click', function(ev) {
            $(".request-dialog").remove();
        });
        return false;
    }
}

$(document).ready(function() {
// login.html
    $(".closeme").on('click', function(ev) {
        $(".error").remove();
    });

    $("#reset_data").on('click', function() {
        $.ajax({
            'url': $SCRIPT_ROOT + '/resetdb',
            'type': 'POST',
            'data': {'reset': true},
            'success': function(data) {
                if (data.no_action === true) {
                    $("#loginpage_content").append("<div class='error'><img class='closeme' src='static/images/close.png' /><p>The sample data has not yet been generated. Please log in first ...</p></div>");
                } else {
                    $("#loginpage_content").append("<div class='error'><img class='closeme' src='static/images/close.png' /><p>" + (data.rows_deleted - 28) + " new records, created from " + data.IP + ", were deleted, and the original sample data was restored.</p></div>");
                }

                $(".closeme").bind('click', function(ev) {
                    $(".error").remove();
                });
            }
        });
    });

// dispatcher.html    
    $(".dispatch-closeme").bind('click', function(ev) {
        $(".error, .flashes").hide();
    });

    $("#jobs-table").tablesorter({
        sortList: [[1, 0]]
    });

    $(".job_status, .job_date").on('click', function() {
        $(".flashes").empty();
        $("#update").empty();
        var $td = $(this);
        var field_value = $td.text();
        var field_name = $td.closest('table').find('th').eq($td.index()).attr("id");
        var job_id = $td.parent().children().eq(0).text();

        if (field_name === "job_status") {
            $("#update").html("<form id='update-form' method=post >\
            <fieldset>\
                <legend>Update</legend> Job " + job_id + ": Status\
                <input type=hidden name='job_id' value=" + job_id + " >\
                <input type=hidden name='field_value' value='" + field_name + "' >\
                <input type=hidden name='current_value' value=" + field_value + " >\
                <br><br><input type='radio' name='new_value' value='pending'>pending<br>\
                <input type='radio' name='new_value' value='completed'>completed<br><br>\
                <input type=submit value=Update>\
                <input type='button' onclick='formReset()' value='Cancel'>\
            </fieldset> </form>").show();
        } else {
            $("#update").html("<form id='update-form' onsubmit='return updateValidate();' method=post >\
            <fieldset>\
                 <legend>Update</legend> Job " + job_id + ": Appointment Date\
                 <input type=hidden name='job_id' value=" + job_id + " >\
                 <input type=hidden name='field_value' value='" + field_name + "' >\
                 <br><br> Enter Date <span style='font-size: 80%'>(yyyy-mm-dd)</span>:\
                 <input type='text' name='new_value' value='" + field_value + "'>\
                 <br><br> <input type=submit value=Update>\
                 <input type='button' onclick='formReset()' value='Cancel'>\
            </fieldset> </form>").show();

        }

        if (field_value === 'pending') {
            $("#update-form input[type='radio'][value='pending']").prop('checked', true);
        } else if (field_value === 'completed') {
            $("#update-form input[type='radio'][value='completed']").prop('checked', true);
        }
    });

// repairRequest.html
    $(".request-closeme").on('click', function(ev) {
        $(".request-dialog").remove();
    });

    $("#requested-jobs-table").tablesorter({
        sortList: [[0, 1]]
    });
});