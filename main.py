import pygame
import random
from Classes.GameDefine import Constants
from Classes.GameDefine import Zombie
from Classes.SoundEffect import SoundEffect

class Game:
	def __init__(self):
		# Setup game window
		self.screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
		pygame.display.set_caption(Constants.GAME_TITLE)
		self.icon = pygame.image.load(Constants.ICON)
		pygame.display.set_icon(self.icon)

		# Load image sprites
		self.background = pygame.image.load(Constants.IMAGE_BG)
		self.gameover = pygame.image.load(Constants.IMAGE_GAMEOVER)
		self.button1 = pygame.image.load(Constants.IMAGE_BUTTON_1)
		self.button2 = pygame.image.load(Constants.IMAGE_BUTTON_2)

		# Font
		self.fontObj = pygame.font.Font(Constants.FONT_NAME, Constants.FONT_SIZE)
		self.fontBig = pygame.font.Font(Constants.FONT_NAME, Constants.FONT_SIZE_BIG)

		self.hits = 0	# Số lần đánh trúng
		self.misses = 0	# Số lần đánh trượt
		self.level = 1
		self.brains = 3	# Số não còn lại, não = 0 gameover
		self.zombieCount = 0	# Số lượng zombie đang xuất hiện

		self.zombie = []	# List zombie đang xuất hiện

		# List vị trí các nấm mộ
		self.gravePositions = []
		self.gravePositions.append(Constants.GRAVE_POS_1)
		self.gravePositions.append(Constants.GRAVE_POS_2)
		self.gravePositions.append(Constants.GRAVE_POS_3)
		self.gravePositions.append(Constants.GRAVE_POS_4)
		self.gravePositions.append(Constants.GRAVE_POS_5)
		self.gravePositions.append(Constants.GRAVE_POS_6)
		self.gravePositions.append(Constants.GRAVE_POS_7)
		self.gravePositions.append(Constants.GRAVE_POS_8)
		self.gravePositions.append(Constants.GRAVE_POS_9)
		self.gravePositions.append(Constants.GRAVE_POS_10)

		# List các frame animation của zombie
		zombieSpriteSheet = pygame.image.load(Constants.IMAGE_ZOMBIE)
		self.zombieImage = []
		self.zombieImage.append(zombieSpriteSheet.subsurface(Constants.ZOM_SPRITE_1))
		self.zombieImage.append(zombieSpriteSheet.subsurface(Constants.ZOM_SPRITE_2))
		self.zombieImage.append(zombieSpriteSheet.subsurface(Constants.ZOM_SPRITE_3))
		self.zombieImage.append(zombieSpriteSheet.subsurface(Constants.ZOM_SPRITE_4))
		self.zombieImage.append(zombieSpriteSheet.subsurface(Constants.ZOM_SPRITE_5))
		self.zombieImage.append(zombieSpriteSheet.subsurface(Constants.ZOM_SPRITE_6))

		# Hammer image
		self.hammerImage = pygame.image.load(Constants.IMAGE_HAMMER).convert_alpha()
		# Xoay ảnh búa khi đập
		self.hammerImageRotate = pygame.transform.rotate(self.hammerImage.copy(), Constants.HAMMER_ANGLE)

		self.soundEffect = SoundEffect()	# Sound effect

		# Brain image
		self.brainImage = pygame.transform.scale(pygame.image.load(Constants.IMAGE_BRAIN), (40, 35))

	# Handle level up
	def getPlayerLevel(self):
		nextLevel = int(self.hits / Constants.LEVEL_UP_GAP) + 1
		if nextLevel != self.level:
			self.soundEffect.playLevelUpSound()	# Play level up sound
			self.brains += 1	# Cộng thêm 1 não
		return nextLevel

	def getStayTime(self):
		# Zombie biến mất nhanh hơn
		maxStayTime = Constants.STAY_TIME - self.level * Constants.STAY_DELTA_TIME
		# Giới hạn giảm
		if maxStayTime <= Constants.RESPAWN_DELTA_TIME:
			maxStayTime = Constants.RESPAWN_DELTA_TIME
		return maxStayTime

	def getRespawnTime(self):
		# Zombie xuất hiện nhanh hơn
		maxRespawnTime = Constants.RESPAWN_TIME - self.level * Constants.RESPAWN_DELTA_TIME
		if maxRespawnTime <= Constants.RESPAWN_DELTA_TIME:
			maxRespwanTime = Constants.RESPAWN_DELTA_TIME
		return maxRespawnTime

	# Check if the mouse hits zombie or not
	def isZombieHit(self, mousePosition):
		mouseX = mousePosition[0]
		mouseY = mousePosition[1]
		for zombieIndex in range(self.zombieCount):
			thisZombie = self.zombie[zombieIndex]
			if thisZombie.zombieStatus == 2:
				continue
			distanceX = mouseX - self.gravePositions[thisZombie.index][0]
			distanceY = mouseY - self.gravePositions[thisZombie.index][1]
			if (0 < distanceX < Constants.ZOM_WIDTH) and (0 < distanceY < Constants.ZOM_HEIGHT):
				return zombieIndex
		return -1

	# Generate a new zombie
	def generateZombie(self):
		if self.zombieCount >= Constants.ZOM_NUM_MAX:
			return 0
		spawnIndex = random.randint(0, Constants.GRAVE_NUM_MAX - 1)
		# Check xem ô đó có bị trùng hay không
		for zombieIndex in range(self.zombieCount):
			if self.zombie[zombieIndex].index == spawnIndex:
				return 0
		newZombie = Zombie(spawnIndex, self.zombieImage[0])
		self.zombie.append(newZombie)
		self.zombieCount += 1
		return 1

	# Calculate player's brains
	def updateBrain(self, isEaten):
		if isEaten:
			self.brains -= 1
		self.screen.blit(self.brainImage, (650, 18))

	# Update, rotate the hammer
	def updateHammer(self, mousePosition, image, imageRotate, isClicked):
		mouseX = mousePosition[0] - Constants.HAMMER_DISTANCE_X
		mouseY = mousePosition[1] - Constants.HAMMER_DISTANCE_Y
		if isClicked:
			self.screen.blit(imageRotate, [mouseX, mouseY])
		else:
			self.screen.blit(image, [mouseX, mouseY])

	# Update zombie's animation
	def updateSprite(self):
		self.screen.blit(self.background, (0, 0))
		for zombieIndex in range(self.zombieCount):
			thisZombie = self.zombie[zombieIndex]
			self.screen.blit(thisZombie.pic, (self.gravePositions[thisZombie.index]))

	# Update player's hits, misses, level, brains
	def updateStatistics(self, isClicked, isEaten):
		self.updateHammer(pygame.mouse.get_pos(), self.hammerImage, self.hammerImageRotate, isClicked)
		self.updateBrain(isEaten)

		# Update the player's hits
		currentHitString = Constants.HIT_TEXT + str(self.hits)
		hitText = self.fontObj.render(currentHitString, True, Constants.TEXT_COLOR)
		hitTextPos = hitText.get_rect()
		hitTextPos.centerx = Constants.HIT_POS
		hitTextPos.centery = Constants.FONT_SIZE
		self.screen.blit(hitText, hitTextPos)

		# Update the player's misses
		currentMissesString = Constants.MISS_TEXT + str(self.misses)
		missesText = self.fontObj.render(currentMissesString, True, Constants.TEXT_COLOR)
		missesTextPos = missesText.get_rect()
		missesTextPos.centerx = Constants.MISS_POS
		missesTextPos.centery = Constants.FONT_SIZE
		self.screen.blit(missesText, missesTextPos)

        # Update the player's level
		currentLevelString = Constants.LEVEL_TEXT + str(self.level)
		levelText = self.fontObj.render(currentLevelString, True, Constants.TEXT_COLOR)
		levelTextPos = levelText.get_rect()
		levelTextPos.centerx = Constants.LEVEL_POS
		levelTextPos.centery = Constants.FONT_SIZE
		self.screen.blit(levelText, levelTextPos)

		# Update the player's brains
		currentBrainString = Constants.BRAIN_COUNT + str(self.brains)
		brainText = self.fontObj.render(currentBrainString, True, Constants.TEXT_COLOR)
		brainTextPos = brainText.get_rect()
		brainTextPos.centerx = Constants.BRAIN_POS
		brainTextPos.centery = Constants.FONT_SIZE
		self.screen.blit(brainText, brainTextPos)

		# Show game over screen
	def showEndScreen(self):
		fontEnd = pygame.font.Font(Constants.FONT_NAME, Constants.FONT_SIZE_BIG)
		missImage = fontEnd.render(str(self.misses), True, (255, 255, 255))
		hitImage = fontEnd.render(str(self.hits), True, (255,255, 255))
		score = self.hits - self.misses
		if score < 0:
			score = 0
		scoreImage = fontEnd.render(str(score), True, (255,255, 255))
		self.screen.blit(self.gameover, (0, 0))
		self.screen.blit(self.button1, (278, 509))
		self.screen.blit(missImage, (580, 364))
		self.screen.blit(hitImage, (311, 364))
		self.screen.blit(scoreImage, (507, 444))
		mouseX, mouseY = pygame.mouse.get_pos()
		if mouseX >= 278 and mouseX <= 557 and mouseY >= 509 and mouseY <= 559:
			self.screen.blit(self.button2, (278, 509))

	# Start the game's main loop
	def start(self):
		# Start screen
		startScreen = pygame.image.load(Constants.IMAGE_START)
		button0 = pygame.image.load(Constants.IMAGE_BUTTON_0)
		button0_hover = pygame.image.load(Constants.IMAGE_BUTTON_0_HOVER)
		gameStart = False
		while not gameStart:
			self.screen.blit(startScreen, (0, 0))
			self.screen.blit(button0, (527, 352))
			mouseX, mouseY = pygame.mouse.get_pos()
			if mouseX >= 527 and mouseX <= 794 and mouseY >= 352 and mouseY <= 406:
				self.screen.blit(button0_hover, (527, 352))
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if mouseX >= 527 and mouseX <= 794 and mouseY >= 352 and mouseY <= 406:
						gameStart = True
				if event.type == pygame.QUIT:
					pygame.quit()

		# Game initialization
		loop = True
		pygame.mouse.set_visible(False)

		# Flag variables
		isClicked = False
		isEaten = False

		# Time variables
		clock = pygame.time.Clock()
		cycleTime = 0                  # Count clock's time
		gameTime = 0
		lastSpawnTime = 0

		# Zombie-spawning variables
		maxStayTime = 5
		respawnTime = 1.5
		hitPos = -1

		for i in range(len(self.zombieImage)):
			self.zombieImage[i].set_colorkey((0, 0, 0))
			self.zombieImage[i] = self.zombieImage[i].convert_alpha()

		while loop:
			if self.brains > 0:
				# Calculate game input
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						loop = False
					if event.type == pygame.MOUSEBUTTONDOWN and event.button == Constants.LEFT_MOUSE_BUTTON:
						isClicked = True
						hitPos = self.isZombieHit(pygame.mouse.get_pos())
						if hitPos != -1:
							self.zombie[hitPos].zombieStatus = 2
							self.hits += 1
							self.level = self.getPlayerLevel()
							maxStayTime = self.getStayTime()
							respawnTime = self.getRespawnTime()
							self.soundEffect.playHitSound() # Play hit sound effect
						else:
							self.misses += 1
							self.soundEffect.playMissSound() # Play miss sound effect
					else:
						isClicked = False

				# Calculate game time
				mil = clock.tick(Constants.FPS)
				sec = mil / 1000.0
				cycleTime += sec
				gameTime += sec

				# Calculate zombies' variables
				zombieIndex = 0
				while zombieIndex < self.zombieCount:
					thisZombie = self.zombie[zombieIndex]
					thisZombie.stayTime += sec

					# Zombie status: rise
					if thisZombie.zombieStatus == 0:
						if thisZombie.stayTime > Constants.SPAWN_ANIMATION_TIME:
							if thisZombie.animationIndex > Constants.SPAWN_ANIMATION_INDEX_MAX:
								if thisZombie.stayTime > maxStayTime:
									thisZombie.animationIndex = Constants.SPAWN_ANIMATION_INDEX_MAX
									thisZombie.zombieStatus = 1
									thisZombie.stayTime = 0
									continue
							else:
								thisZombie.pic = self.zombieImage[thisZombie.animationIndex]
								thisZombie.animationIndex += 1
								thisZombie.stayTime = 0

					# Zombie status: fall
					if thisZombie.zombieStatus == 1:
						if thisZombie.stayTime > Constants.SPAWN_ANIMATION_TIME:
							if thisZombie.animationIndex >= 0:
								thisZombie.pic = self.zombieImage[thisZombie.animationIndex]
							thisZombie.animationIndex -= 1
							thisZombie.stayTime = 0
							# Make sure the last frame doesn't last one frame
							if thisZombie.animationIndex < -1:
								self.zombie.pop(zombieIndex)
								self.zombieCount -= 1
								isEaten = True
								continue

					# Zombie status: dead
					if thisZombie.zombieStatus == 2:
						if thisZombie.stayTime > Constants.DEAD_ANIMATION_TIME:
							if thisZombie.animationIndex < Constants.DEAD_ANIMATION_INDEX_MAX:
								thisZombie.pic = self.zombieImage[thisZombie.animationIndex]
							thisZombie.animationIndex += 1
							thisZombie.stayTime = 0
							if thisZombie.animationIndex > Constants.DEAD_ANIMATION_INDEX_MAX:
								self.zombie.pop(zombieIndex)
								self.zombieCount -= 1
								continue

					zombieIndex += 1

				self.updateSprite()
				self.updateStatistics(isClicked, isEaten)
				if gameTime - lastSpawnTime > respawnTime:
					if self.generateZombie():
						lastSpawnTime = gameTime

				isEaten = False

				# Update the display
				pygame.display.flip()

			else:
				pygame.mouse.set_visible(True)
				self.showEndScreen()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						loop = False
					if event.type == pygame.MOUSEBUTTONDOWN and event.button == Constants.LEFT_MOUSE_BUTTON:
						mouseX, mouseY = pygame.mouse.get_pos()
						if mouseX >= 278 and mouseX <= 557 and mouseY >= 509 and mouseY <= 559:
							self.brains = 3
							self.hits = 0
							self.misses = 0
							self.level = 1
							self.zombieCount = 0

							self.zombie = []
							clock = pygame.time.Clock()
							cycleTime = 0
							lastSpawnTime = 0
							maxStayTime = 5
							respawnTime = 1.5
							hitPos = -1

			pygame.display.update()

####################################################################
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# Start game - Run main loop
myGame = Game()
myGame.start()

# Exit game if the main loop ends
pygame.quit()


