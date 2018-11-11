Disclaimer: This project is not under active development anymore

# Project Fib

In the current media landscape, control over distribution has become almost as important as the actual creation of content, and that has given Facebook a huge amount of power. The impact that Facebook newsfeed has in the formation of opinions in the real world is so huge that it potentially affected the 2016 election decisions, however these newsfeed were not completely accurate. Our solution? FiB because with 1.5 Billion Users, Every Single Tweak in an Algorithm Can Make a Change, and we don't stop at just one.

## Installation
#### The easy way
Go to the [chrome web store](https://chrome.google.com/webstore/detail/project-fib/njfkbbdphllgkbdomopoiibhdkkohnbf "Chrome Web Store") and add our extension to your browser
#### The harder way
##### (For those who want the latest features)
1. Download "extension" folder from our repository
2. Then go to your extensions page, check the box 'Developer Mode'
3. Click "Load unpacked extension..."
4. Find the extension where you downloaded it and select it
5. The extension should be added now

###### Backend Server Docker Container
To build the backend python server locally to use with the extension, this repository includes [backend/Dockerfile](backend/Dockerfile).

Build the Docker image
```
cd backend/
docker build -t hackprincetonf16 .
```

Run the Docker container locally on port 5000
```
docker run -it --rm -p 5000:5000 hackprincetonf16
```

Update `var server` in [extension/myScript.js](extension/myScript.js) to `http://localhost:5000` before installing the extension manually.

## About us
This project is still under development (a lot of work is required and is also being put in). All of us are Univeristy students trying to help solve a problem social media faces. As university we may sometimes take a while to fix issues or approve pull request, please bear with us. We are always on the lookout for sponsors for this project as we are non-profit and need money to run our servers and cover our API costs.

## Contributing to this project
We love contributors. We are open source and every contribution helps. Please read [CONTRIBUTE.md](CONTRIBUTE.md) for how to contribute to our project.

## Licensing
This project is protected under Open Software License 3.0

Please read [License.md](License.md)
