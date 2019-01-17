#Camera control - By:Simon  - 1.17 2019
'''
2017国赛飞行器摄像头代码
实现功能：
1.当启动时，仅有初始场地上的圆时，锁定场地上的圆。
2.当检测到小车的圆时，锁定小车。
'''
import sensor,image,time
from pyb import UART,LED
#判断是否检测到小车，若检测到，则锁定小车，若没有则锁定场地圆
def find_car(circles):
    global front_circle,current_circle,g_mode
    i=0
    current_circle.x=200
    current_circle.y=200
    #锁定场地圆
    for c in circles:
        i+=1
        current_circle.x=c.x()
        current_circle.y=c.y()
        current_circle.r=c.r()

    #如果有两个圆，认为y值小的为小车
    if i>=2:
        current_circle.y=200
        for c in circles:
           if abs(front_circle.y-c.y())>abs(front_circle.y-current_circle.y):
            current_circle.x=c.x()
            current_circle.y=c.y()
            current_circle.r=c.r()
        g_mode=1
        print('找到小车,开始锁定小车......')

    if i!=0:
        front_circle.x=current_circle.x
        front_circle.y=current_circle.y
        front_circle.r=current_circle.r
    else:
        front_circle.x=0
        front_circle.y=0

#锁定小车
def lock_car(circles):
    global front_circle,current_circle
    current_circle.x=500
    current_circle.y=500
    for c in circles:
        if abs(c.x()-front_circle.x)**2+abs(c.y()-front_circle.y)**2<abs(current_circle.x-front_circle.x)**2+abs(current_circle.y-front_circle.y)**2:
            current_circle.x=c.x()
            current_circle.y=c.y()
            current_circle.r=c.r()
    front_circle.x=current_circle.x
    front_circle.y=current_circle.y
    front_circle.r=current_circle.r

#打包数据
def pack_data():
    img.draw_circle(current_circle.x,current_circle.y,current_circle.r,color=(255,0,0))

class CIRCLE(object):
    x=0
    y=0
    r=0

g_mode=0        #0模式时，为锁定场地上的圆
front_circle=CIRCLE()
current_circle=CIRCLE()
#摄像头传感器设置
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)     #QQQVG:80*60
sensor.skip_frames(time=2000)           #略过前两秒的数据
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock=time.clock()

while True:
    clock.tick()
    #修正镜头畸变
    img=sensor.snapshot()
    c=img.find_circles(threshold=4000,x_margin=10,y_margin=10,r_margin=10)
    if c:
        if g_mode==0:
            find_car(c)
            pack_data()
        elif g_mode==1:
            lock_car(c)
            pack_data()
    print(clock.fps())
