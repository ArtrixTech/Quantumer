# Quantumer
Quantumer - An opensource webpage change detecting framework.

# Usage
Execute the Main.py, then login with your WeChat account.

# Commands
To use the Quantumer, you have to control it on the WeChat Platform.As a user, you can add a friend with your service account, and Quantumer will auto accept the friend request.

### Then, use these commands:

- 开始监听

    This command allows user to listen the change of a webpage.
    
    #### Arguments:
    
    - url - The url to check
    - head1 - The first string cut's head argument
    - tail1 - The first string cut's tail argument
    - head1 - The second string cut's head argument
    - tail1 - The second string cut's tail argument
    - interval - The interval of each checking tick
    
    #### Command example:
        开始监听 url=http://bbs.meizu.cn/home.php?mod=space&uid=1304289&do=thread&from=space,head1=a href="thread-6634052-1-1.html" target="_blank" >,tail1=<,interval=10,
    
- 生成命令
  
  This command will generate a command with a guide, to let users use Quantumer in a coveniently way.

- 停止监听
  
  This command will stop your recent listening task.
