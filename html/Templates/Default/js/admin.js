

var admin = {

    confirm: function(title, url){    
        
        //class="reveal-modal [expand, xlarge, large, medium, small]"
        
        var modal = $('<div class="reveal-modal small" ></div>');
        
        var row = $('<div class="row" ></div>');
        var columns = $('<div class="columns twelve" style="text-align: center;" ></div>');
        var title = $('<h6>'+title+'</h6>');
        var buttonNo = $('<a href="#" class="button alert small" >NO</a>');
        var buttonYes = $('<a href="#" class="button success small">YES</a>');
        
        row.append(columns)
        columns.append(title)
        columns.append(buttonYes)
        columns.append('&nbsp;&nbsp;')
        columns.append(buttonNo)
        modal.append(row)
        $('body').append(modal)
        
        $(buttonYes).click(function(){
            //modal.remove();
            document.location.href = url
            return false;
        });
        
        $(buttonNo).click(function(){
            modal.trigger('reveal:close');
            return false;
        });
        
        modal.reveal();
        
        return false;
    }

};

$(function(){
    $('.alert-box  a.close').click(function(){       
        $(this).parent().remove();
        return false;
    });
    
    $('input.auto-check').change(function(){
        var elem = $(this);
        var checkBoxName = elem.attr('data-name');
        if(elem.prop('checked')){
            $('input[name='+checkBoxName+']').prop('checked', this.checked)
        }else{
            $('input[name='+checkBoxName+']').removeAttr('checked')
        }
    });
    
});

