import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


def main(filename, mode):

    raw_text = ''
    with open(filename) as fp:
        raw_text = fp.read()

    raw_text = raw_text.lower()

    # create mapping of unique chars to integers

    chars = sorted(list(set(raw_text)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))
    int_to_char = dict((i, c) for i, c in enumerate(chars))

    n_chars = len(raw_text)
    n_vocab = len(chars)
    print('Total characters: {}'.format(n_chars))
    print('Total vocab: {}'.format(n_vocab))

    # prepare the dataset of input to output pairs encoded as integers

    seq_length = 100
    dataX = []
    dataY = []
    for i in range(0, n_chars - seq_length, 1):
        seq_in = raw_text[i:i+seq_length]
        seq_out = raw_text[i + seq_length]
        dataX.append([char_to_int[char] for char in seq_in])
        dataY.append(char_to_int[seq_out])
    n_patterns = len(dataX)

    print('Total patterns: {}'.format(n_patterns))

    # reshape X to be [samples, time steps, features]

    X = numpy.reshape(dataX, (n_patterns, seq_length, 1))

    # normalize

    X = X / float(n_vocab)

    # one hot encode the output variable

    y = np_utils.to_categorical(dataY)

    # define the LSTM model

    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.2))
    # model.add(LSTM(256))
    # model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    if mode == 'create':
        create_rnn(X, y)
    elif mode == 'predict':
        generate(dataX, int_to_char, n_vocab, model)


def create_rnn(X, y, model):

    # define the checkpoint

    filepath = 'checkpoints/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5'
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]

    model.fit(X, y, epochs=20, batch_size=128, callbacks=callbacks_list)


def generate(dataX, int_to_char, n_vocab, model):

    # load the network weights
    filename = "checkpoints/weights-improvement-19-0.7472.hdf5"
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    # pick a random seed
    start = numpy.random.randint(0, len(dataX)-1)
    pattern = dataX[start]
    print("Seed:")
    print("\"" + ''.join([int_to_char[value] for value in pattern]) + "\"")
    # generate characters
    for i in range(1000):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_char[index]
        seq_in = [int_to_char[value] for value in pattern]
        print(result, end='')
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
    print("\nDone.")


if __name__=='__main__':
    import sys
    sys.exit(main(sys.argv[1], sys.argv[2]))