
'''

	Reads a text file containing sound file samples and writes the fourier transform for each section of the sound file


	Performs fourier transform on a wave represented as an array of pos/neg values

'''



import math, pygame
pygame.init()

print("Beginning Program")



transformList = []


transformFile = open("songFreq.txt", "r")
for k,s in enumerate(transformFile):
	transformSection = s[:-1].split(",")
	transformSection = [float(i) for i in transformSection]
	transformList.append(transformSection)

	#print(k,transformSection)

transformFile.close()

print("Loaded File")

transformSeperation = 44100/30

# Number of transforms to render per second
transformTime = int(44100 / transformSeperation)

# Counter for which transform section program is up to
transformNum = 0



clock = pygame.time.Clock()
screen = pygame.display.set_mode((1300, 700))



def drawWave(points, rect, maxAmplitude):
	pygame.draw.rect(screen, (255,255,255), rect)
	pygame.draw.rect(screen, (0,0,0), rect, 2)

	pointSeperation = rect.w / (len(points)-1)

	for k in range(len(points)):
		if k>0:
			pointPos0 = [
				round(rect.x + (k-1)*pointSeperation),
				round(rect.centery - (points[k-1]/maxAmplitude)*(rect.h/2))
			]
			pointPos1 = [
				round(rect.x + (k)*pointSeperation),
				round(rect.centery - (points[k]/maxAmplitude)*(rect.h/2))
			]

			pygame.draw.line(screen, (255,0,0), pointPos0, pointPos1, 1)
			#pygame.draw.circle(screen, (255,0,0), pointPos, 1)



pygame.mixer.music.load("song.wav")
pygame.mixer.music.play()



print("Starting REDNERING")

font = pygame.font.SysFont(None, 36)

while True:
	clock.tick(transformTime)

	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()

	screen.fill((230,230,230))
	
	#print(transformList[transformNum])
	print("Rendering transform " + str(transformNum))
	drawWave(transformList[transformNum], pygame.Rect(50,50,1200,300), 1)


	time = round(transformNum/transformTime, 2)
	text = "Time: " + str(time)
	text = font.render(str(text), True, (0,0,0))
	screen.blit(text, [100, 400])



	transformNum += 1

	pygame.display.flip()

	#input()


	if transformNum >= len(transformList):
		break


pygame.mixer.quit()




while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()