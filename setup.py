import io

from setuptools import setup
from setuptools import find_packages
# 获取readme.md文件
with io.open("README.md", "r", encoding="utf8") as f:
    readme = f.read()

setup(
    # 包的名称，pip install db-mysql, 和文件夹的名称要一样，不然安装和使用时会头疼
    name='db-mysql',
    version='0.1.0',
    # 暂时和包名一样
    py_modules=['db-mysql'],
    # 作者信息
    author="WRAllen",
    author_email="1072274105@qq.com",
    description="一个基于pymysql的操作mysql的简易框架",
    # 用readme文件来填充pypi页面上的具体介绍
    long_description=readme,
    long_description_content_type='text/markdown',
    # 这个很重要，如果包里面有多个文件，并且直接有所关联一定要把路径确定了
    packages=find_packages("src"),
    package_dir={"": "src"},
    # github地址，Pypi页面上HomePage按钮的链接
    url='https://github.com/WRAllen/db-mysql'
)
