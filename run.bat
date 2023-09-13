@echo off

REM 摄像头服务 4999
start "4999" cmd /c "cd /d C:\Users\15752\Desktop\GraduationDesign\camera_services && D:\miniconda\envs\flask\python.exe app.py"

REM 启动第一个命令窗口并运行 5000
start "5000" cmd /c "cd /d C:\Users\15752\Desktop\GraduationDesign\web && D:\miniconda\envs\flask\python.exe app.py"

REM 启动第二个命令窗口并运行 5001
start "5001" cmd /c "cd /d C:\Users\15752\Desktop\GraduationDesign\yolo && D:\miniconda\envs\yolo\python.exe detect.py"

REM 启动第三个命令窗口并运行 5002
start "5002" cmd /c "cd /d C:\Users\15752\Desktop\GraduationDesign\deepsort && D:\miniconda\envs\deepsort\python.exe demo.py"

REM 执行完毕后暂停，以便查看输出信息
pause