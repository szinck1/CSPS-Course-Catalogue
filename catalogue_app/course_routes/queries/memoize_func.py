from catalogue_app.config import Config
from catalogue_app.course_routes.queries import comment_queries, general_queries, learner_queries, map_queries
from catalogue_app.course_routes.queries import offering_queries, rating_queries

LAST_YEAR = Config.LAST_YEAR
THIS_YEAR = Config.THIS_YEAR


def get_vals(lang, course_code):
	# Instantiate classes
	locations = offering_queries.OfferingLocations(lang, THIS_YEAR, course_code).load()
	ratings = rating_queries.Ratings(lang, course_code).load()
	comments = comment_queries.Comments(lang, course_code).load()
	
	pass_dict = {
		#Global
		'course_code': course_code,
		'course_title': general_queries.course_title(lang, THIS_YEAR, course_code),
		# General
		'course_info': general_queries.course_info(lang, course_code),
		# Dashboard - offerings
		'overall_numbers_LY': offering_queries.overall_numbers(LAST_YEAR, course_code),
		'overall_numbers_TY': offering_queries.overall_numbers(THIS_YEAR, course_code),
		'region_drilldown': locations.region_drilldown(),
		'province_drilldown': locations.province_drilldown(),
		'city_drilldown': locations.city_drilldown(),
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
		'regs_per_month': learner_queries.regs_per_month(lang, THIS_YEAR, course_code),
		'top_5_depts': learner_queries.top_5_depts(lang, THIS_YEAR, course_code),
		'top_5_classifs': learner_queries.top_5_classifs(THIS_YEAR, course_code),
		# Maps
		'offering_city_counts': map_queries.offering_city_counts(THIS_YEAR, course_code),
		'learner_city_counts': map_queries.learner_city_counts(THIS_YEAR, course_code),
		# Ratings
		'all_ratings': ratings.all_ratings(),
		# Comments
		'general_comments': comments.general,
		'technical_comments': comments.technical,
		'language_comments': comments.language,
		'performance_comments': comments.performance,
		# Categorical and yes/no questions
		'reason_to_participate': comments.reason,
		'technical_issues': comments.technical_bool,
		'languages_available': comments.language_bool,
		'tools_used': comments.gccampus_bool,
		'prepared_by': comments.preparation
	}
	return True
