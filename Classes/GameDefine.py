# Kích thước window, FPS của game
class GameConstants:
	SCREEN_WIDTH = 800
	SCREEN_HEIGHT = 600
	FPS = 60

class LevelConstants:
	LEVEL_UP_GAP = 5	# 5 điểm lên level
	LEVEL_DELAY_TIME = 5

# Kích thước sprite zombie, số zombie tối đa cùng lúc
class ZombieConstants:
	ZOM_WIDTH = 98
	ZOM_HEIGHT = 81
	ZOM_NUM_MAX = 3

	# Tọa độ từng frame trên sprite map zombie
	ZOM_SPRITE_1 = [19, 16, 80, 90]
	ZOM_SPRITE_2 = [190, 25, 100, 100]
	ZOM_SPRITE_3 = [367, 25, 95, 100]
	ZOM_SPRITE_4 = [558, 25, 96, 100]
	ZOM_SPRITE_5 = [741, 25, 90, 100]
	ZOM_SPRITE_6 = [901, 23, 88, 102]

class GraveConstants:
	GRAVE_NUM_MAX = 10		# Số lượng mộ tối đa
	# Tọa độ các mộ trên background image
	GRAVE_POS_1 = [101, 205 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_2 = [350, 204 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_3 = [580, 214 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_4 = [182, 297 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_5 = [422, 295 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_6 = [254, 404 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_7 = [505, 414 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_8 = [98, 514 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_9 = [348, 510 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_10 = [589, 510 - ZombieConstants.ZOM_HEIGHT]

class HammerConstants:
	HAMMER_ANGLE = 45	# Khi đập búa, sprite nghiêng 1 góc 45 độ như hiệu ứng đập
	# Khoảng cách của sprite khi đập với lúc bình thường
	HAMMER_DISTANCE_X = 16
	HAMMER_DISTANCE_Y = 25

class TimeConstants:
	# Thời gian của hoạt ảnh xuất hiện và bị đập của zombie
	SPAWN_ANIMATION_TIME = 0.1
	DEAD_ANIMATION_TIME = 0.1

	# Thời gian cho tới khi 1 con zom khác xuất hiện
	RESPAWN_TIME = 1.5
	RESPAWN_DELTA_TIME = 0.2	# Mức giảm mỗi lần level up để tăng độ khó

	# Thời gian zombie ngoi lên và đứng đợi
	STAY_TIME = 5
	STAY_DELTA_TIME = 0.3	# Mức giảm mỗi lần level up để tăng độ khó

	# Thời gian hoạt ảnh đập búa
	HAMMER_ANIMATION_TIME = 0.1

class AnimationConstants:
	# Index của các frame animation trong sprite lớn
	SPAWN_ANIMATION_INDEX_MAX = 2
	DEAD_ANIMATION_INDEX_MAX = 6

class FontConstants:
	FONT_NAME = "./Resources/fonts/ZOMBIE.ttf"
	FONT_SIZE = 36
	FONT_SIZE_BIG = 64

# Các text hiển trị trên màn hình
class TextConstants:
	GAME_TITLE = "Whack A Zombie"
	HIT_TEXT = "HITS - "
	MISS_TEXT = "MISSES - "
	LEVEL_TEXT = "LEVEL - "
	BRAIN_COUNT = " x "

	# Tọa độ các text trên màn hình
	HIT_POS = GameConstants.SCREEN_WIDTH / 2.7
	MISS_POS = GameConstants.SCREEN_WIDTH / 1.58
	LEVEL_POS = GameConstants.SCREEN_WIDTH / 7.75
	BRAIN_POS = 720

	TEXT_COLOR = [255, 255, 255]	# White

class ImageConstants:
	IMAGE = "./Resources/images/"	# Folder chứa ảnh
	ICON = IMAGE + "thor.png"
	IMAGE_START = IMAGE + "start.png"
	IMAGE_BUTTON_0 = IMAGE + "button0.png"
	IMAGE_BUTTON_0_HOVER = IMAGE + "button0_hover.png"
	IMAGE_BG = IMAGE + "background.png"
	IMAGE_GAMEOVER = IMAGE + "gameover.png"
	IMAGE_BUTTON_1 = IMAGE + "button1.png"
	IMAGE_BUTTON_2 = IMAGE + "button2.png"
	IMAGE_HAMMER = IMAGE + "hammer.png"
	IMAGE_ZOMBIE = IMAGE + "zombie.png"
	IMAGE_BRAIN	= IMAGE + "brain.png"

class SoundConstants:
	SOUND = "./Resources/sounds/"	# Folder chứa file audio
	SOUND_BG = SOUND + "music_bg.mp3"
	SOUND_HIT = SOUND + "hit.wav"
	SOUND_MISS = SOUND + "miss.wav"
	SOUND_LEVEL_UP = SOUND + "level_up.wav"

class Constants(GameConstants, LevelConstants, ZombieConstants, GraveConstants, HammerConstants, TimeConstants, AnimationConstants, FontConstants, TextConstants, ImageConstants, SoundConstants):
	LEFT_MOUSE_BUTTON = 1

class Zombie:
	def __init__(self):
		self.index = -1
		self.zombieStatus = -1
		self.anmaionIndex = 0
		self.stayTime = 0
		self.pic = None

	def __init__(self, index, pic):
		self.index = index	# Index để xác định nằm ở mộ có index nào
		self.zombieStatus = 0
		self.animationIndex = 0
		self.stayTime = 0
		self.pic = pic