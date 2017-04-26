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
    model.add(Dense(output_dim=128, input_dim=160, kernel_initializer='normal'))
    model.add(Activation('relu'))
    model.add(Dense(output_dim=128, kernel_initializer='normal'))
    model.add(Activation('relu'))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    
    
    #compile model
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model

def main(input_filename, chars_file):

    raw_text = ''
    with open(input_filename) as fp:
        raw_text = fp.read()
        
    chars = ''
    with open(chars_file) as fp:
        chars = fp.read()

    raw_text = raw_text.lower()
    input_data = raw_text.splitlines()
    input_data = [(x + (' ' * 160))[:160] for x in input_data]

    # create mapping of unique chars to integers

    chars = sorted(list(set(chars)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))
    int_to_char = dict((i, c) for i, c in enumerate(chars))

    # prepare the dataset of input to output pairs encoded as integers
    
    dataX = []
    for i in range(0, len(input_data), 1):
        # output is formatted 'name\tnumber' and we just want the number
        dataX.append([char_to_int[char] for char in input_data[i]])
    n_patterns = len(dataX)

	
	
    #X = numpy.reshape(dataX, (n_patterns, 160, 1))
    X = numpy.reshape(dataX, (n_patterns, 160))
    
    # normalize
    
    seed = 7
    numpy.random.seed(seed)

    #scale = StandardScaler()
    #dataX = scale.fit_transform(dataX)

    # filepath = 'checkpoints/weights-improvement-Adam-{epoch:02d}-{loss:.4f}.hdf5'
    # checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    # callbacks_list = [checkpoint]


    model = nn_model()

    model.load_weights("checkpoints/weights-improvement-Adam-49-0.6549.hdf5")

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    res = model.predict(X)

    for i in range(len(input_data)):
        print(input_data[i] + " -> {}".format(res[i][0] * 100))

    #kfold = KFold(n_splits=10, random_state=seed)

	
	# --The program breaks here--
    #results = cross_val_score(estimator, dataX, dataY, cv=kfold)
    #print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))




if __name__=='__main__':
    import sys
    # I had to do this because of windows
    sys.exit(main(sys.argv[1], "data/cards.collectible.json_formatted.txt"))
    #sys.exit(main(sys.argv[1], sys.argv[2]))
