# Data Cleaning pipeline task by Kopernikus

## About the dataset:

- This dataset comprises images depicting covered parking lots.
- Multiple cameras have been employed to capture diverse perspectives within the dataset.
- Each image is labeled with a unique identifier composed of the camera ID and timestamp.
- Timestamps are provided in two formats: Unix and Python datetime.
- The images encompass various times of the day.
- Some images may contain noise, and there are instances where images are labeled as None.
- Images vary in size.

## How does the code work?

The entire process is repeated for each unique camera_id to systematically identify and mark images for removal across all cameras.

1. Each camera provides a distinct viewpoint, so we organize the dataset based on the camera_id. We maintain a dictionary that associates each camera_id with its corresponding set of images.
2. To facilitate sorting, we convert Python datetime objects to Unix timestamps. This ensures chronological ordering of the images across all cameras.
3. We sort the images based on their timestamps. This step is crucial as images captured closer in time are more likely to exhibit similarities.
4. We define a sliding window mechanism to efficiently compare images. This involves selecting a base image and comparing it with others within a specified window.
5. To optimize processing, we implement a caching mechanism. This prevents the unnecessary reloading of images within a window, improving overall efficiency.
6. The first image within a window is chosen as the base image for comparison. Subsequent images within the window are compared against this base image
7. Images are compared using a scoring mechanism, and if the score exceeds a predefined threshold, the image path is marked for removal.
8. Remove the images marked for removed for a camera id.


# Choosing the right values

The values for min_contour_area and min_score were chosen with experimentation.
We chose  min_contuor_area as 100 and min_score as 3000.

Starting with conservative values and analysing the results these score were estimated to be giving good results.

# How to improve data-collection

- **Curated Images**: By using deep learning models to selectively capture images based on specific criteria, you can focus on collecting only the relevant data for your use case. For instance, in a parking lot scenario, you can capture images containing only cars. This reduces the amount of irrelevant data and makes data storage and processing more efficient. By selectively capturing and storing only the necessary images, you can significantly reduce storage costs and optimize computational resources.
- **GDPR Compliant**: If required by the law, faces and license plates must be blurred. This will save the company from future legal troubles.
- **Image naming**: Choose a consistent image naming scheme for consistency purposes and avoid any future confusion and errors.
- **All angles**: For a given timestamp image of a parking lot must be taken from all cameras for better scene understanding.
