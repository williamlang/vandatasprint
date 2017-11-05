import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.svm import SVC

data = pd.read_csv('final_data.csv', index_col=0)

for column in data:
	if len(data[column].unique()) == 1:
		data.drop(column, axis=1, inplace=True)
	print len(data[column].unique())

penalty_features = data[(data['type'] == 'penalty')][['period', 'sub_type', 'main_player_id', 'seconds', 'game_state']]

penalty_features['sub_type'] = penalty_features['sub_type'].astype('category')
penalty_features['game_state'] = penalty_features['game_state'].astype('category')

sub_type_dict = {penalty_type: i for i, penalty_type in enumerate(penalty_features['sub_type'].unique())}
game_state_dict = {game_state: i for i, game_state in enumerate(penalty_features['game_state'].unique())}

penalty_features['sub_type'] = penalty_features['sub_type'].map(sub_type_dict)
penalty_features['game_state'] = penalty_features['game_state'].map(game_state_dict)

y = penalty_features['sub_type']
X = penalty_features.drop(['sub_type'], axis=1)

avg_score = []
kf = KFold(n_splits=2, shuffle=True)
for train_index, test_index in kf.split(X):
	X_train, X_test = X.iloc[train_index], X.iloc[test_index]
	y_train, y_test = y.iloc[train_index], y.iloc[test_index]
	
	model = SVC(kernel='rbf', C=100).fit(X_train, y_train)
	avg_score.append(model.score(X_test, y_test))

print np.mean(avg_score)
