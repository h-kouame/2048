import random
import joblib
from util import load_games
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn import svm


def random_agent():
    actions = ['u', 'd', 'l', 'r']
    # get random number
    chosen = actions[random.randint(0, len(actions)-1)]
    return chosen


def random_agent_with_prior(action_dist = [0.00656045, 0.51452671, 0.28772259, 0.19212746]):
    ''''
    Prior data from expert game
    up: 0.656045%
    down: 51.452671% - favoured down over up to build at the bottom. they can be swapped
    left: 28.772259% - favoured left over right to build on the left corner. they can be swapped
    right: 19.212746%         
    '''
    actions = ['u', 'd', 'l', 'r']
    # get random number
    chosen = random.choices(actions, action_dist)[0]
    return chosen


class Model:
    def __init__(self, model=None):
        self.model = model

    def train(self, X, Y):
        self.model.fit(X, Y)

    def predict(self, x):
        return self.model.predict(x)

    def save(self, filename="models/svm.joblib"):
        joblib.dump(self.model, filename)

    def load_model(self, filename="models/svm.joblib"):
        self.model = joblib.load(filename)





if __name__=="__main__":
    svm_model = Model(svm.SVC(gamma='scale'))
    current_states, actions, rewards, cumulated_rewards, next_states = load_games(directory="games/human/")
    svm_model.train(current_states, actions)
    svm_model.save(filename="models/svm.joblib")

    nn_model = Model( MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(32, ), random_state=1))
    current_states, actions, rewards, cumulated_rewards, next_states = load_games(directory="games/human/")
    nn_model.train(current_states, actions)
    nn_model.save(filename="models/nn.joblib")
