/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
class Status {
    constructor(step){
        this.step = step;

        this.source=null;
        this.resultCaptioning=[];
        this.ttsPath=null;
        this.voiceConversionPath=null;
    }

    changeStep(step){

        if(step == 1){
            $('.loading').show()
            uploadFile(processImageCaptioningResult)

        }
        if(step == 2){
            $('.loading').show()
            var params = {}
            params['sentence']=$('.active.list-group-item').html()
            requestPost(processTtsResult, apiUrls.STEP2, params)
        }
        if(step == 3){
            $('.loading').show();
            var params = {}
            params['type']=$('#voiceSelector').val()
            requestPost(processVoiceConversionResult, apiUrls.STEP3, params)
        }
    }
}

var apiUrls = {
    STEP1 : '/ic',
    STEP2 : '/tts',
    STEP3 : '/vc'
}

const status = new Status(0);

$(function () {
    $('#upload').on('change', function () {
        readURL(input);

    });

    $('#btnStep1Execution').click(function(){

        if($('#upload').val()) {
            status.changeStep(1);
        } else{
            alert("Choose image file(jpg/jpeg).")
        }
    });

    $('#btnStep2Execution').click(function(){
        if($('.list-group-item.active').text() !== ""){
            status.changeStep(2);
        } else {
            alert("Select a sentence.")
        }
    });

    $('#btnStep3Execution').click(function(){
        status.changeStep(3);
    });
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById( 'upload' );
var infoArea = document.getElementById( 'upload-label' );

input.addEventListener( 'change', showFileName );
function showFileName( event ) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}

/*  ==========================================
    Add Custom Logic
* ========================================== */
function requestPost(callback, url, params){

    $.ajax({
      type: "POST",
      url: url,
      data: params,
      success: function(result){
          console.log(result)
          callback(result);
      },
      error : function(err){
          console.log(err);
      }

    });
}
function requestGet(callback, url){

    $.ajax({
      type: "GET",
      url: url,
      success: function(data){
          alert(data);
      }
    });
}

function processImageCaptioningResult(result){
    $('.loading').hide()

    var addhtml=''
    for (let i=0; i<result.data.length; i++) {
        addhtml+='<button type="button" class="list-group-item list-group-item-action">' + result.data[i] + '</button>'
    }

    console.log(addhtml)
    $('.list-group').html(addhtml)

    $('.list-group-item').click(function(){
        $('.list-group-item').removeClass('active')
        $(this).addClass('active')
    });

    $('#btnStep2Execution').attr('disabled', false);
    $('#btnStep3Execution').attr('disabled', true);

}

function processTtsResult(result){
    $('.loading').hide()
    $('#btnStep3Execution').attr('disabled', false);
    $('#beforeAudioSource').attr("src",result.data)
    $('#beforeAudio')[0].load()
    $('#beforeAudio')[0].play()
}

function processVoiceConversionResult(result){
    $('.loading').hide()

    $('#afterAudioSource').attr("src",result.data)
    $('#afterAudio')[0].load()
    $('#afterAudio')[0].play()
}

function uploadFile(callback){;
    var formData = new FormData();
    formData.append("file", $("#upload")[0].files[0]);

    $.ajax({
        url: '/ic',
        processData: false,
        contentType: false,
        data: formData,
        type: 'POST',
        success: function(result){
            callback(result)
        },
        error: function(xhr, ajaxOptions, thrownError){
            alert(xhr.thrownError);
        }
    });
}
