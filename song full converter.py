'''
    Converts a .wav file into a list of individual sample values


'''



def songFileConvert(songName):
    print("Beginning .wav sample extraction")

    sampleCount = 44100 * songLength

    a = wave.open(songName, "rb")
    p = list(a.readframes(sampleCount))
    a.close()

    for i in range(0,4*sampleCount,4):
        leftSample = p[i] + 256*p[i+1]
        if leftSample>32768:
            leftSample = leftSample - 65536

        #rightSample = p[i+2] + 256*p[i+3]
        #if rightSample>32768:
        #    rightSample = rightSample - 65536

        sampleList.append(leftSample)

        #file.write(str(leftSample) + "," + str(rightSample) + "\n")

        if ((i/4)%round(sampleCount/10)==0):
            print(str(round(100*(i/4)/sampleCount,2)) + "%")

    print("sampleList length: ", len(sampleList))



# Takes in a wave array of sample values and return the fourier transform
def getFourierTransform(wave, startingWrapRate, wrapRateSeperation, wrapRateCount, sampleSeperation):
    wrapRate = startingWrapRate
    transformWave = []

    for i in range(wrapRateCount):

        #if i%round(wrapRateCount/10)==0:
        #   print(str(round(100*i/wrapRateCount,2)) + "%")

        pointSumX = 0
        pointSumY = 0
        for k,sample in enumerate(wave):
            # The current angle for the point, this should change for testing different frequencies
            angle = k*sampleSeperation*wrapRate     # Wrap rate changes how many x values are needed for one full wrap
            #if (k==len(waveSamples)-1):
                #print("Largest angle: " + str(angle) + " = " + str(angle/(2*math.pi)) + " wraps")

            pointSumX += math.cos(angle) * sample
            pointSumY += math.sin(angle) * sample

        pointSize = math.hypot(pointSumX, pointSumY)
        #print("Point Size: " + str(pointSize))

        transformWave.append(pointSize)

        # Next loop wraps a little bit faster to test for higher frequencies
        wrapRate += wrapRateSeperation

    #leastWraps = (sampleCount-1) * sampleSeperation * startingWrapRate / (2*math.pi)
    #mostWraps = (sampleCount-1) * sampleSeperation * (startingWrapRate + wrapRateSeperation*(wrapRateCount-1)) / (2*math.pi)
    #print("Least Wraps: " + str(leastWraps))
    #print("Most Wraps: " + str(mostWraps))

    return transformWave



def songTransform(sampleList):
    print("Transforming song to calculate frequency values")

    # Generate wave
    # Music has 44100 samples per sec
    # Lowest frequency possible is 37Hz?
    # Assuming ~50Hz, 1 second would contain 50 periods
    # Try 1/10th second to extract frequencies
    sampleSeperation = 1/44100      # Samples are seperated by 1/44100 seconds
    sampleCount = 44100/30  # Number of samples used for a particular transform


    startingWrapRate = 5 * 2*math.pi    # Lowest wrap rate
    wrapRateSeperation = 5 * 2*math.pi  # Difference between each of the tested wrap rates
    wrapRateCount = 100     # Number of different frequencies to measure


    transformList = []  # A list of all transform for different sections of the sound
    transformCount = 30*songLength      # Number of individual transforms to add to the list
    transformSeperation = 44100/30      # Distance in samples between each transformed section

    # Largest value across all frequencies in any one of the transforms
    maxValue = 0.0001

    for i in range(transformCount):
        print("Transforming section " + str(i) + "/" + str(transformCount))

        minSample = i*transformSeperation
        maxSample = minSample + sampleCount

        waveSamples = sampleList[round(minSample):round(maxSample)]

        #print(waveSamples)

        frequencyWave = getFourierTransform(waveSamples, startingWrapRate, wrapRateSeperation, wrapRateCount, sampleSeperation)

        maxValue = max([maxValue] + frequencyWave)

        # Add this particular transform to the list
        transformList.append(frequencyWave)


    print("Scaling data between 0 and 1")
    for i in range(len(transformList)):
        for j in range(len(transformList[i])):
            transformList[i][j] /= maxValue     # Scale all frequency values across every transform between 0 and 1
            transformList[i][j] = round(transformList[i][j], 3)
            transformList[i][j] = str(transformList[i][j])


    input("Press to begin writing")

    # Freq file has same name as original .wav file but is .txt format
    songFreq = open(songName[:-4] + ".txt", "a")

    for transform in transformList:
        songFreq.write(",".join(transform) + "\n")

    songFreq.close()

    print("Completed sample transformation")






import sndhdr, wave, math

sampleList = []

songLength = 1  # Number of seconds to convert

songName = input("Song .wav file to convert: ")
songInfo = sndhdr.what(songName)
print(songInfo)


if (songInfo.framerate!=44100 or songInfo.nchannels!=2 or songInfo.sampwidth!=16):
    print("Song is NOT valid format")

else:
    print("Song is valid format")

    songLength = int(input("Song length to convert: "))
    
    # First read file an extract sample values
    songFileConvert(songName)

    # Then perform fourier transform on these sample values
    songTransform(sampleList)

    print("Done")

    input("Press to end program")
