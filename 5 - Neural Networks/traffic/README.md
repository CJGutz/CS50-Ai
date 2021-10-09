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
