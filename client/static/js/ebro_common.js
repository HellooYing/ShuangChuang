/* [ ---- Ebro Admin - common js ---- ] */

    $(function() {
        //* fixed side navigation
        ebro_navigation.side_fixed();
		//* icon navigation
        ebro_navigation.icons();
        //* text navigation
        ebro_navigation.text();
        //* mobile navigation
        ebro_navigation.mobile();
        //* accordions
		ebro_accordions.init();
		//* tooltips_popovers
		ebro_tooltips_popovers.init();
		//* main search autocomplete
		ebro_autocomplete.init();
		
        //* ebro style switcher
        ebro_styleSwitcher.init();
        
        //* don't close dropdown on document click
        $('.notification_dropdown .dropdown-menu').click(function(e) {
            e.stopPropagation();
        });
		
    });

    //* get text without DOM element from node
    jQuery.fn.justtext=function(){return $.trim($(this).clone().children().remove().end().text())};

    //* avoid 'console' errors in browsers that lack a console
    if (!(window.console && console.log)) {
        (function() {
            var noop = function() {};
            var methods = ['assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error', 'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log', 'markTimeline', 'profile', 'profileEnd', 'markTimeline', 'table', 'time', 'timeEnd', 'timeStamp', 'trace', 'warn'];
            var length = methods.length;
            var console = window.console = {};
            while (length--) {
                console[methods[length]] = noop;
            }
        }());
    }

    //* detect touch devices 
    function is_touch_device() {
        return !!('ontouchstart' in window);
    };
	
	//* detect HiRes displays
    function isRetina(){
		var mediaQuery = "(-webkit-min-device-pixel-ratio: 1.5),\
				(min--moz-device-pixel-ratio: 1.5),\
				(-o-min-device-pixel-ratio: 3/2),\
				(min-resolution: 1.5dppx)";
		if (window.devicePixelRatio > 1)
			return true;
		if (window.matchMedia && window.matchMedia(mediaQuery).matches)
			return true;
		return false;
	};
    
    //* browser detect
    jQuery.browser = {};
    jQuery.browser.mozilla = /mozilla/.test(navigator.userAgent.toLowerCase()) && !/webkit/.test(navigator.userAgent.toLowerCase());
    jQuery.browser.webkit = /webkit/.test(navigator.userAgent.toLowerCase());
    jQuery.browser.opera = /opera/.test(navigator.userAgent.toLowerCase());
    jQuery.browser.msie = /msie/.test(navigator.userAgent.toLowerCase());
    
    
    //* navigation
    ebro_navigation = {
        //* icon navigation
        icons: function() {
            if($('#icon_nav_v').length && $('#icon_nav_v').is(':visible')) {
				//* sticky menu 
				$('#icon_nav_v').sticky('.main_section',{
					animate: false,
					useFixed: false,
					animTime: 300
				});
			}
        },
        //* text navigation
        text: function() {
            if($('#text_nav_v').length && $('#text_nav_v').is(':visible')) {
                
				//* vertical accorion menu
				$("#text_nav_v").navgoco({
					caret: '<i class="icon-angle-down"></i>',
					accordion: false,
					openClass: 'parent_active',
					save: true,
					cookie: {
						name: 'side_nav',
						expires: false,
						path: '/'
					},
					slide: {
						duration: 400,
						easing: 'swing'
					}
				});
				
				$("#text_nav_v_collapse").click(function(e) {
					e.preventDefault();
					$("#text_nav_v").navgoco('toggle', false);
				});
			
				$("#text_nav_v_expand").click(function(e) {
					e.preventDefault();
					$("#text_nav_v").navgoco('toggle', true);
				});
                
				//* sticky menu 
				$('#text_nav_v').sticky('.main_section',{
					animate: false,
					useFixed: false,
					animTime: 300
				});
				
            }
            if($('#text_nav_h').length && $('#text_nav_h').is(':visible')) {
				
				//* sub-level menu
                $("#text_nav_h").jMenu({
                    openClick : (is_touch_device()) ? true : false,
                    ulWidth : 200,
                    absoluteTop : 31,
                    absoluteLeft : 0,
                    effects : {
                        effectSpeedOpen : 100,
                        effectSpeedClose : 100,
                        effectTypeOpen : 'show',
                        effectTypeClose : 'hide',
                        effectOpen : 'linear',
                        effectClose : 'linear'
                    },
                    TimeBeforeOpening : 100,
                    TimeBeforeClosing : 100,
                    animatedText : false
				});
                //* add arrow to navigation parent
                $('#text_nav_h a.fNiv').each(function() {
                    if($(this).next('ul').length) {
						$(this).addClass('isTopParent').append('<i class="icon-angle-down"></i>')
					}
                });
                $('#text_nav_h ul a.isParent').each(function() {
                    $(this).append('<i class="icon-angle-right"></i>');
                });
                //* add "active" class on mouseenter
                $('#text_nav_h li').on('mouseenter',function() {
                    $(this).addClass('active');
                }).on('mouseleave',function() {
                    $(this).removeClass('active');
                });
            }
        },
        //* mobile navigation
        mobile: function() {
            if($('#text_nav_v').length) {
                $("#text_nav_v").tinyNav({
                    target: $('#mobile_navigation'),
                    active: 'link_active'
                });
				$('#mobile_navigation select').addClass('form-control').wrap('<div class="container" />');
            }
            if($('#text_nav_h').length) {
                $("#text_nav_h").tinyNav({
                    target: $('#mobile_navigation'),
					active: 'link_active'
                });
				$('#mobile_navigation select').addClass('form-control').wrap('<div class="container" />');
            }
			if($('#side_fixed_nav').length) {
				$("#text_nav_side_fixed").tinyNav({
                    target: $('#mobile_navigation'),
					active: 'link_active'
                });
				$('#mobile_navigation select').addClass('form-control').wrap('<div class="container" />');
			}
        },
		side_fixed: function() {
			if($('#side_fixed_nav').length) {
				
				//* vertical accorion menu
				$("#text_nav_side_fixed").navgoco({
					caret: '<i class="icon-angle-down"></i>',
					accordion: true,
					openClass: 'parent_active',
					save: true,
					cookie: {
						name: 'ebro_side_fixed_nav',
						expires: false,
						path: '/'
					},
					slide: {
						duration: 200,
						easing: 'linear'
					}
				});
				
				//* show scroll
				$('.slim_scroll').slimScroll({
					position: 'left',
					height: 'auto'
				});
				
				//* cookie for side fixed navigation
				var cookieFixedNav = 'ebro_side_fixed';
					
				//* toggle visibility
				$('#toogle_nav_visible').on('switch-change', function (e, data) {
					var value = data.value;
					if(value == true) {
						$.cookie(cookieFixedNav, 'nav_visible');
					} else if($.cookie(cookieFixedNav) != undefined) {
						$.cookie(cookieFixedNav, 'nav_hidden');
						$('body').removeClass('side_fixed_open')
					}
				});
				
				//* show/hide nav on click()
				$('#side_fixed_nav_toggle').click(function( e ) {
					e.stopImmediatePropagation();
					e.preventDefault();
					$('body').toggleClass('side_fixed_open');
					if( ($.cookie(cookieFixedNav) != undefined) && ($.cookie(cookieFixedNav) == 'nav_visible') ) {
						$('#toogle_nav_visible').bootstrapSwitch('setState', false);
						$.cookie(cookieFixedNav, 'nav_hidden');
					}
				});
				
				//* load default state from cookie
				if( ($.cookie(cookieFixedNav) != undefined) && ($.cookie(cookieFixedNav) == 'nav_visible' ) ) {
					$('body').addClass('side_fixed_open');
					$('#toogle_nav_visible').bootstrapSwitch('setState', true);
				}
				
				if(!is_touch_device()) {
					//* Lazy Bind or Delay Bind http://www.ideawu.com/blog/2011/05/jquery-delay-bind-event-handler-lazy-bind.html
					(function(a){a.fn.lazybind=function(d,e,f,b){var c=null;if(void 0!==b)a(this).on(b,function(){clearTimeout(c)});return a(this).on(d,function(a){var b=this;c=setTimeout(function(){e.call(b,a)},f)})}})(jQuery);
					
					$('#side_fixed_nav').lazybind('mouseenter', function(){
						if( ($.cookie(cookieFixedNav) == undefined) || ( ($.cookie(cookieFixedNav) != undefined) && ($.cookie(cookieFixedNav) == 'nav_hidden') ) ) {
							$('body').addClass('side_fixed_open');
						}
					}, 250, 'mouseleave');
					$('#side_fixed_nav').lazybind('mouseleave', function(){
						if( ($.cookie(cookieFixedNav) == undefined) || ( ($.cookie(cookieFixedNav) != undefined) && ($.cookie(cookieFixedNav) == 'nav_hidden') ) ) {
							$('body').removeClass('side_fixed_open');
						}
					}, 350, 'mouseenter');
				} else {
					$("#side_fixed_nav").swipe( {
						swipeRight:function(event, direction, distance, duration, fingerCount) {
							$('body').addClass('side_fixed_open');	
						},
						swipeLeft:function(event, direction, distance, duration, fingerCount) {
							$('body').removeClass('side_fixed_open');	
						},
						threshold:0
					});
				};
				
            }
		}
    }
    
	//* accordions
	ebro_accordions = {
		init: function() {
			$('.panel-group .panel-title a').each(function() {
				var $this = $(this);
				$this.append('<span class="icon-angle-left"></span>');
			})
			
			$('.panel-group .panel-collapse.in').each(function() {
				var $this = $(this);
				$this.closest('.panel').addClass('sect_active').find('.panel-title [class^="icon-"]').toggleClass('icon-angle-left icon-angle-up')
			})
			
			//* add active class (accorion show)
			$('.panel-group .panel-collapse').on('show.bs.collapse',function() {
				$(this).closest('.panel').addClass('sect_active').find('.panel-title [class^="icon-"]').toggleClass('icon-angle-left icon-angle-up');
			}).on('hide.bs.collapse',function() {
				$(this).closest('.panel').removeClass('sect_active').find('.panel-title [class^="icon-"]').toggleClass('icon-angle-left icon-angle-up');
			});
		}
	}
	
	//* tooltips, popovers
	ebro_tooltips_popovers = {
		init: function() {
			$('[data-toggle=tooltip]').tooltip();
			$('[data-toggle=popover]').popover();
		}
	}
	
	//* autocomplete
	ebro_autocomplete = {
		init: function() {
			$('.main_search .typeahead').typeahead({
				name: 'ebro-countries',
				valueKey: 'name',
				prefetch: 'js/lib/typeahead.js/example.json',
				template: [
					'<p class="sg_main"><b>{{name}}</b> <small class="text-muted">{{tld}}</small></p>',
					'<p class="sg_desc">{{subregion}}</p>'
				].join(''),
				engine: Hogan
			});
		}
	}
	
    //* style switcher
    ebro_styleSwitcher = {
        init: function() {
            
			//* layout
            $('#layout_style').on('change', function() {
                $this_val = $(this).val();
                
                $('body').removeClass('boxed full_width').removeClass('pattern_1 pattern_2 pattern_3 pattern_4 pattern_5 pattern_6 pattern_7 pattern_8  pattern_9  pattern_10');
                $('#style_pattern').hide();
                
                if($this_val == 'boxed') {
                    $('body').removeClass('full_width');
                    $('body').addClass($this_val+' pattern_1');
                    $('#style_pattern').show();
                }
                if($this_val == 'full_width') {
                    $('body').addClass('full_width');
                }
            })
            
			//* colors
            $('#theme_switch li').on('click',function() {
                var $color = $(this).attr('title');
                $('#theme_switch li').removeClass('style_active');
                $(this).addClass('style_active');
                $('#theme').attr('href','css/theme/'+$color+'.css');
            });
            
			//* patterns
            $('#style_pattern li').on('click',function() {
                var $pattern = $(this).attr('title');
                $('#style_pattern li').removeClass('pattern_active');
                $(this).addClass('pattern_active');
                $('body').removeClass('pattern_1 pattern_2 pattern_3 pattern_4 pattern_5 pattern_6 pattern_7 pattern_8  pattern_9  pattern_10').addClass($pattern);
            });
            
			//* show/hide style switcher
            $('.switcher_toggle').on('click', function(e) {
                if(!$('#style_switcher').hasClass('switcher_open')) {
                    $('#style_switcher').animate({ marginRight: 0 },200, function() {
                        $(this).addClass('switcher_open')  
                    })  
                } else {
                    $('#style_switcher').animate({ marginRight: '-191px'},200, function() {
                        $(this).removeClass('switcher_open')  
                    })  
                }
                e.preventDefault();
            })
            
			//* sidebar position
            $('#sidebar_switch input[name="sidebar_position"]').on('change', function() {
                $this_val = $(this).val();
                if($this_val == 'right') {
                    $('body').addClass('sidebar_right');
                } else {
                    $('body').removeClass('sidebar_right');
                }
            })
            
			//* reset styles
            $('#style_reset').click(function() {
                $('#style_pattern li').removeClass('pattern_active').eq(0).addClass('pattern_active');
                $('#style_pattern').hide();
                
                $('#layout_style>option:eq(0)').prop('selected', true);
                
                $('#theme_switch li').removeClass('style_active').eq(0).addClass('style_active');
                $('#theme').attr('href','css/theme/color_1.css');
                
                $('body').removeClass('pattern_1 pattern_2 pattern_3 pattern_4 pattern_5 pattern_6 pattern_7 pattern_8  pattern_9  pattern_10 sidebar_right boxed full_width');
				
				$("#sidebar_left").prop("checked", true);
            })

			$('#layout_style>option:eq(0)').prop('selected', true).change();
            $('#sidebar_left').prop('checked', true);
			
			setTimeout(function(){
				$('#style_switcher').animate({ marginRight: '-191px'},200, function() {
					$(this).removeClass('switcher_open')  
				})	
			},100);
			
			ebro_styleSwitcher.save_state();
			
        },
		save_state: function() {
			$('#layout_style').on('change', function() {
                $this_val = $(this).val();
				$.cookie('ebro_layout','fixed');
                if($this_val == 'boxed') {
					$.cookie('ebro_layout', 'boxed');
                }
                if($this_val == 'full_width') {
					$.cookie('ebro_layout', 'full_width');
                }
            });
			$('#theme_switch li').on('click',function() {
				$.cookie('ebro_color', $(this).attr('title'));
            });
			$('#style_pattern li').on('click',function() {
				$.cookie('ebro_pattern', $(this).attr('title'));
			});
			$('#sidebar_switch input[name="sidebar_position"]').on('change', function() {
                $this_val = $(this).val();
				if($this_val == 'right') {
					$.cookie('ebro_sidebar','right');
                } else {
					if($.cookie('ebro_sidebar') != undefined) {
						$.removeCookie('ebro_sidebar');
					}
                }
            });
			$('#style_reset').click(function() {
				if($.cookie('ebro_layout') != undefined) {
					$.removeCookie('ebro_layout');
				}
				if($.cookie('ebro_sidebar') != undefined) {
					$.removeCookie('ebro_sidebar');
				}
				if($.cookie('ebro_color') != undefined) {
					$.removeCookie('ebro_color');
				}
				if($.cookie('ebro_pattern') != undefined) {
					$.removeCookie('ebro_pattern');
				}
            });
			// check styles on page load
			if($.cookie('ebro_layout') != undefined) {
				$('body').removeClass('boxed full_width').removeClass('pattern_1 pattern_2 pattern_3 pattern_4 pattern_5 pattern_6 pattern_7 pattern_8  pattern_9  pattern_10');
				$('#layout_style').val($.cookie('ebro_layout')).change()
				if ( ($.cookie('ebro_layout') != 'boxed') && ($.cookie('ebro_pattern') != undefined) ) {
					$.removeCookie('ebro_pattern');
				}
			}
			if($.cookie('ebro_sidebar') != undefined) {
				if($.cookie('ebro_sidebar') == 'right') {
					$('#sidebar_switch input[name="sidebar_position"]').val('right').change()
					$("#sidebar_right").prop("checked", true)
				}
			}
			if($.cookie('ebro_color') != undefined) {
				$("#theme_switch li[title=\""+$.cookie('ebro_color')+"\"]").click();
			}
			if($.cookie('ebro_pattern') != undefined) {
				$("#style_pattern li[title=\""+$.cookie('ebro_pattern')+"\"]").click();
			}
		}
    }