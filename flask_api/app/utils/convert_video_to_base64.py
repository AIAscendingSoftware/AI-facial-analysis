
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def video_to_base64(video_path):
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
        base64_string = base64.b64encode(video_bytes).decode('utf-8')
    return base64_string

def base64_to_video(base64_string, output_path):
    # print(base64_string,len(base64_string),type(base64_string),'this is base64_string')
    try:
        # Decode the Base64 string back to bytes
        video_bytes = base64.b64decode(base64_string)
        # print('video_bytes:',video_bytes,'thisd is video_bytes ')
        # Write the bytes to a video file
        with open(output_path, "wb") as video_file:
            video_file.write(video_bytes)
        return output_path

    except Exception as e:
        return f"Error decoding Base64 and saving video: {e}"

def converting_image_base64_into_image(base64_string):
    
    # Decode the base64 string
    image_data = base64.b64decode(base64_string)

    # Convert bytes to a PIL Image
    image = Image.open(BytesIO(image_data))
    print('converting_image_base64_into_image function is running and showing the image')
    # Show the image
    plt.imshow(image)
    plt.axis('off')  # Hide axes
    plt.show()