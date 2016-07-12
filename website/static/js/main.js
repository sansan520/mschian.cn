function donghua(box, item, animateClass){
	var tMin,tMax;
	var t=getScrollTop();
	tMin=box.offset().top;
	tMax=$(window).height()+box.outerHeight(true)+tMin;
	if ( (tMin<=t+$(window).height() && t+$(window).height()<=tMax) || (tMin <= $(window).height()) ){
		item.addClass(animateClass);
	}
};
function getScrollTop() {
	var scrollTop = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;
	return scrollTop;
}

