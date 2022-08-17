Task : 
Build a service application using the Python programming language to detect and crop face frames.

Requirements: 
You are allowed to use any library, but with the following conditions:
1. The application can run on a replicable docker ecosystem.
2. Try to ensure that each instance gets the same list of file portions and does not eat the same file if the file is in processing status or has been processed.
3. Also provide a brief explanation for the installation, we expect your program to run directly on the operating system or on docker replication

Save your code in an open repository, so we can monitor progress and results.

Good luck!

POSSIBLE STEPS:
1. Prepare your image list with Faces
2. Try to looking for a library that supported for Face detection like OpenCV
3. Load any required Libraries to docker
4. My assumption, it have possibilities to run in multiple instance. 1 instance 1 docker.
5. We can use Redis as a cloud state service to share which file are under processing or not. And cannot process the same file in different instances.
6. In a single image, it could be have multiple faces
7. any faces will stored into specific folder/dir
8. QA Test for running in multiple call / instances.