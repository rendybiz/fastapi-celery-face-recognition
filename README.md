## Project : Image Face Detection and Crop the files

## Brief
This Project is based on requirements v.0.1.
The requirements are put into single file in requirements.v.0.1.md

## What inside?

* Python 3
* celery 4.4.7
* fastapi 0.64.0
* flower 0.9.7
* pytest 6.2.4
* redis 3.5.3
* uvicorn 0.13.4
* openpyxl 3.0.10
* opencv-python
* pandas 1.4.2
* pandas-gbq 0.17.6

## Prerequisites
This docker was build under Ubuntu 20.04 focal OS.
You need to run the redis server before running this main docker-compose

I put also the docker-compose for redis under ```/redis``` directory. Try to run ```docker-compose up``` under redis directory, it will run your redis container as well.

- ### Steps
  1. Run your redis server first
  2. Edit ```/docker-compose.yml``` file.
        please check  ```environment:``` props for each yml services.  you will see that the main host domain is still in {IP address} form. You need to modify or change the IP address into proper IP address for your redis-server.
  3. Do **Quick Run** Below

## Quick Run
Repository have a docker-compose inside. so you just need to run it using your docker-compose

``` sudo docker-compose up ``` or ``` sudo docker-compose up -d ```

it will create 3 containers
- Web Service , REST API [port: 8004]
- Celery Worker 
- Dashboard, Check Celery task [port: 5556]

Please check and make sure your docker services running smoothly e.g:
``` sudo docker ps ```



## About docker-compose.yml
Dashboard service is an *optional*. It was used to check your celery task stacks.

## Structures
```
.
├── docker-compose.yml // Your main docker services
├── project
│   ├── debug-go-info.log
│   ├── debug-info.log // debug log
│   ├── Dockerfile
│   ├── logs
│   │   └── celery.log // Celery Logs info
│   ├── main.py // Main Runner
│   ├── requirements.txt // Python libraries prerequisites
│   ├── restbook // Restbook REST API Docs
│   │   ├── get.face_recognition.restbook
│   │   └── get.redis_key_clean_up.restbook
│   ├── static // Static files 
│   │   ├── cascade_face.xml
│   │   ├── face-results // Results files
│   │   └── peoples // main files before cropped by tools
│   ├── tests // Unit testing, using pytest
│   │   ├── conftest.py
│   │   ├── __init__.py
│   │   └── test_tasks.py
│   └── worker.py
├── README.md // Read Me First, Please
├── redis // Optional Redis server
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── redis.conf
└── requirements.v.0.1.md
```

## How it works
1. After running your all docker services you can go to our REST API for 
    - ```GET http://localhost:8004/face_recognition```
        By running this REST, it willl return the task id and run the background processing for:
        1. Get the list of files under ```/static/peoples```
        2. image Face recognitions
        3. Face cropping
        4. Save the result into ```/static/face-results```. Filename shouldbe like this ```{filename}-face{number}.{extfile}```
2. You can see the current background processing of celery task in our celery dashboard by using http://localhost:5556/
3. You can run our face_recognition rest multiple times or deploy it in any instances.
   
    In order to filling our requirements about `*does not eat the same file if the file is in processing status or has been processed.*`, I manage it to store the current running to Redis key. So as long as you targeting our services to same redis-server it will not eat the same file.
4. If you want to re-test your face_recognition, you need to delete ```face-results/*``` files and run our ```GET http://localhost:8004/redis_key_clean_up```

## Tricks
You can use Restbook [Restbook VCode](https://marketplace.visualstudio.com/items?itemName=tanhakabir.rest-book) to run Our REST API

For Further information and detail you can try to create new issues in my repo

Thank you
