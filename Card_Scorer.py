import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
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

def nn_model():
    #create model
    model = Sequential()
    model.add(Dense(output_dim=256, input_dim=160, kernel_initializer='normal'))
    model.add(Activation('relu'))
    model.add(Dense(output_dim=256, kernel_initializer='normal'))
    model.add(Activation('softmax'))
    model.add(Dense(500))
    model.add(Activation('softmax'))
    
    
    #compile model
    model.compile(loss='mean_squared_error', optimizer='adam')

    return model

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
        dataY.append(int(out))
    n_patterns = len(dataX)

	
	
    #X = numpy.reshape(dataX, (n_patterns, 160, 1))
    X = numpy.reshape(dataX, (n_patterns, 160))
    
    # normalize

    #X = X / float(n_vocab)

    # one hot encode the output variable

    #y = np_utils.to_categorical(dataY, num_classes=100)

    y = np_utils.to_categorical(dataY, num_classes=500)

	
    print('Total patterns: {}'.format(n_patterns))

    
    seed = 7
    numpy.random.seed(seed)

    #scale = StandardScaler()
    #dataX = scale.fit_transform(dataX)

    filepath = 'checkpoints/weights-improvement-Adam-{epoch:02d}-{loss:.4f}.hdf5'
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]


    estimator = KerasRegressor(build_fn=nn_model, nb_epoch=100, batch_size=128, verbose=0)

    estimator.fit(X, y, epochs=20, batch_size=128, callbacks=callbacks_list)

    res = estimator.predict(X)

    #kfold = KFold(n_splits=10, random_state=seed)

	
	# --The program breaks here--
    #results = cross_val_score(estimator, dataX, dataY, cv=kfold)
    #print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))




if __name__=='__main__':
    import sys
    # I had to do this because of windows
    sys.exit(main("data/cards.collectible.json_formatted.txt" , "data/scored-cards.json_formatted.txt", "test"))
    #sys.exit(main(sys.argv[1], sys.argv[2]))
