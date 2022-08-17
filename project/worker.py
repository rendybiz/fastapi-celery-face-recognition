# Import global need
import  os
import  time
from    celery.utils.log import get_task_logger
from    celery import Celery
from    any_modules import compare
import  redis
import  cv2

celery      = Celery(__name__)

celery.conf.broker_url     = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

redis_host  = os.environ.get("REDIS_HOST", "192.168.160.1")
redis_port  = os.environ.get("REDIS_PORT", "6379")
redis_db    = os.environ.get("REDIS_DB", "0")
logger      = get_task_logger(__name__)

redis_con   = redis.Redis(host=redis_host, port=int(redis_port), db=int(redis_db))
redis_prefix= "img_"

convert_to_gbq_enabled = True
basepath       = 'static/peoples/'
base_face_path = 'static/face-results/'

@celery.task(name="create_task")
def create_task(task_type):
    print("task test!")
    return True

@celery.task(name="face_recognition_task")
def face_recognition_task(request):
    response = True
    try:
        for filebase_name in os.listdir(basepath):
                if os.path.isfile(os.path.join(basepath, filebase_name)):
                    file_name, file_extension = os.path.splitext(filebase_name)
                    print("file name "+ file_name + " " +file_extension)
                    
                    """ Check the availability on redis"""
                    
                    rds_key = redis_prefix+filebase_name
                    fn_redis = redis_con.get(rds_key)
                    if not(fn_redis):
                        print("fn_redis Not", fn_redis)
                        redis_con.set(rds_key, 1)
                    else :
                        print("fn redis exist", fn_redis)
                        continue
                        

                    # setfoo = r.set('foo', 'bar')
                    # foo = r.get('foo')
                
                    image_path = basepath+filebase_name
                    casc_path  = "static/cascade_face.xml"

                    # # Create the haar cascade
                    faceCascade = cv2.CascadeClassifier(casc_path)

                    # # Read the image
                    image   = cv2.imread(image_path)
                    gray    = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    """
                    Detect faces(plural): multiple faces in single image
                    example : static/peoples/peoples1.jpeg
                    faces   : static/face-results/peoples1-face1.jpeg, 
                            static/face-results/peoples1-face1.jpeg, 
                            etc
                    """
                    
                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags = cv2.CASCADE_SCALE_IMAGE
                    )

                    print("Found {0} faces!".format(len(faces)))

                    # Cropping the multiple faces in single image
                    """ Faces could have more than 1 face"""
                    
                    face_n = 1
                    for (x, y, w, h) in faces:
                        # cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 255), 2)
                        faces = image[y:y + h, x:x + w]
                        target_file = base_face_path + file_name+"-face"+str(face_n)+file_extension
                        print("target_file : "+target_file)
                        cv2.imwrite(target_file, faces)
                        face_n+=1
                    
                    """ Sleep 2 seconds as pretending that processing data take a longer process"""
                    time.sleep(2) # <--- comment it when unnecessary
    except OSError as err:
        response = False
        print("OS error: {0}".format(err))
    except BaseException as err:
        response = False
        print("Unknown error in workers", err)
   

    return response


@celery.task(name="redis_key_clean_up")
def redis_key_clean_up(request):
    for filebase_name in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, filebase_name)):
            file_name, file_extension = os.path.splitext(filebase_name)
            print("file name "+ file_name + " " +file_extension)
            
            """ Check the availability on redis"""
            
            rds_key = redis_prefix+filebase_name
            fn_redis = redis_con.get(rds_key)
            if(fn_redis):
                redis_con.delete(rds_key)
