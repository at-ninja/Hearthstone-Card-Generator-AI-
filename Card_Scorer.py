import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# Not sure if I need these yet
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


def main(input_filename, output_filename, mode):

    raw_text = ''
    with open(input_filename) as fp:
        raw_text = fp.read()
        
    output = []
    with open(output_filename) as fp:
        output = fp.read().splitlines()

    raw_text = raw_text.lower()
    input_data = raw_text.splitlines()

    # create mapping of unique chars to integers

    chars = sorted(list(set(raw_text)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))
    int_to_char = dict((i, c) for i, c in enumerate(chars))

    #n_chars = len(raw_text)
    n_cards = len(output)
    
    n_vocab = len(chars)
    print('Total cards: {}'.format(n_cards))
    print('Total vocab: {}'.format(n_vocab))

    # prepare the dataset of input to output pairs encoded as integers
    
    dataX = []
    dataY = []
    for i in range(0, len(input_data), 1):
        # output is formatted 'name\tnumber' and we just want the number
        out = output[i].split('\t')[1]
        dataX.append([char_to_int[char] for char in input_data[i]])
        dataY.append(out)
    n_patterns = len(dataX)
    
    print('Total patterns: {}'.format(n_patterns))
    print(len(dataX[0]))

    
    #create model
    model = Sequential()
    model.add(Dense(160, input_dim=160, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    
    
    #compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    seed = 7
    numpy.random.seed(seed)
    
    estimator = KerasRegressor(build_fn=model, nb_epoch=100, batch_size=128, verbose=0)

    kfold = KFold(n_splits=10, random_state=seed)
    
    
    # --The program breaks here--
    results = cross_val_score(estimator, dataX, dataY, cv=kfold)
    print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))
    


if __name__=='__main__':
    import sys
    # I had to do this because of windows
    sys.exit(main("data/cards.collectible.json_formatted.txt" , "data/scored-cards.json_formatted.txt", "test"))
    #sys.exit(main(sys.argv[1], sys.argv[2]))
