from celery import shared_task
from .helpers import download_video, delete_file, create_folder_from_video_path, delete_folder_from_video_path, \
                    take_screenshot_at_second, get_video_file_clip, get_video_duration, get_video_area, \
                    search_videos_and_add_to_db, detect_video_scenes, mock_search_videos_and_add_to_db
from .models import Query, Video, URL
from django.utils import timezone
from django.db.models import F,Subquery, OuterRef
from server.settings import AUTH_PASSWORD_FOR_REQUESTS, DEBUG
from googleapiclient.errors import HttpError


import logging
logger = logging.getLogger(__name__)

from poseestimator.helpers import get_bbox_area_ratio, check_bbox_score, check_keypoint_visibility, \
                                    max_shoulder_score, max_knee_score, get_pose_inference, \
                                    three_keypoints_among_shoulders_elbows_hands_visible
import time as timeit


'''
@shared_task()
def process_video_without_human(url):
    # load the package only when the task is called
    

    logger.warn(f"Processing video for URL: {url}")

    video_file_path = download_video(url)
    video_dir = create_folder_from_video_path(video_file_path)
    video = get_video_file_clip(video_file_path)
    
    # get the scenes and calculate their durations
    video_scenes = detect_video_scenes(video_file_path, threshold=28.0)
    
    prediction_scenes = []

    for scene in video_scenes:

        video_duration = round(scene[1] - scene[0], 3)
        video_area = get_video_area(video)
        time = scene[0] # start of scene
        
        if video_duration > 3600:
            skip_time = 45
        elif video_duration > 1800:
            skip_time = 30
        elif video_duration > 900:
            skip_time = 20
        elif video_duration > 600:
            skip_time = 15
        elif video_duration > 400:
            skip_time = 10
        elif video_duration > 200:
            skip_time = 5
        elif video_duration > 100:
            skip_time = 2
        else:
            skip_time = 1
        

        prediction = {"overall_prediction" : None, "single_predictions" : [], "quality": None}
        just_skipped = False
        while time < scene[1]: # end of scene
            start = timeit.time()
            print(f"Time: {time}")
            file_path = take_screenshot_at_second(video, time, video_dir)
            print(f"Step 1")
            
            inference_result = get_pose_inference(file_path)
            print(f"Step 2", inference_result)

            number_of_people = len(inference_result['predictions'][0])
            if number_of_people > 1:
                prediction["overall_prediction"] = "multiple"
                logger.warn("Multiple people detected")
                break

            if number_of_people == 1:

                prediction["overall_prediction"] = "single"
                logger.warn("overall prediction: single")

                
                keypoints = inference_result['predictions'][0][0]['keypoint_scores']
                bbox = inference_result['predictions'][0][0]['bbox'][0]
                bbox_score = inference_result['predictions'][0][0]['bbox_score']
                
                bbox_area_ratio = get_bbox_area_ratio(bbox, video_area)

                logger.warn(f"bbox_area_ratio: {bbox_area_ratio}")
                logger.warn(f"bbox_score: {check_bbox_score(bbox_score)}")
                logger.warn(f"keypoints: {check_keypoint_visibility(keypoints)}")
                logger.warn(f"max_shoulder_score: {max_shoulder_score(keypoints)}")
                logger.warn(f"max_knee_score: {max_knee_score(keypoints)}")



                if (bbox_area_ratio > 1/60 and check_bbox_score(bbox_score) and check_keypoint_visibility(keypoints)):
                    # check for HIGH criteria
                    if (bbox_area_ratio > 1/30 and max_shoulder_score(keypoints) >= 0.5 and max_knee_score(keypoints) >= 0.5):
                        if len(prediction["single_predictions"]) > 2 and all([prediction == "high" for prediction in prediction["single_predictions"]]):
                            prediction["quality"] = "high"
                            break

                        prediction["single_predictions"].append("high")

                    # check for MEDIUM criteria
                    elif (bbox_area_ratio > 1/30 and three_keypoints_among_shoulders_elbows_hands_visible(keypoints)):
                        if len(prediction["single_predictions"]) > 2 and all([prediction == "medium" or prediction == "high" for prediction in prediction["single_predictions"]]):
                            prediction["quality"] = "medium"
                            break
                        
                        prediction["single_predictions"].append("medium")

                    else:
                        prediction["single_predictions"] = []  # reset the list
                    
                    time += 1  # only skip one second to skip to the next frame
                    just_skipped = False
                else:
                    time += skip_time
                    just_skipped = True
                    prediction["single_predictions"] = []  # reset the list

            

            elif number_of_people == 0:
                time += skip_time
                just_skipped = True

            print(f"time elapsed: {timeit.time() - start}")
        
        logger.warn(f"Scene duration: {video_duration}")
        logger.warn(f"Scene prediction: {prediction}")

        prediction_scenes.append(prediction)
    
    delete_file(video_file_path)
    delete_folder_from_video_path(video_file_path)

    return video_scenes , prediction_scenes
'''

@shared_task
def query_search():
    logger.warn("Searching for videos with  first 100 Keywords in Query")
    # Subquery to get the top 100 keywords' IDs
    top_100_keywords = Query.objects.order_by('-last_processed', 'use_counter')[:100]
    logger.warning(top_100_keywords)
    logger.warning("Subquery with top 100 Keywords")
    for keyword in top_100_keywords:
        try:
            if DEBUG:
                mock_search_videos_and_add_to_db(keyword.keyword)
                print("Mock search")
            else:
                search_videos_and_add_to_db(keyword.keyword)

        except HttpError as e:
            if e.resp.status == 403 and 'quotaExceeded' in str(e):
                logger.warning("YouTube API quota exceeded: " + str(e))
                break
            else:
                # Handle other HttpErrors
                logger.warning("HTTP error: " + str(e))
                break
        # Updating keyword in query
        if not DEBUG:
            keyword.update_used_keyword
            keyword.save()
        logger.warning(f"Keyword '{keyword.keyword}' queried and urls added to db")
    
        

'''
@shared_task
def process_urls():
    unprocessed_urls = URL.objects.filter(is_processed=False)
    for url_obj in unprocessed_urls:
        process_video_without_human.delay(url_obj.url)
        url_obj.is_processed = True
        url_obj.save()
'''