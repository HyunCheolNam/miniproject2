'use strict';

var mobileViewport = 992;
var isSafari = navigator.userAgent.indexOf("Safari") > -1;
var isChrome   = navigator.userAgent.indexOf('Chrome') > -1;
if((isSafari) && (isChrome)) {
    isSafari = false;
}

$(document).ready(function(){
    OwlCarousel();

    $('.blur-area').blurArea();
    $('.ws-action').windowScrollAction();
    checkboxes();
    afternavHeight();
    activeBookmark();
    magnificLightbox();
    priceSlider();
    BSTabsActions();
    datePickers();
    heroSearchSections();
    $('.quantity-selector').quantitySelector();
    autocomplete();
    searchResultsCollapse();
    comingSoonCountdown();
    smoothScroll();

    if($(window).width() > mobileViewport) {
       YouTubeVideo();
       stickySidebars();
    }

    if($(window).width() < mobileViewport) {
        mobileFilters();
    }
});

googleMaps();


function smoothScroll() {
    var scroll = new SmoothScroll('a[data-scroll]');
}


function YouTubeVideo() {
    var $video = $('#youtube-video');
    if($video.length) {

        $video.YTPlayer({
            fitToBackground: true,
            videoId: $video.data('video-id'),
            events: {
                onReady: function() {
                    $video.data('ytPlayer').player.mute();
                }
            }
        });

        $(document).on('scroll', function(){
            videoScroll();
        });

        function videoScroll() {
            var fraction = 0.75,
                player = $video.data('ytPlayer').player,
                videoHeight = $video.height(),
                videoOffsetTop = $video.offset().top,
                windowScrollY = window.scrollY;

            if(windowScrollY > (videoHeight + videoOffsetTop) *fraction) {
                player.pauseVideo();
            } else {
                player.playVideo();
            }
        }
    }
}

function OwlCarousel() {
    $('.owl-carousel').each( function() {
        var $carousel = $(this);
        $carousel.owlCarousel({
            // dots : false,
            // items : $carousel.data("items"),
            slideBy : $carousel.data("slideby"),
            center : $carousel.data("center"),
            loop : $carousel.data("loop"),
            margin : $carousel.data("margin"),

            autoplay : $carousel.data("autoplay"),
            autoplayTimeout : $carousel.data("autoplay-timeout"),
            navText : [ '<span class="fa fa-angle-left"><span>', '<span class="fa fa-angle-right"></span>' ],
            responsive: {
                0 : {
                    items: 1,
                    dots: true,
                    nav: false
                },
                992 : {
                    items: $carousel.data("items"),
                    dots: false,
                    nav : $carousel.data("nav")
                }
            }
        });
    });
}

function stickySidebars() {
    $('.sticky-col').stick_in_parent({
        parent: $('#sticky-parent')
    });

    $('.sticky-cols').stick_in_parent({
        parent: $('.sticky-parent')
    });
}


function mobileFilters() {
    if($('#mobileFilters').length) {
        $(document).on('scroll', function(){
            filtersScroll();
        });
    }

    function filtersScroll() {

        var filters = $('#mobileFilters');
        var footer =  $('#mainFooter');

        if(filters.offset().top + filters.height() > footer.offset().top - 10 || !$(document).scrollTop()) {
            filters.removeClass('active');
        } else {
            filters.addClass('active');
        }

        if($(document).scrollTop + window.innerHeight > footer.offset().top) {
            filters.addClass('active');
        }
    }
}

function checkboxes() {
    $('.icheck, .iradio').iCheck({
        checkboxClass: 'icheck',
        radioClass: 'iradio'
    });
}


function googleMaps() {
    if($('.google-map').length) {
        window.initMap = function() {
            $('.google-map').gmap();
        }
    } else {
        window.initMap = function() {
            return;
        }
    }
}



function afternavHeight() {
    $('.afternav-height').each(function(){
        var $mainNav = $('#main-nav'),
            mainNavHeight = $mainNav.height(),
            height = $(window).height() - mainNavHeight;

        $(this).css('height', height);
    });
}


function activeBookmark() {
    $('.theme-search-results-item-bookmark').each(function(index, el){
        $(el).on('click', function(e){
            e.preventDefault();
            $(this).toggleClass('active');
        });
    });
}



