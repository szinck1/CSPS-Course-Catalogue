from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_babel import gettext
from catalogue_app.config import Debug
from catalogue_app.course_routes.form import course_title_form, course_code_form
from catalogue_app.course_routes.queries import lsr_queries, product_info_queries, comments_queries, ratings_queries
course = Blueprint('course', __name__)

# Make LAST_YEAR and THIS_YEAR available to all templates
LAST_YEAR = Debug.LAST_YEAR
THIS_YEAR = Debug.THIS_YEAR
@course.context_processor
def context_processor():
	return {'LAST_YEAR': LAST_YEAR.replace('_', '-'), 'THIS_YEAR': THIS_YEAR.replace('_', '-')}


# Search by course code
@course.route('/course-code-selection', methods=['GET', 'POST'])
def course_code_selection():
	lang = session.get('lang', 'en')
	form_name = gettext('Course Code')
	form = course_code_form(lang, form_name)
	form = form(request.form)
	
	if request.method == 'POST' and form.validate():
		course_code = form.course_selection.data
		return redirect(url_for('course.course_result', course_code=course_code))
	return render_template('form.html', form=form, title=gettext("Selection"), button_val=gettext("Go"))


# Search by course title
@course.route('/course-title-selection', methods=['GET', 'POST'])
def course_title_selection():
	lang = session.get('lang', 'en')
	form_name = gettext('Course Title')
	form = course_title_form(lang, form_name)
	form = form(request.form)
	
	if request.method == 'POST' and form.validate():
		course_code = form.course_selection.data
		return redirect(url_for('course.course_result', course_code=course_code))
	return render_template('form.html', form=form, title=gettext("Selection"), button_val=gettext("Go"))


# Run queries and render template
@course.route('/course-result')
def course_result():
	# Get arguments from query string; if incomplete, return to selection page
	if 'course_code' not in request.args:
		return redirect(url_for('course.course_selection'))
	# Automatically escaped in Jinja2 (HTML templates) and MySQL queries
	course_code = request.args['course_code']
	lang = session.get('lang', 'en')
	
	# If course_code doesn't exist, render not_found.html
	course_title = lsr_queries.course_title(lang, THIS_YEAR, course_code)
	if not course_title:
		return render_template('not-found.html')
	
	# Check if course is online - needed for certain templates
	online_course = lsr_queries.online_course(THIS_YEAR, course_code)
	
	# Run queries and save in dict to be passed to templates
	pass_dict = {
		#Global
		'course_code': course_code,
        'course_title': course_title,
		'online_course': online_course,
		# General
		'course_description': product_info_queries.course_description(lang, course_code),
		'course_info': product_info_queries.course_info(lang, course_code),
		# Dashboard
		'overall_numbers_LY': lsr_queries.overall_numbers(LAST_YEAR, course_code),
		'overall_numbers_TY': lsr_queries.overall_numbers(THIS_YEAR, course_code),
		'offerings_per_region': lsr_queries.offerings_per_region(THIS_YEAR, course_code),
		'province_drilldown': lsr_queries.province_drilldown(THIS_YEAR, course_code),
		'offerings_per_lang_LY': lsr_queries.offerings_per_lang(LAST_YEAR, course_code),
		'offerings_per_lang_TY': lsr_queries.offerings_per_lang(THIS_YEAR, course_code),
		'offerings_cancelled_global_LY': lsr_queries.offerings_cancelled_global(LAST_YEAR),
		'offerings_cancelled_global_TY': lsr_queries.offerings_cancelled_global(THIS_YEAR),
		'offerings_cancelled_LY': lsr_queries.offerings_cancelled(LAST_YEAR, course_code),
		'offerings_cancelled_TY': lsr_queries.offerings_cancelled(THIS_YEAR, course_code),
		'top_5_depts': lsr_queries.top_5_depts(lang, THIS_YEAR, course_code),
		'top_5_classifs': lsr_queries.top_5_classifs(THIS_YEAR, course_code),
		'avg_class_size_global_LY': lsr_queries.avg_class_size_global(LAST_YEAR),
		'avg_class_size_global_TY': lsr_queries.avg_class_size_global(THIS_YEAR),
		'avg_class_size_LY': lsr_queries.avg_class_size(LAST_YEAR, course_code),
		'avg_class_size_TY': lsr_queries.avg_class_size(THIS_YEAR, course_code),
		'avg_no_shows_global_LY': round(lsr_queries.avg_no_shows_global(LAST_YEAR), 1),
		'avg_no_shows_global_TY': round(lsr_queries.avg_no_shows_global(THIS_YEAR), 1),
		'avg_no_shows_LY': round(lsr_queries.avg_no_shows(LAST_YEAR, course_code), 1),
		'avg_no_shows_TY': round(lsr_queries.avg_no_shows(THIS_YEAR, course_code), 1),
		# Geodata
		
		# Ratings
		'overall_satisfaction': ratings_queries.drf_average(THIS_YEAR, 'Overall Satisfaction', course_code),
		'knowledge_before': ratings_queries.drf_average(THIS_YEAR, 'Knowledge before', course_code),
		'knowledge_after': ratings_queries.drf_average(THIS_YEAR, 'Knowledge after', course_code),
		'learning_needs_met': ratings_queries.drf_average(THIS_YEAR, 'Learning Needs Met', course_code),
		# Comments
		'general_comments': comments_queries.general_comments(course_code),
		'instructor_comments': comments_queries.instructor_comments(course_code),
		'reason_to_participate': comments_queries.reason_to_participate(course_code),
		'technical_issues': comments_queries.technical_issues(course_code)
	}
	return render_template('/course-page/main.html', pass_dict=pass_dict)


# Not yet implemented
@course.route('/departmental')
def departmental():
	return render_template('departmental.html')
