# SneakPic - organizing your pictures with AI

# intro

<p>
SneakPic allows you to arrange, analyze and search for insights in your photo collection by using a YOLOv5 ML model under the hood.
you can search for objects detected from your photo album collections by filtering according those tags not similar to any conventional photo album :) 
</p>
# An installation and how to use demo video
Please watch the video in this link https://youtu.be/CAjbHjZah28

## Arcitecture

This app composed from the following components:
Backend:
<ul>
    <li>Backend microservice: FastApi + uvicorn ASGI
    <li>DB microservice: mongoDB
    <li>*ML repository: Pytourch which accommodates the YOLOv5 ML models for detection
</ul>
Frontend:
<ul>
    <li>web Microservice: streamlit web server
</ul>
the following diagram describes the architecture:

![architecture](https://user-images.githubusercontent.com/83791207/217057456-320ffd45-3a89-4b01-bcc4-41e040067823.png)



## How to Install SneakPic?
This app is designed to run as containers on Docker env.
### If you have Windows OS
Verify that you have WSL 2.0 and Docker Desktop installed on your system.
after downloading the source code, locate the content inside the WSL Virtual machine in a designated path,
by copying it from Window os to the WSL virtual machine by the following command

```
cp -r /mnt/c/[the place where the source code is stored] /[destination dir in the WSL VM]

```

### For linux and Windows users
After locating the source code in the destination path, we can proceed towards building the app via docker compose:
```
docker compose build

```
it will take a while (about 10 to 15 minutes), after the build process is completed just run the following:
```
docker compose up

```

and that is it :)

### How to use?

For regular usage navigate to http://localhost:8081 - you will redirect to the app

#### Advance use

For maintenance and testing purposes you can navigate to the API interface by browsing to http://localhost:8080/docs - you will redirect to the Swagger landing page where you can test the app using the Test route, very important to first create a Test database (it is the first post endpoint as shown in the snip below), and then you can proceed and test the functionality/flow of the application in a testing environment.
![swagger-test](https://user-images.githubusercontent.com/83791207/217056945-28b1a5e0-f9c6-457e-8e35-29551bbf41c6.png)

For troubleshooting just navigate to the production route
![swagger-production](https://user-images.githubusercontent.com/83791207/217056913-db841f64-30b9-45f4-9470-bbf931b67872.png)


# An installation and how to use demo video
Please watch the video in this link https://youtu.be/CAjbHjZah28


## Here some snips

![app collection](https://user-images.githubusercontent.com/83791207/217056849-e77fce96-5707-4c8e-84f6-9def14b34201.png)


![app_detection](https://user-images.githubusercontent.com/83791207/217056876-542797de-aee8-4bc3-8f86-2fa125c9a32f.png)

![app_filtering](https://user-images.githubusercontent.com/83791207/217056891-5f1567d6-5732-485a-aa02-daeced47069f.png)







