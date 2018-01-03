## 配置文件说明 ##

- db.ini -- 数据库配置， session配置

    ```
    [db]
    host=127.0.0.1
    port=3306
    user=root
    pass=root

    [session]
    host=127.0.0.1
    port=6379
    session=10

    [cache]
    host=127.0.0.1
    port=6379

    [rabbitmq]
    user = guest
    pass = guest
    host = 127.0.0.1
    port = 5672

    ```

- env.ini -- 环境基本配置
    1. 线上配置
    debug=False;
    env=online
    ```
    [common]
    debug=True
    env=develop
    ;develop/online/release
    ```

