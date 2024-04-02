import sensor, image, time

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # 需要关闭自动增益
sensor.set_auto_whitebal(False)  # 需要关闭自动白平衡

# 定义颜色阈值（蓝色和红色）
blue_threshold = (0, 80, 0, 50, -80, -20)
red_threshold = (50, 80, 50, 127, -10, 127)

while True:
    img = sensor.snapshot()  # 获取图像

    # 寻找蓝色目标并标记
    blue_blobs = img.find_blobs([blue_threshold], pixels_threshold=200, area_threshold=200)
    blue_blobs.sort(key=lambda b: b.pixels(), reverse=True)
    for i in range(min(2, len(blue_blobs))):
        blob = blue_blobs[i]
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 0, 255))

        # 画出上点和下点
        img.draw_circle(blob.cx(), blob.cy() - blob.h()//2, 5, color=(0, 255, 0))  # 上点
        img.draw_circle(blob.cx(), blob.cy() + blob.h()//2, 5, color=(0, 255, 0))  # 下点

    # 寻找红色目标并标记
    red_blobs = img.find_blobs([red_threshold], pixels_threshold=200, area_threshold=200)
    red_blobs.sort(key=lambda b: b.pixels(), reverse=True)
    for i in range(min(2, len(red_blobs))):
        blob = red_blobs[i]
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy(), color=(255, 0, 0))

        # 画出上点和下点
        img.draw_circle(blob.cx(), blob.cy() - blob.h()//2, 5, color=(0, 255, 0))  # 上点
        img.draw_circle(blob.cx(), blob.cy() + blob.h()//2, 5, color=(0, 255, 0))  # 下点

