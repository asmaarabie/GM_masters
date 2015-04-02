Gesture Recording ,	8.4.14, Lorenz Gruber, Final Year Project

This dataset contains 2 gestures: 
	- Tick 
	- Z 

80 files for each each gesture, by 8 persons, each performed each movement 10 times

Start position of hand:
The hand should be in a calm position with right hand straight, as if one was cycling. 

Start and stop sound:
The phone makes a start and stop sound to indicate to the user when to start…

Recording details:
- Recording period: 2s
- Pause: 2s
- FSample: 20 Hz
- Repetitions per Gesture: 10

File name structure in csvData:
Each .csv file is named as g[XX]_[YY]_t[ZZ].mat:
[XX]: gesture index
[YY]: tester ID
[ZZ]: trial index

IMPORTANT!! the acceleration values are in g, not m/s2. 

Each .csv file has 8 columns (the gyro data was recorded as well. )
|t		|epoch time in ms|
|tRel		|relative time in s|
|x		|in g|
|y		|in g|
|z		|in g|
alpha
beta
gamma
