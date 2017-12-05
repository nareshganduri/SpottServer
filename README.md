# SpottServer
A simple Flask backend for the [Spott](https://github.com/seb314/Spot) app

## Uses
The server exposes a simple API.

### Uploading Images
To upload images, send a POST request to _/upload_

The POST request should be encoded as "multipart/form-data" and should specify the following parameters:
* src - The binary image data itself
* date - An ASCII string specifying the file name
* location - An ASCII string ('0' - 2') specifying the floor location

On success, a plain ASCII string will be returned, reading 'SUCCESS'

### Downloading Images
To download images, send a POST request to _/download_

The POST request uses the default encoding and should specify the following parameters:
* location - An ASCII string ('0' - '3') specifying the floor location
  * If location is '3', then all images in the database will be returned

On success, the image data will be sent as a JSON object.

More specifically, the result will look like this:

\[{"data":"img1_blahblah", "date":"4:04 PM"}, {"data":"img2_blahblah", "date":"2:01 AM"}, ... \]

Each image returned has two parameters:
* data - The image binary data itself, encoded as a base64 string
* date - An ASCII string representing the time the picture was uploaded to the server

The server is up now. Try it out at http://spott-server.herokuapp.com/
