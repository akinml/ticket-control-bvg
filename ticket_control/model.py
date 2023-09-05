from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import pickle

from model_preprocessing import get_data


# this will run if "model.py" is called in Terminal
if __name__ == "__main__":
    X_train, y_train, X_test, y_test = get_data()
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)

    parameters = {'max_depth':[10, 11, 12], 'min_samples_split':[4, 5, 6]}
    rflf = GridSearchCV(rf_model, parameters, scoring='recall', n_jobs=-1)
    rflf.fit(X_train, y_train)

    rflf.best_estimator_.score(X_test, y_test)
    best_model = rflf.best_estimator_
    pickle.dump(best_model, open('model.pkl', 'wb'))
