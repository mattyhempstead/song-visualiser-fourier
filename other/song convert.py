'''
    Converts a .wav file into a list of individual sample values


'''



import sndhdr

songName = input("Song .wav file to convert: ")

songInfo = sndhdr.what(songName)
print(songInfo)

if (songInfo.framerate!=44100 or songInfo.nchannels!=2 or songInfo.sampwidth!=16):
    print("Song is NOT valid format")

else:
    print("Song is valid format")
    print("Beginning .wav conversion")

    file = open("song.txt", "a")

    sampleCount = 44100 * 60

    import wave
    a = wave.open(songName, "rb")
    #a.setpos(3750)
    p = list(a.readframes(sampleCount))
    a.close()

    for i in range(0,4*sampleCount,4):
        leftSample = p[i] + 256*p[i+1]
        rightSample = p[i+2] + 256*p[i+3]

        if leftSample>32768:
            leftSample = leftSample - 65536

        if rightSample>32768:
            rightSample = rightSample - 65536

        file.write(str(leftSample) + "," + str(rightSample) + "\n")

        if ((i/4)%round(sampleCount/10)==0):
            print(str(round(100*(i/4)/sampleCount,2)) + "%")


    file.close()

    print("Done")


input("Press to end")


