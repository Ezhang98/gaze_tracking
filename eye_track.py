import cv2
import random
import numpy as np
import dlib
from math import hypot
from pygame.locals import *
from random import randint
import pygame
import time
import os
import sys

def midpoint(p1 ,p2):
	return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points, facial_landmarks, frame):
	left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
	right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
	center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
	center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

	#hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
	#ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

	hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
	ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

	ratio = hor_line_lenght / ver_line_lenght
	return ratio

def get_gaze_ratio(eye_points, facial_landmarks, frame, gray):
	left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
								(facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
								(facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
								(facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
								(facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
								(facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
	cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)

	height, width, _ = frame.shape
	mask = np.zeros((height, width), np.uint8)
	cv2.polylines(mask, [left_eye_region], True, 255, 2)
	cv2.fillPoly(mask, [left_eye_region], 255)
	eye = cv2.bitwise_and(gray, gray, mask=mask)

	min_x = np.min(left_eye_region[:, 0])
	max_x = np.max(left_eye_region[:, 0])
	min_y = np.min(left_eye_region[:, 1])
	max_y = np.max(left_eye_region[:, 1])

	gray_eye = eye[min_y: max_y, min_x: max_x]
	_, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
	height, width = threshold_eye.shape
	left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
	left_side_white = cv2.countNonZero(left_side_threshold)

	right_side_threshold = threshold_eye[0: height, int(width / 2): width]
	right_side_white = cv2.countNonZero(right_side_threshold)

	if left_side_white == 0:
		gaze_ratio = 1
	elif right_side_white == 0:
		gaze_ratio = 5
	else:
		gaze_ratio = left_side_white / right_side_white
	return gaze_ratio

def draw_targets(window, display_h, display_w):
	radius = 30
	for i in range(1,4):
		pygame.draw.circle(window, pygame.Color(255, 0, 0), (display_w/7, display_h*i/4), radius, 0)	
	for i in range(1,4):
		pygame.draw.circle(window, pygame.Color(255, 0, 0), (display_w/2, display_h*i/4), radius, 0)	
	for i in range(1,4):
		pygame.draw.circle(window, pygame.Color(255, 0, 0), (display_w - display_w/7, display_h*i/4), radius, 0)	

def App():

	detector = dlib.get_frontal_face_detector()
	font = cv2.FONT_HERSHEY_PLAIN
	predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
	pygame.display.init()

	#get display size
	display_h = pygame.display.Info().current_h
	display_w = pygame.display.Info().current_w

	# logo = pygame.image.load("logo32x32.png")
	# pygame.display.set_icon(logo)
	pygame.display.set_caption("minimal program")

	#create new "full-screen" window
	window = pygame.display.set_mode((display_w , display_h))

	# Counters


	directory = os.fsencode("test")

	# for file in os.listdir(directory):
		# filename = os.fsdecode(file)
		# print(filename)
	processFile("./test/" + "right_gonzalo.mov", window, detector, predictor, font, display_h, display_w)
	quit()
 	# if filename.index(""): 
     # print(os.path.join(directory, filename))
#      continue
#  else:
#      continue

	cv2.destroyAllWindows()	


def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return pygame.Color(rgbl[0],rgbl[1],rgbl[2])

def processFile(filename, window, detector, predictor, font, display_h, display_w):
#Wait for capture to start
	cap = cv2.VideoCapture(filename)

	#frame counter
	frames = 0

	# show frame
	# while(not cap.isOpened()):
	while(True):
		_, frame = cap.read()
		if(frame is None):
			print("Frame is none")
			break
		#cv2.waitKey(1)
		time.sleep
		cv2.imshow("Frame", frame)

		# face detection
		frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

		frames += 1
		new_frame = np.zeros((500, 500, 3), np.uint8)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = detector(gray)

		for face in faces:
			x, y = face.left(), face.top()
			x1, y1 = face.right(), face.bottom()
			cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

			landmarks = predictor(gray, face)

			# Detect blinking
			# left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks, frame)
			# right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks, frame)
			# blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

			# print(blinking_ratio)
			# if blinking_ratio > 5.7:
			# cv2.putText(frame, "BLINKING", (50, 150), font, 7, (255, 0, 0))

			# Gaze detection
			gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks, frame, gray)
			gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks, frame, gray)
			gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
			# print("Pre_gaze: ", gaze_ratio)
			# window.fill((0,0,0))

			eventList = pygame.event.get()

			if(eventList):
				event = eventList[0]
				if event.type == pygame.QUIT:
					break
			# if event.type == pygame.MOUSEMOTION:
			# 	m_pos = pygame.mouse.get_pos()
			# 	print("Mouse: " ,m_pos)

			sight_x = 2880 + int(gaze_ratio * -2880/3)
			# sight_y = int((blinking_ratio-3)*1800/2)

	# 		print("Gaze: " , gaze_ratio)
	# 		print("Blink: ", blinking_ratio)

	# 		#print("Eyes: ",(sight_x, sight_y))
			draw_targets(window, display_h, display_w)
	# 		#NOTE: Holding y constant to test X values using gaze ratio
			if(sight_x > display_w):
				sight_x = display_w
			if(sight_x < 0):
				sight_x = 0
			pygame.draw.circle(window, random_color(), (sight_x, display_h/2), 20, 2)	
			pygame.display.update()

	cap.release()
	cv2.destroyAllWindows()	
	return



#cap = cv2.VideoCapture(0)

	# while True:
	# 	sight_x = 0
	# 	sight_y = 0		

	# 	gaze_ratio = 0
	# 	blinking_ratio = 0

	# 	_, frame = cap.read()
	# 	if(frame is None):
	# 		print("Frame is none")
	# 		break

	# 	frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

	# 	frames += 1
	# 	new_frame = np.zeros((500, 500, 3), np.uint8)
	# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# 	faces = detector(gray)

	# 	for face in faces:
	# 		x, y = face.left(), face.top()
	# 		x1, y1 = face.right(), face.bottom()
	# 		cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

	# 		landmarks = predictor(gray, face)

	# 		# Detect blinking
	# 		# left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks, frame)
	# 		# right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks, frame)
	# 		# blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

	# 		# print(blinking_ratio)
	# 		# if blinking_ratio > 5.7:
	# 		# cv2.putText(frame, "BLINKING", (50, 150), font, 7, (255, 0, 0))


	# 		# Gaze detection
	# 		gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks, frame, gray)
	# 		gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks, frame, gray)
	# 		gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
	# 		print("Pre_gaze: ", gaze_ratio)


	# 		cv2.imshow("Frame", frame)
	# 		# cv2.imshow("New frame", new_frame)
	# 		# if(gaze_ratio < 0):
	# 		#	  gaze_ratio = 0
	# 		# if(gaze_ratio > 3):
	# 		#	  gaze_ratio = 3
	# 		# print(gaze_ratio)
	# 		#2880x 1800
	# 		# 3 - 0
	# 		# 0 - 2880

	# 		# cv2.moveWindow("New frame", 2880 + int(gaze_ratio * -2880/3) , int(1800/4))
	# 		# if gaze_ratio <= 1:
	# 		#	  cv2.putText(frame, "RIGHT", (50, 100), font, 2, (0, 0, 255), 3)
	# 		#	  new_frame[:] = (0, 0, 255)

	# 		# elif 1 < gaze_ratio < 1.7:
	# 		#	  cv2.putText(frame, "CENTER", (50, 100), font, 2, (0, 0, 255), 3)

	# 		# else:
	# 		#	  new_frame[:] = (255, 0, 0)
	# 		#	  cv2.putText(frame, "LEFT", (50, 100), font, 2, (0, 0, 255), 3)
	# 		window.fill((0,0,0))

	# 		eventList = pygame.event.get()

	# 		if(eventList):
	# 			event = eventList[0]
	# 		if event.type == pygame.QUIT:
	# 			break
	# 		if event.type == pygame.MOUSEMOTION:
	# 			m_pos = pygame.mouse.get_pos()
	# 			print("Mouse: " ,m_pos)

	# 		sight_x = 2880 + int(gaze_ratio * -2880/3)
	# 		sight_y = int((blinking_ratio-3)*1800/2)

	# 		print("Gaze: " , gaze_ratio)
	# 		print("Blink: ", blinking_ratio)

	# 		#print("Eyes: ",(sight_x, sight_y))
	# 		draw_targets(window, display_h, display_w)
	# 		#NOTE: Holding y constant to test X values using gaze ratio
	# 		pygame.draw.circle(window, random_color(), (sight_x, display_h/2), 20, 2)	
	# 		pygame.display.update()

	# 	# if cv2.waitKey(100) == ord('q'):
	# 	# break

	
	

if __name__ == "__main__" :
	App()
