# Neural network configurations


# config 1
    Conv2D(20, (4, 4), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
    MaxPooling2D(pool_size=(2,2))
    Conv2D(20, (3, 3), activation="relu")
    MaxPooling2D(pool_size=(3,3))
    Flatten()
    Dense(10, activation = "relu")
    Dense(NUM_CATEGORIES, activation = "softmax")

    accuracy training: 0.8131
    accuracy testing: 0.8179

# config 2 - changing 2nd poolsize to (2,2)

    accuracy training: 0.0557 
    accuracy testing: 0.0498

# config 3 - back to config 1 and changing 1st conv to (3,3)

    accuracy traing: 0.0535
    accuracy testing: 0.0503

# config 4 - 1st pool to (3,3)

    accuracy traing: 0.7704
    accuracy testing: 0.7374

# config 5 - 1st conv testing size to 32

    accuracy training: 0.7973
    accuracy testing: 0.7792

# config 6 - 1st conv testing to 50 and 2nd conv testing size to 50

    accuracy training: 0.0567
    accuracy testing: 0.0556

# config 7 - set conv testing to 32 and 64

    accuracy training: 0.0571
    accuracy testing: 0.0551

# config 8 - set conv testing to 32 and 16

    accuracy training: 0.0566
    accuracy testing: 0.0559

# config 9 - set conv to 32 and 20 and and 1st dense to 20 units

    accuracy training: 0.4227
    accuracy testing: 0.5199

# config 10 - 1st dense to 5 units

    accuracy training: 0.0591
    accuracy testing: 0.0521

# config 11 - 1st dense to 10 (same as config 5)

    accuracy training: 0.0600
    accuracy testing: 0.0586

# config 12 - Adding dropout of 0.5 after 1st dense

    accuracy training: 0.1868
    accuracy testing: 0.2962

# config 13 - 1st dense to havae Num-categories * 8 units

    accuracy training: 0.8105
    accuracy testing: 0.8331

# config 14 - Added another desne layer with num-categories * 4 units