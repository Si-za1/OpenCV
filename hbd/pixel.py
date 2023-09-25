import cv2
import numpy as np

# Loading the background image
background = cv2.imread(r"F:\Leapfrog_data\opencv_projects\hbd\welcometemplate_720.png", cv2.IMREAD_UNCHANGED)
print(background.shape)

# Defining the photo file paths and positions
photo_info = [
    {"file_path": r"F:\Leapfrog_data\opencv_projects\hbd\jog.jpg", "position": (70, 179)},
    {"file_path": r"F:\Leapfrog_data\opencv_projects\hbd\jog.jpg", "position": (295, 175)},
    {"file_path": r"F:\Leapfrog_data\opencv_projects\hbd\jog.jpg", "position": (520, 180)}
]

# Common dimensions for photos to be inserted
photo_width = 130
photo_height = 150

# Perform alpha composition for each photo
for idx, photo_data in enumerate(photo_info):
    # Load the photo image
    photo = cv2.imread(photo_data["file_path"], cv2.IMREAD_UNCHANGED)
    
    # Resize the photo to the desired dimensions
    photo = cv2.resize(photo, (photo_width, photo_height))
    
    # Create an alpha channel for the photo
    alpha_channel = np.ones((photo_height, photo_width), dtype=photo.dtype) * 255
    photo = cv2.merge((photo, alpha_channel))
    
    # Get the dimensions of the background image
    background_height, background_width, _ = background.shape
    
    # Calculate the position to align the photo
    x_position, y_position = photo_data["position"]
    
    # Perform alpha composition for each channel
    for c in range(0, 3):
        background[y_position:y_position + photo_height, x_position:x_position + photo_width, c] = \
            background[y_position:y_position + photo_height, x_position:x_position + photo_width, c] * \
            (background[y_position:y_position + photo_height, x_position:x_position + photo_width, 3] / 255.0) + \
            photo[:, :, c] * (1 - background[y_position:y_position + photo_height, x_position:x_position + photo_width, 3] / 255.0)

# Display the resulting image
cv2.imshow("Birthday_image", background)
cv2.waitKey(0)
cv2.destroyAllWindows()
