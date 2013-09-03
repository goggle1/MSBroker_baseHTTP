1，满足自动加载module文件夹下面的任意深度模块，如：/ms/example_0    /ms/ms_1/example_1

2，注意：每一层级文件夹下面必须有__init__.py

4，注意：模块名与类名一致

3，注意：当前工作目录与“MSBroker.py”同层。有时需要用到模块所在的目录，例如os.path.dirname(__file__)+"/examplelog.log"，保证日志在模块所在的文件夹目录下

5，注意：模块输入为input_dic，其key值是list型（以保证同一键可对应多值）

6，注意：模块输出为（result_flag,result_string），result_flag=0表示模块运行成功，result_string为返回客户端的字符串

7，MSBroker.py下有框架日志msbrokerlog.log；模块中有模块日志“examplelog.log”。

7，访问格式：ip:port/模块路径?参数1=值1&参数2=值2

例如：“http://ip:11000/ms/example_0?a=1&a=2&b=1”     “http://ip:11000/ms/ms_1/example_1?a=1&a=2&b=1”