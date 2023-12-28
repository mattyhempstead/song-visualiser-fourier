
'''

	Reads a text file containing sound file samples and writes the fourier transform for each section of the sound file


	Performs fourier transform on a wave represented as an array of pos/neg values

'''



import math, pygame, time
pygame.init()

print("Beginning Program")

fileName = input("Enter file path (without file extension): ")
freqFileName = fileName + ".txt"
songFileName = fileName + ".wav"

transformList = []

transformFile = open(freqFileName, "r")
for k,s in enumerate(transformFile):
	transformSection = s[:-1].split(",")
	transformSection = [float(i) for i in transformSection]
	transformList.append(transformSection)
transformFile.close()

print("Loaded File")

# Time between each transform section
transformSeperation = 1/30

clock = pygame.time.Clock()
screen = pygame.display.set_mode((700, 700))

font = pygame.font.SysFont(None, 36)


def drawWaveCircle(points, circle, maxAmplitude):

	# Sum up amplitudes
	circleGrowth = sum(points) / len(points)
	circle["r"] = round(circle["r"] + 30*circleGrowth)

	pygame.draw.circle(screen, (0,0,0), [circle["x"], circle["y"]], circle["r"])

	pointSeperation = math.pi / (len(points)-1)

	for k in range(len(points)-1):
		pointAngle = k * pointSeperation - math.pi/2
		pointAngleVector = [math.cos(pointAngle), math.sin(pointAngle)]

		pointBase = [
			circle["x"] + pointAngleVector[0] * circle["r"],
			circle["y"] + pointAngleVector[1] * circle["r"]
		]

		pointEnd = [
			pointBase[0] + pointAngleVector[0] * maxAmplitude * (points[k])**2,
			pointBase[1] + pointAngleVector[1] * maxAmplitude * (points[k])**2
		]

		pygame.draw.line(screen, (255,0,0), pointBase, pointEnd, 4)


	# Draw left side - added in 2023 to make more presentable
	for k in range(len(points)-1):
		pointAngle = k * pointSeperation - math.pi/2
		pointAngleVector = [math.cos(pointAngle), math.sin(pointAngle)]

		pointBase = [
			circle["x"] - pointAngleVector[0] * circle["r"],
			circle["y"] + pointAngleVector[1] * circle["r"]
		]

		pointEnd = [
			pointBase[0] - pointAngleVector[0] * maxAmplitude * (points[k])**2,
			pointBase[1] + pointAngleVector[1] * maxAmplitude * (points[k])**2
		]

		pygame.draw.line(screen, (255,0,0), pointBase, pointEnd, 4)



print("Starting Song")
pygame.mixer.music.load(songFileName)
pygame.mixer.music.play()

startTime = time.time()

while True:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()

	screen.fill((230,230,230))
	

	
	# Time within song
	songTime = time.time() - startTime

 	# Which transform section program is up to
	transformNum = round(songTime / transformSeperation)
	if transformNum >= len(transformList):
		break

	#print(transformList[transformNum])
	print("Rendering transform " + str(transformNum))
	drawWaveCircle(transformList[transformNum], {"x":350,"y":350,"r":150}, 250)

	text = "Time: " + str(round(songTime, 2))
	text = font.render(str(text), True, (0,0,0))
	screen.blit(text, [20, 20])

	pygame.display.flip()


pygame.mixer.quit()
