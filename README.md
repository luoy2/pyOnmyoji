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
pip install -r requriments.txt
```

#### a few notes：
1. change your path of Onmyoji while constructing `Game` class;
2. if `findimg` function not work, try to take sceen shot by your own and save it to `res` folder. Edit the variable name in `img` folder
3. good luck with everything, don't get greedy in case of getting banned!