function magnificLightbox() {
    $('.magnific-gallery').each(function(index, el){
        $(el).magnificPopup({
            delegate: 'a',
            type: 'image',
            gallery: {
                enabled: true,
                navigateByImgClick: true,
                preload: [0,1]
            }
        })
    });

    $('.magnific-gallery-link').each(function(index , value){
      var gallery = $(this);
      var galleryImages = $(this).data('items').split(',');
        var items = [];
        for(var i=0;i<galleryImages.length; i++){
          items.push({
            src:galleryImages[i],
            title:''
          });
        }
        gallery.magnificPopup({
          mainClass: 'mfp-fade',
          items:items,
          gallery:{
            enabled:true,
            tPrev: $(this).data('prev-text'),
            tNext: $(this).data('next-text')
          },
          type: 'image'
        });
    });

    $('.magnific-inline').magnificPopup({
        type: 'inline',
        fixedContentPos: true
    });

    $('.magnific-iframe').magnificPopup({
        type: 'iframe'
    });
}


function priceSlider() {
    $("#price-slider").ionRangeSlider({
        type: "double",
        prefix: "$"
    });

    $("#price-slider-mob").ionRangeSlider({
        type: "double",
        prefix: "$"
    });
}



function BSTabsActions() {
    $('#sticky-tab').on('shown.bs.tab', function (e) {
      $('.sticky-tab-col').stick_in_parent({
            parent: $('#sticky-tab-parent')
        });
    });


    $('#slideTabs a').click(function (e) {
      e.preventDefault();
      $(this).tab('show');
      var control = $(this).attr('aria-controls')
      var active = $('#slideTabsSlides').find('.active')[0];
      var target = $('#slideTabsSlides').find("[data-tab='" + control + "']")[0];
      if(active !== target) {
        $(active).removeClass('active');
        $(target).addClass('active');
      }
    });
}


function datePickers() {

    $('.datePickerSingle').datetimepicker({
        format: 'ddd, MMM D'
    });


    $('.datePickerStart').datetimepicker({
        format: 'ddd M/D'
    }).on('dp.change', function(e){
        var parent = $($(this).parents('.row')[0]),
            endDate = parent.find('.datePickerEnd');
        endDate.data("DateTimePicker").minDate(e.date).show();
    });

    $('.datePickerEnd').datetimepicker({
        format: 'ddd M/D',
        useCurrent: false
    }).on('dp.change', function(e){
        var parent = $($(this).parents('.row')[0]),
            startDate = parent.find('.datePickerStart');
        startDate.data("DateTimePicker").maxDate(e.date);
    });

}


function heroSearchSections() {
    $('.theme-hero-search-section').each(function(){
        var label,
            input;

        label = $(this).find('.theme-hero-search-section-label');
        input = $(this).find('.theme-hero-search-section-input');

        if(input.val()) {
            label.addClass('active');
        }

        input.focus(function(){
            label.addClass('active');
        });

        input.blur(function(){
            if(!input.val()) {
                label.removeClass('active');
            }
        });
    });
}

function autocomplete() {
    $('.typeahead').typeahead({
        minLength: 3,
        showHintOnFocus: true,
        source: function(q, cb) {
            return $.ajax({
                dataType: 'jsonp',
                type: 'get',
                url: 'http://gd.geobytes.com/AutoCompleteCity?callback=?&q=' + q,
                chache: false,
                success: function(data) {
                    var res = [];
                    $.each(data, function(index, val){
                        if(val !== "%s") {
                            res.push({
                                id: index,
                                name: val
                            })
                        }
                    })
                    cb(res);
                }
            })
        }
    })
}


function searchResultsCollapse() {

    $('.theme-search-results-item-collapse').on('shown.bs.collapse', function(){
        $(this).parents('.theme-search-results-item').addClass('active');
    });

    $('.theme-search-results-item-collapse').on('hidden.bs.collapse', function(){
        $(this).parents('.theme-search-results-item').removeClass('active');
    });

}


function comingSoonCountdown() {

    $('#commingSoonCountdown').countdown('2018/10/10', function(e){
        $(this).html(e.strftime(''
            + '<div><p>%D</p><span>days</span></div>'
            + '<div><p>%H</p><span>hours</span></div>'
            + '<div><p>%M</p><span>minutes</span></div>'
            + '<div><p>%S</p><span>seconds</span></div>'
        ));
    });
}

$('.mobile-picker').each(function(i, item){
    if(!isSafari) {
        $(item).attr('type', 'text');
        $(item).val($(item).attr('value'));
        $(item).on('focus', function(){
            $(item).attr('type', 'date');
        });
        $(item).on('blur', function(){
            $(item).attr('type', 'text');
        });
    }
});
