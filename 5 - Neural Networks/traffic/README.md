# Documentation

My expirementation process was mostly tweaking numbers and functions from tensorflow like
pooling and convolutions.Later I added dropout as well which seemed to help in some cases.
It seemed like the poolsize and units in the convolution layer was the most crucial to get right.
For a while I got problems with the network starting in config 2 and these problems didn't seem
to solve even when i tried to go back to config 1. This I have to investigate further.

Because my computer doesn't have a lot of processing power it take up to 10 minutes to run 
a new configuration. If this wasn't the case I could probably run more and get a better result.
My best score on testing was 0.96 on configuration 20 which I am happy with.

youtube-link: https://youtu.be/znbV6ocEqRk

# Neural network configurations

## config 1
    Conv2D(20, (4, 4), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
    MaxPooling2D(pool_size=(2,2))
    Conv2D(20, (3, 3), activation="relu")
    MaxPooling2D(pool_size=(3,3))
    Flatten()
    Dense(10, activation = "relu")
    Dense(NUM_CATEGORIES, activation = "softmax")

    accuracy training: 0.8131
    accuracy testing: 0.8179

## config 2 - changing 2nd poolsize to (2,2)

    accuracy training: 0.0557 
    accuracy testing: 0.0498

## config 3 - back to config 1 and changing 1st conv to (3,3)

    accuracy traing: 0.0535
    accuracy testing: 0.0503

## config 4 - 1st pool to (3,3)

    accuracy traing: 0.7704
    accuracy testing: 0.7374

## config 5 - 1st conv testing size to 32

    accuracy training: 0.7973
    accuracy testing: 0.7792

## config 6 - 1st conv testing to 50 and 2nd conv testing size to 50

    accuracy training: 0.0567
    accuracy testing: 0.0556

## config 7 - set conv testing to 32 and 64

    accuracy training: 0.0571
    accuracy testing: 0.0551

## config 8 - set conv testing to 32 and 16

    accuracy training: 0.0566
    accuracy testing: 0.0559

## config 9 - set conv to 32 and 20 and and 1st dense to 20 units

    accuracy training: 0.4227
    accuracy testing: 0.5199

### config 10 - 1st dense to 5 units

    accuracy training: 0.0591
    accuracy testing: 0.0521

## config 11 - 1st dense to 10 (same as config 5)

    accuracy training: 0.0600
    accuracy testing: 0.0586

## config 12 - Adding dropout of 0.5 after 1st dense

    accuracy training: 0.1868
    accuracy testing: 0.2962

## config 13 - 1st dense to have Num-categories * 8 units

    accuracy training: 0.8105
    accuracy testing: 0.8331

## config 14 - Added another desne layer with num-categories * 4 units

    accuracy training: 0.8321
    accuracy testing: 0.8794

## config 15 - Added another dense layer with num-catoegories * 16 units with dropout

    accuracy training: 0.8611
    accuracy testing: 0.8640

## config 16 - Added forgotten dropout from former config

    accuracy training: 0.8244
    accuracy testing: 0.8600

## config 17 - Deleted 2nd conv and pool

    accuracy training: 0.8500
    accuracy testing: 0.9237

## config 18 - conv to size (4,4)

    accuracy training: 0.8314
    accuracy testing: 0.9103

## config 19 - antoher conv after pool and both conv sizes to (3, 3)

    accuracy training: 0.9173
    accuracy testing: 0.9572
    accuracy training2: 0.9322
    accuracy testing2: 0.9600