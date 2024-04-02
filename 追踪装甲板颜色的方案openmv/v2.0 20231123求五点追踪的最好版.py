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

clock = time.clock()

while True:
    clock.tick()  # 开始计时

    img = sensor.snapshot()  # 获取图像

    # 寻找蓝色目标并标记
    blue_blobs = img.find_blobs([blue_threshold], pixels_threshold=200, area_threshold=200)
    blue_blobs.sort(key=lambda b: b.cx())
    if len(blue_blobs) >= 2:
        L1 = (blue_blobs[0].cx(), blue_blobs[0].cy() - blue_blobs[0].h()//2)
        L2 = (blue_blobs[0].cx(), blue_blobs[0].cy() + blue_blobs[0].h()//2)
        R1 = (blue_blobs[1].cx(), blue_blobs[1].cy() - blue_blobs[1].h()//2)
        R2 = (blue_blobs[1].cx(), blue_blobs[1].cy() + blue_blobs[1].h()//2)

        # 如果需要，交换位置
        if R1[0] < L1[0]:
            L1, R1 = R1, L1
            L2, R2 = R2, L2

        # 画出点的圆圈
        img.draw_circle(L1[0], L1[1], 5, color=(0, 255, 0))  # 左上点
        img.draw_circle(L2[0], L2[1], 5, color=(0, 255, 0))  # 左下点
        img.draw_circle(R1[0], R1[1], 5, color=(0, 255, 0))  # 右上点
        img.draw_circle(R2[0], R2[1], 5, color=(0, 255, 0))  # 右下点

        # 在图像上显示标签
        img.draw_string(L1[0], L1[1], "L1", color=(255, 255, 255), mono_space=False)
        img.draw_string(L2[0], L2[1], "L2", color=(255, 255, 255), mono_space=False)
        img.draw_string(R1[0], R1[1], "R1", color=(255, 255, 255), mono_space=False)
        img.draw_string(R2[0], R2[1], "R2", color=(255, 255, 255), mono_space=False)

        # 连接线段并标注交点
        img.draw_line(L1[0], L1[1], R2[0], R2[1], color=(255, 0, 0))  # 连接L1和R2的线段
        img.draw_line(L2[0], L2[1], R1[0], R1[1], color=(255, 0, 0))  # 连接L2和R1的线段
        intersection_point = ((L1[0] + R2[0]) // 2, (L1[1] + R2[1]) // 2)  # 两线段的中点即为交点
        img.draw_string(intersection_point[0], intersection_point[1], f"Intersection: {intersection_point}", color=(255, 255, 255), mono_space=False)

    # 寻找红色目标并标记
    red_blobs = img.find_blobs([red_threshold], pixels_threshold=200, area_threshold=200)
    red_blobs.sort(key=lambda b: b.cx())
    if len(red_blobs) >= 2:
        L1 = (red_blobs[0].cx(), red_blobs[0].cy() - red_blobs[0].h()//2)
        L2 = (red_blobs[0].cx(), red_blobs[0].cy() + red_blobs[0].h()//2)
        R1 = (red_blobs[1].cx(), red_blobs[1].cy() - red_blobs[1].h()//2)
        R2 = (red_blobs[1].cx(), red_blobs[1].cy() + red_blobs[1].h()//2)

        # 如果需要，交换位置
        if R1[0] < L1[0]:
            L1, R1 = R1, L1
            L2, R2 = R2, L2

        # 画出点的圆圈
        img.draw_circle(L1[0], L1[1], 5, color=(0, 255, 0))  # 左上点
        img.draw_circle(L2[0], L2[1], 5, color=(0, 255, 0))  # 左下点
        img.draw_circle(R1[0], R1[1], 5, color=(0, 255, 0))  # 右上点
        img.draw_circle(R2[0], R2[1], 5, color=(0, 255, 0))  # 右下点

        # 在图像上显示标签
        img.draw_string(L1[0], L1[1], "L1", color=(255, 255, 255), mono_space=False)
        img.draw_string(L2[0], L2[1], "L2", color=(255, 255, 255), mono_space=False)
        img.draw_string(R1[0], R1[1], "R1", color=(255, 255, 255), mono_space=False)
        img.draw_string(R2[0], R2[1], "R2", color=(255, 255, 255), mono_space=False)

        # 连接线段并标注交点
        img.draw_line(L1[0], L1[1], R2[0], R2[1], color=(255, 0, 0))  # 连接L1和R2的线段
        img.draw_line(L2[0], L2[1], R1[0], R1[1], color=(255, 0, 0))  # 连接L2和R1的线段
        intersection_point = ((L1[0] + R2[0]) // 2, (L1[1] + R2[1]) // 2)  # 两线段的中点即为交点
        img.draw_string(intersection_point[0], intersection_point[1], f"Intersection: {intersection_point}", color=(255, 255, 255), mono_space=False)

    # 显示帧率
    img.draw_string(5, 5, "FPS: " + str(clock.fps()), color=(255, 255, 255), mono_space=False)
