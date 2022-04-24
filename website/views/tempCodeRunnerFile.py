return Response(gen(VideoCamera),
    #                 mimetype='multipart/x-mixed-replace; boundary=frame')