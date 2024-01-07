### 使用SQLAlchemy如何进行数据库迁移

- `使用Alembic`

  Alembic简介：SQLAlchemy是一款非常优秀的ORM框架，但是本身没有带数据库版本控制功能，这很不方便，进行开发过程中难免修改数据模型，添加一个表，修改一个字段，都需要手动修改的话就比较费事了，还不如不用SQLAlchemy呢。

  在这里介绍一款SQLAlchemy作者写的数据库版本控制工具---Alembic。另外还有一个工具叫做SQLAlchemy-Migrate，在使用过程中感觉Alembic更为灵活。

  ##  

  ## 安装alembic

  ```
  $ pip3 install alembic
  ```

  ## 初始化

  使用之前，先在项目根目录进行初始化。

  ```
  $ alembic init alembic
  ```

  初始化完成后，会生成一个alembic.ini配置文件及一个alembic目录。

## 创建模型类

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
#!/usr/bin/env python                       
# -*- coding:utf-8 -*-                      
# File Name    : sb.py                      
# Author       : hexm                       
# Mail         : xiaoming.unix@gmail.com    
# Created Time : 2017-03-29 20:03           

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# 用户id对应角色id 多对多
useridToRoleid = Table('useridToRoleid', Base.metadata,
        Column('userid', Integer, ForeignKey('users.id')),
        Column('roleid', Integer, ForeignKey('roles.id')),
    )

# 角色id对应权限id 多对多
roleidToIdentityid = Table('roleidToIdentityid', Base.metadata,
        Column('roleid', Integer, ForeignKey('roles.id')),
        Column('identityid', Integer, ForeignKey('identities.id')),
    )

# 文章id和标签id 多对多
articleidToTagid = Table('articleidToTagid', Base.metadata,
        Column('articleid', Integer, ForeignKey('articles.id')),
        Column('tagid', Integer, ForeignKey('tags.id')),
    )

class User(Base):
    """
    用户表
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False, unique=True)

    roles = relationship('Role', secondary=useridToRoleid, backref='users')

    def __repr__(self):
        return "<%s users.username: %s>" % (self.id, self.username)

class Role(Base):
    """
    角色表
    """
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)

    identity = relationship('Identity', secondary=roleidToIdentityid, backref='roles')

    def __repr__(self):
        return "<%s roles.name: %s>" % (self.id, self.name)

class Identity(Base):
    """
    权限表
    """
    __tablename__ = 'identities'
    id = Column(Integer, primary_key=True)
    name = Column(String(16))

    def __repr__(self):
        return "<%s identities.name: %s>" % (self.id, self.name)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)

    title = relationship('Article', backref='category')

    def __repr__(self):
        return "<%s categories.name: %s" % (self.id, self.name)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(16))

    def __repr__(self):
        return "<%s categories.name: %s" % (self.id, self.name)

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(300))
    content = Column(Text)
    click_count = Column(Integer, default=0)

    category_id = Column(Integer, ForeignKey('categories.id'))
    tags = relationship('Tag', secondary=articleidToTagid, backref='articles')

    def __repr__(self):
        return "<%s categories.name: %s" % (self.id, self.title)
```

## 修改配置文件

修改alembic.ini配置文件，只修改数据库连接部分即可，

将

```
sqlalchemy.url = driver://user:pass@localhost:port/dbname
```

修改为

```
sqlalchemy.url = mysql+pymysql://root:@localhost/linux_study
```

修改alembic/env.py

将

```
target_metadata = None
```

修改为

```
import sys                                             
from os.path import abspath, dirname                   
sys.path.append(dirname(dirname(abspath(__file__))))   
from modules.models import Base                        
target_metadata = Base.metadata            
```

## 自动创建版本

使用alembic revision -m "注释" 创建数据库版本，上面我们修改了配置文件alembic/env.py，指定了target_metadata，这里可以使用--autogenerate参数自动生成迁移脚本。

```
$ alembic revision --autogenerate -m "initdb"
```

### 将迁移文件映射到数据库中

$ `alembic upgrade head`

## 其他常用参数

**更新数据库**

```
$ alembic upgrade 版本号
```

**更新到最新版**

```
alembic upgrade head
```

**降级数据库**

```
$ alembic downgrade 版本号
```

**更新到最初版**

```
alembic downgrade head
```

**离线更新（生成sql）**

```
alembic upgrade 版本号 --sql > migration.sql
```

**从特定起始版本生成sql**

```
alembic upgrade 版本一:版本二 --sql > migration.sql
```

**查询当前数据库版本号**

查看alembic_version表。

**清除所有版本**

将versions删掉，并删除alembic_version表