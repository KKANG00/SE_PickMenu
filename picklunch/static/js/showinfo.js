function layer_open(el){
   var $el = $('#' + el);
   $el.fadeIn();      //레이어의 id를 temp변수에 저장
   var $elWidth = ~~($el.outerWidth()),
      $elHeight = ~~($el.outerHeight()),
        docWidth = $(document).width(),
        docHeight = $(document).height();
      //bg 클래스가 없으면 일반레이어로 실행한다.

      // 화면의 중앙에 레이어를 띄운다.
        if ($elHeight < docHeight || $elWidth < docWidth) {
            $el.css({
                marginTop: -$elHeight /4,
                marginLeft: -$elWidth/2
            })
        } else {
            $el.css({top: 0, left: 0});
        }
        $el.find('a.btn-layerClose').click(function(){
           $el.fadeOut();
                           // 닫기 버튼을 클릭하면 레이어가 닫힌다.
            return false;
        });
        $el.find('a.btn-layerEdit').click(function(){
           layer_open(el+'edit');

            return false;
        });//만약 edit버튼을 누르면 edit에 대한 layer가 새로 생기간다.
}
//즐겨찾기 추가버튼인 하트를 이모티콘으로 바꾸기 위한 함수
window.onload=function heart(){
  var obj=document.getElementsByName('favoriticon');
  for(var i=0;i<obj.length;i++){
    if(obj[i].title=="X"){
      obj[i].className="fa fa-heart-o";
    }
    else{
      obj[i].className="fa fa-heart";
    }
  }
}
