from catalogue_app.config import Debug
from catalogue_app.course_routes.queries import comment_queries, general_queries, learner_queries, map_queries
from catalogue_app.course_routes.queries import offering_queries, rating_queries

LAST_YEAR = Debug.LAST_YEAR
THIS_YEAR = Debug.THIS_YEAR


def get_vals(course_code, lang='en'):
	pass_dict = {
		#Global
		'course_code': course_code,
		'course_title': general_queries.course_title(lang, THIS_YEAR, course_code),
		'online_course': general_queries.online_course(THIS_YEAR, course_code),
		# General
		'course_description': general_queries.course_description(lang, course_code),
		'course_info': general_queries.course_info(lang, course_code),
		# Dashboard - offerings
		'overall_numbers_LY': offering_queries.overall_numbers(LAST_YEAR, course_code),
		'overall_numbers_TY': offering_queries.overall_numbers(THIS_YEAR, course_code),
		'offerings_per_region': offering_queries.offerings_per_region(THIS_YEAR, course_code),
		'province_drilldown': offering_queries.province_drilldown(THIS_YEAR, course_code),
		'city_drilldown': offering_queries.city_drilldown(THIS_YEAR, course_code),
		'offerings_per_lang_LY': offering_queries.offerings_per_lang(LAST_YEAR, course_code),
		'offerings_per_lang_TY': offering_queries.offerings_per_lang(THIS_YEAR, course_code),
		'offerings_cancelled_global_LY': offering_queries.offerings_cancelled_global(LAST_YEAR),
		'offerings_cancelled_global_TY': offering_queries.offerings_cancelled_global(THIS_YEAR),
		'offerings_cancelled_LY': offering_queries.offerings_cancelled(LAST_YEAR, course_code),
		'offerings_cancelled_TY': offering_queries.offerings_cancelled(THIS_YEAR, course_code),
		'avg_class_size_global_LY': offering_queries.avg_class_size_global(LAST_YEAR),
		'avg_class_size_global_TY': offering_queries.avg_class_size_global(THIS_YEAR),
		'avg_class_size_LY': offering_queries.avg_class_size(LAST_YEAR, course_code),
		'avg_class_size_TY': offering_queries.avg_class_size(THIS_YEAR, course_code),
		'avg_no_shows_global_LY': round(offering_queries.avg_no_shows_global(LAST_YEAR), 1),
		'avg_no_shows_global_TY': round(offering_queries.avg_no_shows_global(THIS_YEAR), 1),
		'avg_no_shows_LY': round(offering_queries.avg_no_shows(LAST_YEAR, course_code), 1),
		'avg_no_shows_TY': round(offering_queries.avg_no_shows(THIS_YEAR, course_code), 1),
		# Dashboard - learners
		'regs_per_month': learner_queries.regs_per_month(THIS_YEAR, course_code),
		'top_5_depts': learner_queries.top_5_depts(lang, THIS_YEAR, course_code),
		'top_5_classifs': learner_queries.top_5_classifs(THIS_YEAR, course_code),
		# Maps
		'offering_city_counts': map_queries.offering_city_counts(THIS_YEAR, course_code),
		'learner_city_counts': map_queries.learner_city_counts(THIS_YEAR, course_code),
		# Ratings
		'all_ratings': rating_queries.all_ratings(THIS_YEAR, course_code),
		# Comments
		'general_comments': comment_queries.fetch_comments(course_code, 'Comment - General '),
		'technical_comments': comment_queries.fetch_comments(course_code, 'Issue Description'),
		'language_comments': comment_queries.fetch_comments(course_code, 'Comment - OL Not Available'),
		'performance_comments': comment_queries.fetch_comments(course_code, 'Comment - application for performance improvement'),
		# Categorical and yes/no questions
		'reason_to_participate': comment_queries.fetch_categorical(course_code, 'Reason to Participate'),
		'technical_issues': comment_queries.fetch_categorical(course_code, 'Technical Issues'),
		'languages_available': comment_queries.fetch_categorical(course_code, 'Official Language Available '),
		'tools_used': comment_queries.fetch_categorical(course_code, 'GCCampus Tools Used'),
		'prepared_by': comment_queries.fetch_categorical(course_code, 'Prep')
	}
	return pass_dict
