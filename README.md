# comfyui-dependency-checker

由于使用ComfyUI，不断的安装不同的插件，导致很多开源插件依赖冲突，所以想做一个简单的检测工具，同时也可以安装插件节点和依赖的小工具

=== ComfyUI 插件依赖冲突检测报告 === 混沌云制作 === 2025.6.27

=== 需要定制LORA可以联系我 === 微信 : chaosdoor

=== https://www.liblib.art/userpage/52322c5d27404cd28aea54b9641d5451/publish

=== 专注于电商落地服务 ===


使用方法：
-----------------------------------------------------------------
下载文件  comfyui_dependency_checker.py  run_checker.bat  
-----------------------------------------------------------------
两个文件复制到  D:\XXX\XX\ComfyUI   ComfyUI的根目录就可以
-----------------------------------------------------------------
运行方式 点击 run_checker.bat  
-----------------------------------------------------------------
![图片描述](https://github.com/chaoscloudcn/comfyui-dependency-checker/blob/main/20250630173445.png?raw=true)
![图片描述](https://github.com/chaoscloudcn/comfyui-dependency-checker/blob/main/20250630175059.png?raw=true)

检测已安装所有插件的需要的依赖文件
获取所有插件里面的 requirements.txt 

比对所有依赖的版本 ，
1 那些有冲突 冲突的插件名称 需要的依赖版本 
2 那些未安装
3 分析总结
4 然后安装
5 选择0全部安装
6 安装失败自动跳过安装下一个

需要自己开启科学上网




