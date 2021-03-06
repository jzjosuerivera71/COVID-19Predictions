import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

class LSTMModel():
    def split(self, cases):
        '''
        Formats the Data to Allow for LSTM Training

        Args: Array With the Number of Cases at Each Time Step
        Returns: Tuple of Arrays with LSTM Inputs of Sample Size sampleSize and Correct Outputs 
        '''
        dataX = []
        dataY = []
        for i in range(len(cases)-(self.__sampleSize+self.__daysIntoFuture)):
            dataX.append(cases[i:i+self.__sampleSize])
            dataY.append(cases[i+(self.__sampleSize+self.__daysIntoFuture)])
        return np.array(dataX), np.array(dataY)

    def __init__(self, cases, daysIntoFuture, sampleSize, lstmUnits, epochs):
        '''
        Constructor to Declare All Fields

        Args: cases: Array of Cases, daysIntoFuture, Number of Days Into the Future for Predictions,
            sampleSize: LSTM Sample Size, lstmUnits: Number of LSTM Units to be Used,
            epochs: Number of Epochs for Training
        Returns: None
        '''
        self.__daysIntoFuture = daysIntoFuture
        self.__sampleSize = sampleSize
        self.__lstmUnits = lstmUnits
        self.__epochs = epochs
        self.__dataX, self.__dataY = self.split(cases)
        self.__modelInput = cases[-sampleSize:]
    
    def model(self):
        '''
        Trains an LSTM Model and Predicts

        Args: None
        Returns: None
        Prints: The Prediction for the Model
        '''
        model = Sequential()
        model.add(LSTM(self.__lstmUnits, activation='relu', return_sequences=True, input_shape=(self.__sampleSize, 1)))
        model.add(LSTM(self.__lstmUnits, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        X = self.__dataX.reshape((len(self.__dataX), self.__sampleSize, 1))

        model.fit(X, self.__dataY, epochs=self.__epochs, verbose=1)

        modelInput = self.__modelInput.reshape(1, self.__sampleSize, 1)
        prediction = model.predict(modelInput, verbose=0)
        print(prediction[0][0], "Cases Expected in", self.__daysIntoFuture, "Days")