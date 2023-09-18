import cv2
import cvzone

# Load the background image with alpha channel
background = cv2.imread(r"F:\Leapfrog_data\opencv_projects\hbd\bg.jpg", cv2.IMREAD_UNCHANGED)
print(background.shape)

# Load the image to be overlaid
balloon = cv2.imread(r"F:\Leapfrog_data\opencv_projects\hbd\balloon.png", cv2.IMREAD_UNCHANGED)
print(balloon.shape)

birthday = cv2.imread(r"F:\Leapfrog_data\opencv_projects\hbd\birthday.png", cv2.IMREAD_UNCHANGED)
print(birthday.shape)

person = cv2.imread(r"F:\Leapfrog_data\opencv_projects\hbd\person.png", cv2.IMREAD_UNCHANGED)
print(person.shape)

# # First create the image with alpha channel
# birthday = cv2.cvtColor(birthday, cv2.COLOR_RGB2RGBA)
# First create the image with alpha channel
background = cv2.cvtColor(background, cv2.COLOR_RGB2RGBA)

# Then assign the mask to the last channel of the image
background[:, :, 3] = 0.5

background = cv2.resize(background, (1600, 1800))
balloon =cv2.resize(balloon, (200,200))
birthday = cv2.resize(birthday, (300,300))
person = cv2.resize(person, (200,200))

ImageOverlay = cvzone.overlayPNG(background, balloon, pos=[100, 100])
ImageOverlay = cvzone.overlayPNG(ImageOverlay, birthday, pos=[50, 230])
ImageOverlay = cvzone.overlayPNG(ImageOverlay, person, pos=[1000, 280])

name = "Siza Adhikari"
font = cv2.FONT_HERSHEY_SIMPLEX
name_font_scale = 1
name_font_color = (0, 0, 0)  # Dark gray color
name_text_position = (1000, 500)  # Adjusted position for the right corner

# Corrected usage of cv2.putText
cv2.putText(ImageOverlay, name, name_text_position, font, name_font_scale, name_font_color, thickness=1)

# Saving the output filename
output_filename = "blended_template.png"
cv2.imwrite(output_filename, ImageOverlay)

while True:
# Overlay the image on the background
    # Display the result
    cv2.imshow('Blended Image', ImageOverlay)
    # Wait for a key press and check if it's the 'Esc' key (ASCII 27)
    key = cv2.waitKey(1)
    if key == 27:  # If 'Esc' key is pressed
        break

cv2.destroyAllWindows()
