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

        # 画出左上、左下、右上、右下点
        L1 = (blob.cx() - blob.w()//2, blob.cy() - blob.h()//2)
        L2 = (blob.cx() - blob.w()//2, blob.cy() + blob.h()//2)
        R1 = (blob.cx() + blob.w()//2, blob.cy() - blob.h()//2)
        R2 = (blob.cx() + blob.w()//2, blob.cy() + blob.h()//2)

        img.draw_circle(L1[0], L1[1], 5, color=(0, 255, 0))  # 左上点
        img.draw_circle(L2[0], L2[1], 5, color=(0, 255, 0))  # 左下点
        img.draw_circle(R1[0], R1[1], 5, color=(0, 255, 0))  # 右上点
        img.draw_circle(R2[0], R2[1], 5, color=(0, 255, 0))  # 右下点

    # 寻找红色目标并标记
    red_blobs = img.find_blobs([red_threshold], pixels_threshold=200, area_threshold=200)
    red_blobs.sort(key=lambda b: b.pixels(), reverse=True)
    for i in range(min(2, len(red_blobs))):
        blob = red_blobs[i]
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy(), color=(255, 0, 0))

        # 画出左上、左下、右上、右下点
        L1 = (blob.cx() - blob.w()//2, blob.cy() - blob.h()//2)
        L2 = (blob.cx() - blob.w()//2, blob.cy() + blob.h()//2)
        R1 = (blob.cx() + blob.w()//2, blob.cy() - blob.h()//2)
        R2 = (blob.cx() + blob.w()//2, blob.cy() + blob.h()//2)

        img.draw_circle(L1[0], L1[1], 5, color=(0, 255, 0))  # 左上点
        img.draw_circle(L2[0], L2[1], 5, color=(0, 255, 0))  # 左下点
        img.draw_circle(R1[0], R1[1], 5, color=(0, 255, 0))  # 右上点
        img.draw_circle(R2[0], R2[1], 5, color=(0, 255, 0))  # 右下点

        # 确保 "R1" 和 "R2" 的横坐标值大于 "L1" 和 "L2"
        if R1[0] <= L1[0] or R2[0] <= L2[0]:
            print("Error: Right points should have greater x-coordinate values than left points.")
