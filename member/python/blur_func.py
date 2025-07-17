import cv2
import numpy as np
from ultralytics import YOLO
import numpy as np
from PIL import Image


def bluring(path):

    
    # Load YOLOv8 model for person detection
    person_model = YOLO("yolo11l.pt")

    # Skin color detection thresholds in YCrCb color space
    def detect_skin(image):
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Define lower and upper bounds for skin color
        lower = np.array([60,46,40], dtype=np.uint8)
        upper = np.array([255,247,219], dtype=np.uint8)

        # Mask skin areas
        skin_mask = cv2.inRange(ycrcb, lower, upper)

        # Apply morphological operations to clean up noise
        kernel = np.ones((5, 5), np.uint8)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)

        return skin_mask

    def exists(image):
        #image = cv2.imread(image_path)
        results = person_model(image)
        status = False

        for result in results:
            for i, box in enumerate(result.boxes):
                cls = int(box.cls[0])
                if person_model.names[cls] == "person":
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Crop each detected person
                    person_crop = image[y1:y2, x1:x2]

                    # Skip if detection is too small
                    if person_crop.shape[0] < 50 or person_crop.shape[1] < 50:
                        continue

                    # Detect skin in cropped person region
                    skin_mask = detect_skin(person_crop)
                    skin_pixels = np.sum(skin_mask > 0)
                    total_pixels = person_crop.shape[0] * person_crop.shape[1]

                    # Calculate skin coverage percentage
                    skin_percentage = (skin_pixels / total_pixels) * 100

                    # Determine clothing status
                    if skin_percentage > 30:
                      status = True
                      break
                    else :
                      status = False
            if status:
                break
            else:
                continue

        return status


    def binary_LEFT(i, j):
      mid = int((i + j)/2)
      vidObj.set(cv2.CAP_PROP_POS_FRAMES, mid)
      success, image_mid = vidObj.read()

      if i == j-1:
        return i

      if exists(image_mid):
        return binary_RIGHT(mid, j)
      else:
        return binary_LEFT(i, mid)


    def binary_RIGHT(i, j):
      mid = int((i + j)/2)
      vidObj.set(cv2.CAP_PROP_POS_FRAMES, mid)
      success, image_mid = vidObj.read()
      if i == j-1:
        return i

      if exists(image_mid):
        return binary_RIGHT(mid, j)
      else:
        return binary_LEFT(i, mid)




    vidObj = cv2.VideoCapture(path)

    tot_frame = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(vidObj.get(cv2.CAP_PROP_FPS))


    fight_ahe = []

    for i in range(frame_rate, tot_frame - frame_rate, 2*frame_rate):
      vidObj.set(cv2.CAP_PROP_POS_FRAMES, i)
      success, image = vidObj.read()

      if exists(image):

          vidObj.set(cv2.CAP_PROP_POS_FRAMES, i - frame_rate)
          success, imageL = vidObj.read()

          vidObj.set(cv2.CAP_PROP_POS_FRAMES, i + frame_rate)
          success, imageR = vidObj.read()

          if exists(imageL) and exists(imageR):
            fight_ahe.append([i - frame_rate, i + frame_rate]) # include -m to +m
            print(fight_ahe)

          else:
            if exists(imageL):
               #fight_ahe.append([i - frame_rate, i]) # include -m to 0 and binary on right

              value = binary_RIGHT(i, i + frame_rate)

              fight_ahe.append([i - frame_rate, value])
              print(fight_ahe)

            elif exists(imageR):
              #fight_ahe.append([i, i + frame_rate]) # include 0 to +m and binary on left
              value = binary_LEFT(i - frame_rate, i)
              fight_ahe.append([value, i + frame_rate])
              print(fight_ahe)


            else:
              #binary on both side
              value_L = binary_LEFT(i - frame_rate, i)
              print(value_L)
              value_R = binary_RIGHT(i, i + frame_rate)
              fight_ahe.append([value_L, value_R])
              print(fight_ahe)


      else:
          vidObj.set(cv2.CAP_PROP_POS_FRAMES, i - frame_rate)
          success, imageL = vidObj.read()

          vidObj.set(cv2.CAP_PROP_POS_FRAMES, i + frame_rate)
          success, imageR = vidObj.read()

          if exists(imageL) and exists(imageR):
            fight_ahe.append([i - frame_rate, i + frame_rate]) # include -m to +m
            print(fight_ahe)
          else:
            if exists(imageL):
               #  and binary on left
               value = binary_LEFT(i - frame_rate, i)
               fight_ahe.append([i - frame_rate, value])
               print(fight_ahe)

            elif exists(imageR):
               #  and binary on right
               value = binary_RIGHT(i, i + frame_rate)
               fight_ahe.append([value, i + frame_rate])
               print(fight_ahe)

            else:
              print("kutach nai")

    print(len(fight_ahe))
    print(fight_ahe)

    gaps=[]
    for i in range(len(fight_ahe) - 1):
        # Calculate gap between the end of the current timeframe and the start of the next
        gap_start = fight_ahe[i][1]
        gap_end = fight_ahe[i + 1][0]
        if gap_end == gap_start:
          continue
        else:
          gaps.append([gap_start, gap_end])

    # Print the gap values
    print(gaps)

    timeframes_in_frames = fight_ahe

    # Convert the frame numbers to time in seconds
    timeframes_in_seconds = [(start / frame_rate, end / frame_rate) for start, end in timeframes_in_frames]

    # Print the result
    print(timeframes_in_seconds)




    def pixelate(image, segmentation_mask, pixel_size=69):
        # Convert PIL image to NumPy array
        original_image_numpy = np.array(image)
        height, width, _ = original_image_numpy.shape

        # Convert segmentation mask to NumPy array and resize it
        if isinstance(segmentation_mask, Image.Image):
            segmentation_mask = np.array(segmentation_mask)

        mask_resized = cv2.resize(segmentation_mask, (width, height), interpolation=cv2.INTER_NEAREST)
        mask_binary = (mask_resized > 0).astype(np.uint8)  # Ensure binary mask (0 or 1)

        # Apply pixelation to the entire image
        pixelated_image = original_image_numpy.copy()

        # Loop through the image in blocks
        for y in range(0, height, pixel_size):
            for x in range(0, width, pixel_size):
                # Get the block (a square block of size `pixel_size` x `pixel_size`)
                block = original_image_numpy[y:y+pixel_size, x:x+pixel_size]
                # Compute the average color of the block
                avg_color = block.mean(axis=(0, 1), dtype=int)
                # Apply the average color to the entire block
                pixelated_image[y:y+pixel_size, x:x+pixel_size] = avg_color

        # Use mask to blend pixelated and original images correctly
        result = original_image_numpy.copy()
        for c in range(3):  # Apply mask per channel to avoid color issues
            result[:, :, c] = np.where(mask_binary == 1, pixelated_image[:, :, c], original_image_numpy[:, :, c])

        # Convert result back to PIL image
        #result_image = Image.fromarray(result)
        return result


    #from os import sched_getscheduler




    # Load YOLOv8 model for person detection
    person_model = YOLO("yolo11l-seg.pt")

    # Skin color detection thresholds in YCrCb color space
    def detect_skin(image):
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

        # Define lower and upper bounds for skin color
        lower = np.array([0, 133, 77], dtype=np.uint8)
        upper = np.array([255,247,219], dtype=np.uint8)

        # Mask skin areas
        skin_mask = cv2.inRange(ycrcb, lower, upper)

        # Apply morphological operations to clean up noise
        kernel = np.ones((5, 5), np.uint8)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)

        return skin_mask


    def detect_and_analyze(image):
        #image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = person_model(image)
        results = results[0]

        if type(results) == type(None):
            return image

        if type(results.masks) == type(None):
            return image
        segmentation_masks = results.masks.data
        segments_all = [segmentation_masks[i] for i in range (len(segmentation_masks))]

        for i, box in enumerate(results.boxes):
            cls = int(box.cls[0])
            if person_model.names[cls] == "person":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                person_crop = image[y1:y2, x1:x2]
                if person_crop.shape[0] < 50 or person_crop.shape[1] < 50:
                    continue
                skin_mask = detect_skin(person_crop)
                skin_pixels = np.sum(skin_mask > 0)
                total_pixels = person_crop.shape[0] * person_crop.shape[1]

                # Calculate skin coverage percentage
                skin_percentage = (skin_pixels / total_pixels)
                a = skin_pixels % total_pixels
                b = skin_pixels // total_pixels
                c = a+b

                segs = segments_all[i]
                img_arr = segs.cpu().numpy()

        ###### expected error in format mismatch between PIL IMage

                c = c*100
                print(c)
                if c > 20:
                    print("bluring initiated")
                    res = pixelate(image, img_arr)
                    return res
                else:
                    print("no")
                    return image
            #     res = blur(image, skin_mask)
            #     return res

            # else:
            #     return image
        # #return image



    # Load YOLO model
      # Change to your custom model if needed

    # Load the video
    video_path = path
    output_path = "D:\\Desktop\\Video_Edit_Function\\New folder\\Demo1_Interface\\demo1\\member\\media\\Blur_output.mp4"

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Define the time segments where YOLO should be applied (start, end) in seconds
    time_segments = timeframes_in_seconds  # Modify this with your timeframes
    frame_segments = [(int(start * fps), int(end * fps)) for start, end in time_segments]

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0  # Keep track of frame index

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Stop if video ends

        # Check if the current frame is within a processing segment
        process_frame = any(start <= frame_idx <= end for start, end in frame_segments)

        if process_frame:
             frame = detect_and_analyze(frame) # Get the frame with detections

        # Write frame (processed or not) to output video
        out.write(frame)

        frame_idx += 1  # Move to next frame

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Processed video saved as {output_path}")
