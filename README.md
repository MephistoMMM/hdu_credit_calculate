# hdu_credit_calculate
A simple calculator for calculating hdu credits.

### introduction

hdu\_credit\_calculate(hcc) 能够根据你在 **courses_categories.data** 中制定的分类规则，和你记录在 **credit.data** 中的课程成绩数据，自动帮你计算出你一共修的学分数，并与 **courses_categories.data** 中定义的各类需要修的学分数与总共需要修的学分数作比较。

result example: 

![result](http://7xtgln.com1.z0.glb.clouddn.com/result.png)

### Usage

* 根据你的培养计划文档中的信息，将课程分类信息写进 **courses_categories.data** 文档
* 进入`数字杭电`->`选课系统`->`成绩查询`, 复制各个学期的成绩表单到 **credit.data** 文档（也可以去`数字杭电`->`选课系统`->`信息查询`->`学生选课情况查询`中复制数据）
* 根据样本排版（建议先将成绩或选课列表复制到excel或numbers，删除多余列，增加修改必要列后，再将结果赋值到 **credit.data** 文档）
* `./calculate.py`

课外选修项目或一些难以在 选课系统 得到的项目，可以根据 **credit.data** 中的格式手动写上去。

for example:

    2015-2016	2	W0001050	社会实践	                    课外选修	 	1.0
    
*ps1: credit.data 中的课程数据寻找与其相匹配的类时，按照 courses_categories.data 中类定义的顺序进行的（从上至下）。*

*ps2: 如果某一项课程数据的要添加到与其相匹配的第一个类中，但是该类的总分已经到达 courses_categories.data 中设定的最大值，则hcc会尝试该项课程数据添加到下一个与其相匹配的类中，以此类推。*

*ps3: 现在，不及格的成绩就不要写在 credit.data 中。*

### TODO

* 友好的错误 数据格式错误 提示
* 自己指定读取的数据文件名

### License

MIT
