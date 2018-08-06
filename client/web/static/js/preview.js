function setImagePreviews(avalue) {
    var docObj = document.getElementById("doc");
    var dd = document.getElementById("dd");
    dd.innerHTML = "";
    var fileList = docObj.files;
    for (var i = 0; i < fileList.length; i++) {   
  
    dd.innerHTML += "<div class='preview_picture' id='preview_picture"+i+"' style='float:left' > <img style='width:800px;' id='img" + i + "' /> </div>";
    document.getElementById("preview_picture"+i).style.height=document.body.clientHeight-70+"px";
    var imgObjPreview = document.getElementById("img"+i); 
    if (docObj.files && docObj.files[i]) {

      //火狐下，直接设img属性
       //imgObjPreview.style.display = 'block';
        imgObjPreview.style.width = '600px';
       //imgObjPreview.src = docObj.files[0].getAsDataURL();
       //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式
      imgObjPreview.src = window.URL.createObjectURL(docObj.files[i]);
     }
     else {
      //IE下，使用滤镜
      docObj.select();
      var imgSrc = document.selection.createRange().text;
      alert(imgSrc)
      var localImagId = document.getElementById("img" + i);
      //必须设置初始大小
      localImagId.style.width = "150px";
      localImagId.style.height = "180px";
      //图片异常的捕捉，防止用户修改后缀来伪造图片
      try {
       localImagId.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale)";
       localImagId.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = imgSrc;
      }
      catch (e) {
       alert("您上传的图片格式不正确，请重新选择!");
       return false;
      }
      imgObjPreview.style.display = 'none';
      document.selection.empty();
     }
    } 
   
    return true;
   }