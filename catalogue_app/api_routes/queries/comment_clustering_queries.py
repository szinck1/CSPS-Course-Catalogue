from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from catalogue_app.course_routes.queries.comment_queries import Comments

def get_clusters(course_code):
	"""Query a course's comments from DB and run LDA (unsupervised) algo to cluster
	comments by subject matter.
	"""
	# Query comments
	corpus = [comment[0] for comment in Comments('en', course_code).load().general]
	
	# Pre-processing
	# Lowercase
	corpus = [elem.lower() for elem in corpus]
	
	# Stopwords (only EN), lemmatize (only if sample has all ASCII chars)
		# Idea: a 'French' subject usually appears, is useful
			# Consequently, don't remove FR stopwords to encourage this formation
	
	# Vectorize
	vectorizer = CountVectorizer(stop_words='english')
	X = vectorizer.fit_transform(corpus)
	
	# Instantiate and train model
	TOPICS = 3
	WORDS_PER_TOPIC = 3
	lda = LatentDirichletAllocation(n_components=TOPICS,
									doc_topic_prior=1/TOPICS,
									topic_word_prior=1/TOPICS,
									learning_method='batch',
									max_iter=50,
									n_jobs=1,
									verbose=False)
	X_trans = lda.fit_transform(X)
	
	return _get_clusters(lda, vectorizer.get_feature_names(), WORDS_PER_TOPIC)


def _get_clusters(model, feature_names, n_top_words):
	""""""
	clusters = {}
	for ctr, topic in enumerate(model.components_):
		key = 'Cluster {0}'.format(ctr)
		val = ' '.join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
		clusters[key] = val
	return clusters



# X_trans.argmax(axis=1) to get best label for each sample

# TODO
# French??
# Validation / error if passed junk
# Try NMF
# Try only clustering with e.g. nouns, nouns and adjectives
# Wrap it all in Sklearn pipeline
# Automatically choose k
# Trying finding a single word to name clusters via wordnet





