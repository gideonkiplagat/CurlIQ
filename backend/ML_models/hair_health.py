#Hair quality analysis
import cv2
import numpy as np

def analyze_hair_health(image_path):
    """
    Analyzes the hair health from the provided image path.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: Hair health analysis results.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Thresholding to create a binary image
    _, binary_image = cv2.threshold(blurred_image, 120, 255, cv2.THRESH_BINARY_INV)

    # Find contours of the hair region
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate hair density and health metrics
    hair_density = len(contours) / (image.shape[0] * image.shape[1]) * 100  # Percentage of hair pixels

    # Placeholder for other metrics (e.g., shine, thickness)
    shine_score = np.random.uniform(0, 1)  # Simulated value for shine score
    thickness_score = np.random.uniform(0, 1)  # Simulated value for thickness score

    return {
        "hair_density": hair_density,
        "shine_score": shine_score,
        "thickness_score": thickness_score,
        "health_status": "Healthy" if hair_density > 0.5 else "Unhealthy"
    }
    
    def extract_hair_mask(image):
        """
        Extracts the hair region from the image using color segmentation.

        Args:
            image (numpy.ndarray): Input image.

        Returns:
            numpy.ndarray: Hair mask.
        """
        # Convert to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color range for hair (this may need adjustment based on hair color)
        lower_color = np.array([0, 50, 50])
        upper_color = np.array([180, 255, 255])

        # Create a mask for the hair region
        mask = cv2.inRange(hsv_image, lower_color, upper_color)

        return mask
    