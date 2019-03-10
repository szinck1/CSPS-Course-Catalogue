from flask import jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from catalogue_app.course_routes.queries.comment_queries import Comments

def lda():
	
	# Query comments
	corpus = [comment[0] for comment in Comments('en', 'A313').load().general]
	
	corpus2 = ['mars loves food and cream',
			  'mars loves science and tech',
			  'cream is the food for mars',
			  'mars likes tech but also science']
	# Lowercase
	corpus = [elem.lower() for elem in corpus]
	# Stopwords, lemmatize, etc.
		# pass
	# Vectorize
	vectorizer = CountVectorizer(stop_words='english')
	X = vectorizer.fit_transform(corpus)
	
	
	#print(sorted([(val, key) for key, val in vectorizer.vocabulary_.items()]))
	
	# Instantiate model
	TOPICS = 3
	lda = LatentDirichletAllocation(n_components=TOPICS,
									doc_topic_prior=1/TOPICS,
									topic_word_prior=1/TOPICS,
									learning_method='batch', # 'online' for large
									max_iter=50,
									n_jobs=1,
									verbose=0,
									random_state=1) # Use constant random seed for dev
	X_trans = lda.fit_transform(X)
	
	
	
	
	def print_top_words(model, feature_names, n_top_words):
		my_list = []
		for topic_idx, topic in enumerate(model.components_):
			message = "Topic #%d: " % topic_idx
			message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
			my_list.append(message)
		return my_list
	
	
	
	return print_top_words(lda, vectorizer.get_feature_names(), 3)
	
	
	
	
	
	
	
	
	# Return highest prob for each sample
	#return X_trans.argmax(axis=1)
	
	# Same as built-in json.dumps but creates response, adds MIME type
	#return jsonify(response)
	
	
	# TODO
	# French??
	# Try NMF
	# Automatically choose k
	# Trying finding a single word to name clusters via wordnet
