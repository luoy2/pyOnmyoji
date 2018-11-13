# pyOnmyoji
python play onmyoji(网易-阴阳师), folked win32 controller from SerpentAI

The initial purpose of this project is trying to train a RNN to play Onmyoji as a data science project. (Special thanks to [SerpentAI](https://github.com/SerpentAI/SerpentAI) providing the framework)

While working on the model constructing, I will try to move some features from my [Lua Bot](https://github.com/luoy2/yys_lua_script) to this python project.

#### python env:

| python version        | availability |
| ------------- |:-------------:|
|python 3.6| available |
|< python 3.5 | untested     |
|python 2.x| unavailable |


#### install
```
pip install -r requirements.txt
```



#### a few notes：
1. all the color cords were taken on a **4k monitor(win ui zoom 150%)**, so if you are on a different resolution and zoom percentage, you probably need to re take all the color cords. I will upload a tutorial and a PyQt tool about taking the color cords sometime later. Basically, all the colors were in `colors/util.py` and the structure would be:

```
LiaoAttack = ColorToMatch([537, 169, 1459, 963], [[(0, 0), (243, 178, 94)], [(33, -37), (150, 59, 46)], [(-331, -3), (243, 178, 94)]], 1)
```

  - first list `[537, 169, 1459, 963]` is the region of the color tuples you want to find
  - second list were the color tuples. the first cords will always be `[0, 0]`, which means you need to find a RGB color (e.g. (243, 178, 94), and the (33, -37) offset color should be (150, 59, 46), going forward.
  - third value is the tolerence value for find colors
 
 
 
 #### Tansuo
1. 进入方法：进入探索界面， 运行`tansuo.py`. 若不需要寮突破， 请将`liao_status` 设为0. 否则会优先去打寮突破-> 个人突破 -> 探索。
  ```
  if __name__ == '__main__':
    liao_status = 1
  ```
2. 探索目前的机制是狗粮大队长默认处于左1号位， 然后会在寮突破， 探索， 个人突破中循环。 探索会自动打最后一章的经验怪以及boss。
  
  
 #### 结界突破
 1. 锁定突破阵容后， 进入结界突破寮突破界面， 运行`jiejietupo.py`
 
 #### 御魂队长模式
 1. 选好阵容， 找好基友， 锁定出战阵容
 2. 在小队等待界面运行`party.py`
 
 #### 御魂队员模式
 1. 同上
 2. 在任意界面运行`party_member.py`
 
 
 #### 业原火
 1. 锁定出战阵容
 2. 在开始之前的界面运行`yeyuanhuo.py`. 目前只支持痴
 
 
 
