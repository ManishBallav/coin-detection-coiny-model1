import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
%matplotlib inline

coins = cv2.imread('coins.jpg', 1)
coins = cv2.cvtColor(coins,cv2.COLOR_BGR2RGB)
plt.imshow(coins)
plt.axis('off')

min_r = 104
max_r = 106

def edge_detect_coins():

    coins_height, coins_width, coins_channel = coins.shape

    # optimisation by decreasing the size of image, resulting in 4x faster run time
    coins_resized = cv2.resize(coins, (int(coins_width/2), int(coins_height/2)))

    # blur to optimise edge finding
    coins_blurred = cv2.GaussianBlur(coins_resized, (5, 5), cv2.BORDER_DEFAULT)

    # used Canny to find the edge
    coins_edge = cv2.Canny(coins_blurred, 127, 255)

    cv2.imwrite("coins_blurred.jpg", coins_blurred)
    cv2.imwrite("coins_edge.jpg", coins_edge)

    return coins_edge

hello = edge_detect_coins()
hello = cv2.cvtColor(hello,cv2.COLOR_BGR2RGB)
plt.imshow(hello)

def coin_center_detect():

    
    coins_edge = edge_detect_coins()

    max_height, max_width = coins_edge.shape

    edge_threshold = 0.075  # how many pixels need to pass to be considered a coin edge
    intensity_threshold = 255 * 0.09  # the min value of pixel intensity to be considered edge
    next_circle_step = 3  # the amount of pixels to move to start comparing again
    coin_detection = []

   
    for radius in range(min_r, max_r):
        img_circle = np.zeros((radius * 2, radius * 2, 1), np.uint8)
        circle = cv2.circle(img_circle, (radius, radius), radius, 255)

        circumference = 2 * math.pi * radius

        circle_pixels = []

        for y in range(len(circle)):
            for x in range(len(circle[y])):
                if circle[x][y] == 255:
                    circle_pixels.append((x, y))

        print(('radius', radius))

        
        for start_y in range(0, max_height - 2 * radius, next_circle_step):
            for start_x in range(0, max_width - 2 * radius, next_circle_step):
                count = 0

        
                for (x, y) in circle_pixels:
                    image_y = start_y + y
                    image_x = start_x + x

                    if coins_edge[image_y][image_x] >= intensity_threshold:
                        count += 1

                if count > 50:
                    percentage = round(count / circumference * 100, 2)
                    coor_x = start_x + radius
                    coor_y = start_y + radius
                    print(('candidate', coor_x, coor_y, radius, percentage))

                if (count / circumference) > edge_threshold:
                    coor_x = start_x + radius
                    coor_y = start_y + radius
                    coin_detection.append((coor_x, coor_y, radius))  # center
                    print(('-----------------', start_x + radius, start_y + radius, radius))

    return coin_detection

def circle_coins():

    coins_circled = coin_center_detect()
    coins_copy = coins.copy()
    for detected_circle in coins_circled:
        x_coor, y_coor, detected_radius = detected_circle
        coins_detected = cv2.circle(coins_copy, (x_coor*2, y_coor*2), detected_radius*2, (0, 0, 255), 1)

    cv2.imwrite("coins_detected.jpg", coins_detected)

new2 = circle_coins()

