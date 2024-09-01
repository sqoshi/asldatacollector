// Start camera and capture image
document.getElementById("capture-btn").onclick = function() {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");

    // Draw video frame to canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas image to a data URL (base64 string)
    const imageData = canvas.toDataURL("image/jpeg");

    // Send the image to the server for processing
    fetch('/collect/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("capture-status").textContent = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

// Initialize camera stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        const video = document.getElementById("camera");
        video.srcObject = stream;
    })
    .catch(error => {
        console.error('Error accessing the camera', error);
    });
