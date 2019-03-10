from flask import jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from catalogue_app.db import query_mysql

def lda():
	corpus = ['mars loves food and cream',
			  'mars loves science and tech',
			  'cream is the food for mars',
			  'mars likes tech but also science']
	# Lowercase
	corpus = [elem.lower() for elem in corpus]
	# Stopwords, lemmatize, etc.
		# pass
	# Vectorize
	vectorizer = CountVectorizer()
	X = vectorizer.fit_transform(corpus)
	
	
	print(sorted([(val, key) for key, val in vectorizer.vocabulary_.items()]))
	
	# Instantiate model
	TOPICS = 2
	lda = LatentDirichletAllocation(n_components=TOPICS,
									doc_topic_prior=1/TOPICS,
									topic_word_prior=1/TOPICS,
									learning_method='batch', # 'online' for large
									max_iter=10,
									n_jobs=1,
									verbose=0,
									random_state=1) # Use constant random seed for dev
	X_trans = lda.fit_transform(X)
	
	# Return highest prob for each sample
	return X_trans.argmax(axis=1)
	
	# Same as built-in json.dumps but creates response, adds MIME type
	#return jsonify(response)
	
	
	# TODO
	# Try NMF
	# Automatically choose k
	# Trying finding a single word to name clusters via wordnet
