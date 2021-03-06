# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime, \
    DECIMAL

# print(sys.path)
from website.run import create_app
from flask_sqlalchemy import SQLAlchemy

app = create_app()
db = SQLAlchemy(app)


# 用户基础表(游客/房东公共部分)
class UserBase(db.Model):

    __tablename__ = 'userbase'

    user_id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    user_account = Column('user_account', String(45), index=True, nullable=False)
    user_password = Column('user_password', String(45), nullable=False)
    user_mobile = Column('user_mobile', String(45), nullable=False)
    user_headimg = Column('user_headimg', String(100))
    user_type = Column('user_type', Integer, nullable=False)  # 0房东，1游客

    user_createtime = Column('user_createtime', DateTime, default=datetime.datetime.now)
    user_modifytime = Column('user_modifytime', DateTime, default=datetime.datetime.now)

    houseowner = db.relationship('HouseOwner', backref='userbase', lazy='dynamic')


    def to_json(self):
        return {
            'user_id': self.user_id,
            'user_account': self.user_account,
            'user_mobile': self.user_mobile,
            'user_headimg': self.user_headimg,
            'user_type': self.user_type
        }

# 房东表(用户扩展表,若想成为房东就需要提供更多资料)
class HouseOwner(db.Model):

    __tablename__ = 'houseowner'

    ho_id = Column('ho_id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', Integer, ForeignKey('userbase.user_id'))   # 外键
    ho_name = Column('ho_name', String(45), index=True, nullable=False)   # 真实姓名
    ho_tel = Column('ho_tel', String(45))    # 家庭电话
    ho_email = Column('ho_email', String(45))   # 邮箱
    ho_nicard = Column('ho_nicard', String(100), nullable=False)    # 身份证件照

    ho_createtime = Column('ho_createtime', DateTime, default=datetime.datetime.now)
    ho_modifytime = Column('ho_modifytime', DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {
            'ho_id': self.ho_id,
            'user_id':self.user_id,
            'ho_name': self.ho_name,
            'ho_tel': self.ho_tel,
            'ho_email': self.ho_email,
            'ho_nicard': self.ho_nicard
        }

# 游客扩展表(以后可能需要预约登记之类的),就可以加扩展表,登记更多用户资料
# class Visitor(db.Model):
#     __tablename__ = 'visitor'
#
#     vi_id = Column('vi_id', Integer, primary_key=True, autoincrement=True)
#     user_id = Column('user_id', Integer, ForeignKey('userbase.user_id'))   # 外键


#  房源类型表
class HouseType(db.Model):

    __tablename__ = "housetype"

    ty_id = Column('ty_id', Integer, primary_key=True)
    ty_name = Column('ty_name', String(45), nullable=False)
    ty_valume =Column('ty_valume', Integer, default=0)

    houseresources = db.relationship('HouseResources', backref='housetype', lazy='dynamic')

    def to_json(self):
        house_type = {
            'ty_id': self.ty_id,
            'ty_name': self.ty_name,
            'ty_valume': self.ty_valume
        }
        return house_type

# 房源表
class HouseResources(db.Model):

    __tablename__ = "houseresources"

    hs_id = Column('hs_id', Integer, primary_key=True)
    ty_id = Column('ty_id', Integer, ForeignKey('housetype.ty_id'))
    user_id = Column('user_id', Integer, ForeignKey('userbase.user_id', ondelete='CASCADE'))
    hs_name = Column('hs_name', String(20))   # 房源名称
    hs_intro = Column('hs_intro', String(500))
    hs_province = Column('hs_province', String(20))
    hs_city = Column('hs_city', String(20))
    hs_country = Column('hs_country', String(20))
    hs_address = Column('hs_address', String(50))
    hs_hitvalume = Column('hs_hitvalume', Integer)    # 点击量
    hs_images = Column('hs_images', String(500))
    hs_status = Column('hs_status',Integer)  #  房源状态, 0 表示暂停营业,1 表示正常营业
    hs_createtime = Column('hs_createtime', DateTime, default=datetime.datetime.now())
    hs_modifytime = Column('hs_modifytime', DateTime, default=datetime.datetime.now())

    def to_json(self):
        return {
            'hs_id': self.hs_id,
            'ty_id': self.ty_id,
            'user_id': self.user_id,
            'hs_name':self.hs_name,
            'hs_province': self.hs_province,
            'hs_city': self.hs_city,
            'hs_country': self.hs_country,
            'hs_address': self.hs_address,
            'hs_hitvalume':self.hs_hitvalume,
            'hs_images': self.hs_images,
            'hs_status':self.hs_status,
            'hs_intro':self.hs_intro
        }

# 客房类型表
# class RoomType(db.Model):
#
#     __tablename__ = "roomtype"
#
#     rt_id = Column('rt_id', Integer, primary_key=True)
#     rt_name = Column('rt_name', String(50), nullable=False)



class GuestRoom(db.Model):

    __tablename__ = "guestroom"

    gr_id = Column('gr_id', Integer, primary_key=True)
    hs_id = Column('hs_id', Integer, ForeignKey('houseresources.hs_id', ondelete='CASCADE'))

    gr_name = Column('gr_name', String(100))    # 客房名称
    gr_price = Column('gr_price', DECIMAL(10, 2))
    gr_desc = Column('gr_desc', String(500))   # 简单描述:如几张床,是否有独立卫浴等;
    gr_images = Column('gr_images', String(500))

    gr_createtime = Column('gr_createtime',DateTime,default=datetime.datetime.now())
    gr_modifytime = Column('gr_modifytiem',DateTime,default=datetime.datetime.now())

    def to_json(self):
        return {
            'gr_id': self.gr_id,
            'hs_id': self.hs_id,
            'gr_name':self.gr_name,
            'gr_price': self.gr_price,
            'gr_describe': self.gr_describe,
            'gr_images':self.gr_images
        }


# if __name__ == '__main__':
#     db.create_all()
#     manager.run()


#http://www.cnblogs.com/yueerwanwan0204/p/5327912.html