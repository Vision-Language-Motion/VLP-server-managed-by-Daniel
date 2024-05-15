import cv2
import os
import shutil
import json
from mmpose.apis import MMPoseInferencer
from mmpretrain.models import VisionTransformer
import time


start_time = time.time()
inferencer = MMPoseInferencer('rtmpose-l')

def process_video(video_path, base_output_dir, save_frames, save_video, save_pose_image):
    video_name = os.path.basename(video_path).split('.')[0]
    video_output_dir = os.path.join(base_output_dir, 'temp', video_name)  # save temporal result
    os.makedirs(video_output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_area = frame_width * frame_height
    min_bbox_area = frame_area / 60  # figure should be bigger than 1/60 of frame area
    
    frame_count = 0
    frame_paths = []  # store frame
    people_counts = []  # store number of visible human
    frame_qualities = []  # save frame quality（high, medium, low）
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 30 == 0:  # sample per 30 frames
            frame_path = os.path.join(video_output_dir, f'{frame_count}.png')
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            if save_pose_image: #choose save the pose image or not
                vis_out_path = os.path.join(video_output_dir, f'{frame_count}_pose.png')
                result_generator = inferencer(frame_path, pred_out_dir=video_output_dir, vis_out_dir=vis_out_path, draw_bbox=True)
            else:
                result_generator = inferencer(frame_path, pred_out_dir=video_output_dir)
            next(result_generator)
        frame_count += 1
    
    cap.release()

    for frame_path in frame_paths:
        json_path = frame_path.replace('.png', '.json')
        with open(json_path, 'r') as file:
            data = json.load(file)
            visible_people = 0
            for person in data:
                scores = person['keypoint_scores']
                bbox = person['bbox'][0]
                bbox_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                bbox_score = person['bbox_score']
                head_points = scores[:5]
                other_points = scores[5:]
                visible_head_points = sum(score >= 0.7 for score in head_points)
                visible_other_points = sum(score >= 0.35 for score in other_points)
                visible_points = visible_head_points + visible_other_points
                if bbox_area >= min_bbox_area and bbox_area < frame_area and bbox_score >= 0.4 and visible_points >= 5:
                    visible_people += 1
                    shoulders_visible = scores[5] >= 0.5 or scores[6] >= 0.5
                    knees_visible = scores[13] >= 0.5 or scores[14] >= 0.5
                    arms_hands_visible = sum(scores[i] >= 0.5 for i in [5, 6, 7, 8, 9, 10]) >= 3
                    if shoulders_visible and knees_visible and bbox_area/frame_area > 1/30:
                        frame_qualities.append("high")
                    elif arms_hands_visible and bbox_area/frame_area > 1/30:
                        frame_qualities.append("medium")
                    else:
                        frame_qualities.append("low")
                
            people_counts.append(visible_people)
        
    # classify after number of human figure(single, multiple, nohuman)
    if all(count == 0 for count in people_counts):
        destination_folder = 'nohuman'
    elif any(people_counts[i] > 1  for i in range(len(people_counts))):
        destination_folder = 'multiple'
    else:
        destination_folder = 'single'
        #further subdivision in single category
        high_count = sum(1 for i in range(len(frame_qualities) - 2) if all(q == "high" for q in frame_qualities[i:i+3]))
        medium_count = sum(1 for i in range(len(frame_qualities) - 2) if all(q in ["medium", "high"] for q in frame_qualities[i:i+3]))
        if high_count > 0:
            destination_folder = os.path.join('single', 'high')
        elif medium_count > 0:
            destination_folder = os.path.join('single', 'medium')
        else:
            destination_folder = os.path.join('single', 'low')

    final_video_dir = os.path.join(base_output_dir, destination_folder)
    final_json_dir = os.path.join(final_video_dir, video_name)
    os.makedirs(final_video_dir, exist_ok=True)
    os.makedirs(final_json_dir, exist_ok=True)
    
    if save_video: #choose save original video or not
        shutil.copy(video_path, final_video_dir)
    for frame_path in frame_paths:
        json_path = frame_path.replace('.png', '.json')
        shutil.copy(json_path, final_json_dir)
        if save_pose_image:
            pose_image_path = frame_path.replace('.png', '_pose.png')
            shutil.copy(pose_image_path, final_json_dir)
        if save_frames:
            shutil.copy(frame_path, final_json_dir)
        else:
            os.remove(frame_path)

    shutil.rmtree(os.path.join(base_output_dir, 'temp'))


video_folder = '/home/markusc/MyP/openpose_estimation/webvid1k' # input video folder, change to your own path
base_output_dir = '/home/markusc/MyP/mmpose_estimation/process_in_batch/rtml24webvid1k' #output folder, change to your own path
save_frames = False #trigger to save original frame
save_video = False #trigger to save original video
save_pose_image = False #trigger to save pose image
video_formats = ['.mp4', '.avi', '.mov', '.mkv'] # add more video format if needed

for video_file in os.listdir(video_folder):
    video_path = os.path.join(video_folder, video_file)
    if os.path.isfile(video_path) and any(video_file.endswith(fmt) for fmt in video_formats):  
        process_video(video_path, base_output_dir, save_frames, save_video, save_pose_image)
