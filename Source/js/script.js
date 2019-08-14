$(document).ready(function() {

	//functional for navigation incon

	let nav_icon = $('.nav-icon'),
		account_bar = $('.account-bar'),
		general_form = $('.general_form');

		nav_icon.click(function(){
			account_bar.toggleClass('show'),
			general_form.toggleClass('show'),
			$(this).toggleClass('active');

			if($(this).hasClass('active')){
				$('body, html').css('overflow', 'hidden');
			}else(
				$('body, html').removeAttr('style')
			)
		})

	//dropdown list function

	$('.general_dropdown-list').each(function(){
		let that_list = $(this),
			that_span = that_list.find('span'),
			that_ul = that_list.find('ul');

			that_span.click(function(){
				that_ul.slideToggle();
				$(this).toggleClass('show')
			})
			that_ul.each(function(){
				let that_li = $(this).find('li');
				that_li.click(function(){
					let inner_content = $(this).text();
					that_ul.slideUp()
					that_span.text(inner_content).attr('data-name', inner_content).removeClass('show')
				})
			})

	})

	//input focus function
	$('.input_box input').focus(function(){
		$(this).parent().addClass('focus')
	}).blur(function(){
		if($(this).val() === ''){
			$(this).parent().removeClass('focus')
		}
	})
});