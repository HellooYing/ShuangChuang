/* [ ---- Ebro Admin - dashboard 1 ---- ] */

	$(function() {
		//* small charts
		ebro_peity.init();
		//* easy pie charts
		ebro_easy_pie.init();
		//* vector map
		ebro_vector_map.init();
		//* charts
		ebro_charts.browsers();
		ebro_charts.social();
		ebro_charts.overview();
		//* video embed
		ebro_video.init();
		//* photo carousel
		ebro_carousel.init();
		//* calendar
		ebro_calendar.init();
	});
	
	//* small charts
	ebro_peity = {
		init: function() {
			if($.fn.peity) {
				if(jQuery.browser.msie) devicePixelRatio = 1;
				
				//* bars
				$.fn.peity.defaults.bar = {
					delimiter: ",",
					height: 24,
					max: null,
					min: 0,
					spacing: devicePixelRatio || 1,
					width: 32
				}

				if($('.peity_bar_up').length) {
					$(".peity_bar_up").peity("bar",{
						colours: ["#6cc334"]
					});
				}
				
				if($('.peity_bar_down').length) {
					$(".peity_bar_down").peity("bar",{
						colours: ['#e11b28']
					});
				}
			}
		}
	}
	
	//* easy pie charts
	ebro_easy_pie = {
		init: function() {
			if($('.easy_chart_a').length) {
				$('.easy_chart_a').easyPieChart({
					animate: 2000,
					size: 70,
					lineWidth: 5,
					scaleColor: false,
					barColor: '#CE4627'
				});
			}
			if($('.easy_chart_a').length) {
				$('.easy_chart_b').easyPieChart({
					animate: 2000,
					size: 70,
					lineWidth: 5,
					scaleColor: false,
					barColor: '#48AC2E'
				});
			}
		}
	}
	
	//* vector map
	ebro_vector_map = {
		init: function() {
			if($('#world_map_vector').length) {
				$('#world_map_vector').vectorMap({
					map: 'world_mill_en',
					backgroundColor: 'transparent',
					regionStyle: {
						initial: {
							fill: '#c4c4c4'
						},
						hover: {
							"fill-opacity": 1
						}
					},
					series: {
						regions: [{
							values: countries_data,
							scale: ['#ade59f', '#48ac2e'],
							normalizeFunction: 'polynomial'
						}]
					},
					onRegionLabelShow: function(e, el, code){
						if(typeof countries_data[code] == 'undefined') {
							e.preventDefault();
						} else {
							var countryLabel = countries_data[code];
							el.html(el.html()+': '+countryLabel+' visits');
						}
					}
				});
			}   
		}
	}
	
	//* charts
	ebro_charts = {
		browsers: function() {
			if($('#flot_social').length) {
				
				function labelFormatter(label, series) {
					return '<div class="flot_label">' + label +'</div>';
				}
				
				$.plot('#flot_browsers', data_browsers, {
					series: {
						pie: { 
							show: true,
							radius: 1,
							label: {
								show: true,
								radius: 3/4,
								formatter: labelFormatter,
								background: { 
									opacity: 0.5,
									color: '#000'
								}
							},
							innerRadius: 0.5
						}
					},
					legend: {
						show: false
					},
					colors: ["#7baf42","#efa91f","#f04b51","#0892cd","#b1b1b1"]
				});
				
			}
		},
		social : function() {
			if($('#flot_social').length) {
				var chart_placeholder = $('#flot_social');

				// add 2h to match utc+2
				for (var i = 0; i < data_twitter.length; ++i) {data_twitter[i][0] += 60 * 120 * 1000};
				for (var i = 0; i < data_google.length; ++i) {data_google[i][0] += 60 * 120 * 1000};
				for (var i = 0; i < data_linkedin.length; ++i) {data_linkedin[i][0] += 60 * 120 * 1000};
				for (var i = 0; i < data_facebook.length; ++i) {data_facebook[i][0] += 60 * 120 * 1000};

				var options = {
					grid: {
						clickable: true, 
						hoverable: true,
						autoHighlight: true,
						backgroundColor: null,
						borderWidth: 0,
						color: "#666",
						labelMargin: 10,
						axisMargin: 0,
						mouseActiveRadius: 10,
						minBorderMargin: 5
					},
					series: {
						lines: {
							show: true,
							lineWidth: 3,
							steps: false
						},
						points: {
							show:true,
							radius: 4,
							symbol: "circle",
							fill: true
						}
					},
					tooltip: true,
					tooltipOpts: {
						content: "%x - %y",
						shifts: {
							x: 20,
							y: 0
						},
						defaultTheme: false
					},
					xaxis: {
						mode: "time",
						minTickSize: [1, "day"],
						timeformat: "%d/%m",
						labelWidth: "40"
					},
					yaxis: { min: 0 },
					legend: {
						noColumns: 0,
						position: "ne"
					},
					colors: ["#7baf42","#0892cd","#efa91f","#f04b51"],
					shadowSize: 0
				};

				$.plot(chart_placeholder,[{
					label: "Twitter",
					data:data_twitter,
					points: {fillColor: '#fff'}
				}, {	
					label: "Google+",
					data:data_google,
					points: {fillColor: '#fff'}
				}, {	
					label: "LinkedIn",
					data:data_linkedin,
					points: {fillColor: '#fff'}
				}, {	
					label: "Facebook",
					data:data_facebook,
					points: {fillColor: '#fff'}
				}],options);
			}
		},
		overview : function() {
			if($('#flot_overview').length) {
				var chart_placeholder = $('#flot_overview');

				// add 2h to match utc+2
				for (var i = 0; i < data_new_visits.length; ++i) {data_new_visits[i][0] += 60 * 120 * 1000};
			   
				var options = {
					grid: {
						clickable: true, 
						hoverable: true,
						autoHighlight: true,
						backgroundColor: null,
						borderWidth: 0,
						color: "#666",
						labelMargin: 10,
						axisMargin: 0,
						mouseActiveRadius: 10,
						minBorderMargin: 5
					},
					series: {
						lines: {
							show: true,
							lineWidth: 3,
							steps: false,
							fill: true
						},
						points: {
							show:true,
							radius: 4,
							symbol: "circle",
							fill: true
						}
					},
					tooltip: true,
					tooltipOpts: {
						content: "%x - %y",
						shifts: {
							x: 20,
							y: 0
						},
						defaultTheme: false
					},
					xaxis: {
						mode: "time",
						minTickSize: [1, "day"],
						timeformat: "%d/%m",
						labelWidth: "40"
					},
					yaxis: { min: 0 },
					legend: {
						noColumns: 0,
						position: "ne"
					},
					colors: ["#0892cd"],
					shadowSize: 0
				};

				$.plot(chart_placeholder,[{
					label: "New Visits",
					data:data_new_visits,
					points: {fillColor: '#fff'},
					lines: {fillColor: 'rgba(8,146,205,.2)'}
				}],options);
			}
		}
	}
	
	//* video embed
	ebro_video = {
		init: function() {
			if ($('.fit_vid').length) {
				$(".fit_vid").fitVids();
			}
		}
	}
	
	//* photo carousel
	ebro_carousel = {
		init: function() {
			if ($('.photo-carousel').length) {
				
				$(".photo-carousel").owlCarousel({
					navigation : true,
					navigationText: ["<span class=\"glyphicon glyphicon-chevron-left\"></span>","<span class=\"glyphicon glyphicon-chevron-right\"></span>"],
					items : 4,
					itemsDesktop : [1199,3],
					itemsDesktopSmall : [979,3]
				});
				 
				$(".photo-carousel").find('.gal_lightbox').magnificPopup({ 
					type: 'image',
					gallery: {
						enabled: true,
						arrowMarkup: '<i title="%title%" class="icon-chevron-%dir% mfp-nav"></i>'
					},
					image: {
						cursor: null
					},
					callbacks: {
						beforeOpen: function() {
						},
						beforeClose: function() {
						}
					},
					retina: {
						ratio: 2
					}
					
				});
			}
		}
	}
	
	//*  calendar
	ebro_calendar = {
		init: function() {
			if($('#ebro_cal').length) {
				var date = new Date();
				var d = date.getDate();
				var m = date.getMonth();
				var y = date.getFullYear();
				
				$('#ebro_cal').fullCalendar({
					header: {
						center: 'prev title next',
						left: 'month agendaWeek agendaDay today',
						right: ''
					},
					buttonText: {
						prev: '<i class="icon-chevron-left" />',
						next: '<i class="icon-chevron-right" />'
					},
					editable: true,
					events: [
						{
							title: 'All Day Event',
							start: new Date(y, m, 1)
						},
						{
							title: 'Long Event',
							start: new Date(y, m, d-5),
							end: new Date(y, m, d-2)
						},
						{
							id: 999,
							title: 'Repeating Event',
							start: new Date(y, m, d-3, 16, 0),
							allDay: false
						},
						{
							id: 999,
							title: 'Repeating Event',
							start: new Date(y, m, d+4, 16, 0),
							allDay: false
						},
						{
							title: 'Meeting',
							start: new Date(y, m, d, 10, 30),
							allDay: false
						},
						{
							title: 'Lunch',
							start: new Date(y, m, d, 12, 0),
							end: new Date(y, m, d, 14, 0),
							allDay: false
						},
						{
							title: 'Birthday Party',
							start: new Date(y, m, d+1, 19, 0),
							end: new Date(y, m, d+1, 22, 30),
							allDay: false
						},
						{
							title: 'Click for Google',
							start: new Date(y, m, 28),
							end: new Date(y, m, 29),
							url: 'http://google.com/'
						}
					]
				});
			}
		}	
	}