# auto_sign
 今日校园云函数批量签到脚本



# 项目说明

1. 本项目仅供学习交流，请勿用作商业用途，否则后果自负；
2. 脚本仅适用于海南大学每日签到，其他情况请自行修改测试；
3. 建议使用云函数定时运行脚本，推荐腾讯云/阿里云；
4. 项目途经多位大佬之手，代码水平有限，如无重大情况不更新；



# 使用方法

## 本地运行

环境：python3

依赖：requests、pyDes、base64等依赖包（根据报错提示安装即可）

1. 安装所需环境，在user_password.txt添加学号密码，请严格按照格式【学号----密码】每行添加一个；
2. 主函数在index.py里面，直接运行check_in_all函数即可；



## 云函数运行

1. 登录阿里云，在控制台找到【函数计算】服务并进入；
2. 在【服务/函数】功能中点击新建服务，名称随意填，点击创建即完成；
3. 在【服务/函数】功能中点击新建函数，选择第一个事件函数，选中python3即可，其他随意；

![image-20201207002021611](https://images.at0de.com/images/2020/12/06/image-20201207002021611.png)

4. 跳转到代码执行，通过代码包或文件夹上传所有文件，点击保存；
5. 在user_password.txt中添加学号密码，请严格按照格式【学号----密码】每行添加一个；
6. 函数入口是index.handler代表默认运行index文件的handler函数，保存并运行即可；

7. 如需server酱通知可自行配置；



## 关于报错

函数正常运行即表示成功，如报错请检查你的学号密码输入是否正确，格式是否正确；



# 项目贡献

xxx