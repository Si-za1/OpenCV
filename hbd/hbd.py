import cv2
import numpy as np

# Step 1: Create a Blank Image
width = 1400
height = 1200
blank_image = np.zeros((height, width,3), np.uint8)

# Step 2: Set Background Color
background_color = (255, 255, 255)  # White background
blank_image[:] = background_color

# Step 3: Add Text (On the Left Side)
text = "Wishing you a happy birthday!"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (120, 120, 120)  # Black color
text_position = (200, 300)
cv2.putText(blank_image, text, text_position, font, font_scale, font_color, thickness=1)

# Step 4: Add Name (On the Right Corner)
name = "Siza Adhikari"
name_font_scale = 1
name_font_color = (0, 0, 0)  # Dark gray color
name_text_position = (800, 600)  # Adjusted position for the right corner
cv2.putText(blank_image, name, name_text_position, font, name_font_scale, name_font_color, thickness=1)

# Step 5: Load and Add Image (Above the Name)
image = cv2.imread("F:\Leapfrog_data\opencv_projects\hbd\jog.jpg") 
image = cv2.resize(image, (200, 200))  # Resize

# Create a circular mask
mask = np.zeros(image.shape[:2], dtype=np.uint8)
center = (image.shape[1] // 2, image.shape[0] // 2)
radius = min(center[0], center[1])
cv2.circle(mask, center, radius, (255, 255, 255), -1)  # -1 fills the circle

# Apply the circular mask to the image
image = cv2.bitwise_and(image, image, mask=mask)

# Adjusted position above the name
image_position = (800, 320)

# Overlay the circular image above the name
blank_image[image_position[1]:image_position[1] + image.shape[0], image_position[0]:image_position[0] + image.shape[1]] = image

# Step 6: Save the Image
output_filename = "birthday_post.png"
cv2.imwrite(output_filename, blank_image)

# Step 7: Display the Image
cv2.imshow("Birthday Post", blank_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
