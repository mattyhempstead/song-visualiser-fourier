
'''

	Performs fourier transform on a wave represented as an array of pos/neg values

'''



import sys, math, random, pygame
pygame.init()

print("Beginning Program")


clock = pygame.time.Clock()
screen = pygame.display.set_mode((1300, 700))


# Generate wave
sampleSeperation = 0.03
sampleCount = 3000
waveSamples = []
for i in range(sampleCount):
	x = i*sampleSeperation
	y = math.sin(x/3) + math.sin(x)/2 + math.sin(3*x)/3
	#y = math.sin(x)
	waveSamples.append(y)

maxSample = max(waveSamples)

#print(waveSamples)



'''
	Do the forisomething transform for the whole length of the wave
	1. Wrap the entire wave around a point
	2. Find average point...


'''
startingWrapRate = 0.1
wrapRate = startingWrapRate
wrapRateSeperation = 0.002
wrapRateCount = 2000
frequencyWave = []


for i in range(wrapRateCount):

	if i%round(wrapRateCount/10)==0:
		print(str(round(100*i/wrapRateCount,2)) + "%")


	pointSum = [0,0]
	for k,sample in enumerate(waveSamples):
		# The current angle for the point, this should change for testing different frequencies
		angle = k*sampleSeperation*wrapRate		# Wrap rate changes how many x values are needed for one full wrap
		#if (k==len(waveSamples)-1):
			#print("Largest angle: " + str(angle) + " = " + str(angle/(2*math.pi)) + " wraps")

		pointSum[0] += math.cos(angle) * sample
		pointSum[1] += math.sin(angle) * sample

	pointSize = math.hypot(pointSum[0], pointSum[1])
	#print("Point Size: " + str(pointSize))

	frequencyWave.append(pointSize)

	# Next calculation wraps a little bit faster
	wrapRate += wrapRateSeperation

leastWraps = (sampleCount-1) * sampleSeperation * startingWrapRate / (2*math.pi)
mostWraps = (sampleCount-1) * sampleSeperation * (startingWrapRate + wrapRateSeperation*(wrapRateCount-1)) / (2*math.pi)
print("Least Wraps: " + str(leastWraps))
print("Most Wraps: " + str(mostWraps))

maxFrequency = max(frequencyWave)

#print(frequencyWave)





def drawWave(points, rect, maxAmplitude):
	pygame.draw.rect(screen, (255,255,255), rect)
	pygame.draw.rect(screen, (0,0,0), rect, 2)

	pointSeperation = rect.w / (len(points)-1)

	for k,sample in enumerate(points):
		#print(sample,k)
		pointPos = [
			round(rect.x + k*pointSeperation),
			round(rect.centery - (sample/maxAmplitude)*(rect.h/2))
		]

		pygame.draw.circle(screen, (255,0,0), pointPos, 1)




screen.fill((230,230,230))


drawWave(waveSamples, pygame.Rect(50,50,1200,200), maxSample)

drawWave(frequencyWave, pygame.Rect(50,400,1200,200), maxFrequency)


pygame.display.flip()




while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()