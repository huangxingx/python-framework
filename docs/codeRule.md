## 编码规则 ##
* 引包
  1. 引用google的编码规范， 尽量引用模块， 使用from XXX import module
  2.  pycharm 配置 pettyloan/ 为 source root， 自己写的模块引用重 跟路径引用，
  不使用相对路径（特殊情况除外）;
  3.  tornado 所有的库的引用方式为：

        ```python
        import tornado
        from tornado import ioloop
        from tornado import web
        from tornado.options import define
        from tornado.options import options
        from tornado.options import parse_command_line
        ```

* 代码风格
  1. 严格运用 pep8 编码规范;
  2. 尽量减少 pycharm 静态检查的警告，警告数小于10, 不的出现error;
  3. 代码提交之前，使用 pycharm 自带的格式化进行代码的格式化，
        - 代码格式化：Ctrl+Alt+L
        - 引包格式化：Ctrl+Alt+O

## 命名规则 ##
 * models 的定义： 所有的定义以 Model 结尾;
 * services定义： 所有的定义以 Service结尾;
 * handlers定义： 所有的定义以 Handler结尾;
 * models 实例化： 以 m_XXX 开头;
 * services 实例化： 以 s_XXX 开头;

## 日志的使用 ##
 * 由于libs中封装的logger和tornado自带的logger冲突问题暂未解决，故日志使用方法
      ```
      import logging
      ```
    直接用标准库 logging

## 第三方库使用规则 ##
* 如果要使用除框架外的第三方库，必须经的全员同意，不得擅自使用;如经的同意后， 使用之前的
先加到 requirements.txt 文件中，明确下载途径和版本号;
