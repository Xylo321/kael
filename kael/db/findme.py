from kael.db import MySQLBase


class JiaoYuJingLi(MySQLBase):
    """
    教育经历
    """
    def add_jiaoyujingli(self, user_id, resume_id, school_name, ruxue_time, biye_time,
                         zhuanye_name, description):
        """
        增加教育经历

        :param user_id 用户id
        :param resume_id 简历id
        :param school_name 学校名字
        :param ruxue_time 入学时间
        :param biye_time 毕业时间
        :param zhuanye 专业名称
        :param description 描述
        """
        pass


class GongZuoJingLi(MySQLBase):
    """
    工作经历
    """
    def add_gongzuojingli(self, user_id, resume_id, company_name, rugongsi_time, ligongsi_time,
                          job, description):
        """
        增加工作经历

        :param user_id
        :param resume_id
        :param company_name 公司名字
        :param rugongsi_time 进入公司时间
        :param ligongsi_time 离开公司时间
        :param job 职位名称
        :param description 描述
        """
        pass


class Resume(MySQLBase):
    """
    简历
    """
    def add_resume(self, user_id, title, name, age, tel, _email, xueli,
                   jiaoYuJingLis, gongZuoJingLis, gerenpingjia, qiuzhiyixiang):
        """
        增加简历

        :param user_id 用户id
        :param title 简历标题
        :param name 姓名
        :param age 年龄
        :param tel 电话
        :param _email 邮箱
        :param xueli 学历
        :param jiaoYuJingLis 教育经历数组
        :param gongZuoJingLis 工作经历数组
        :param gerenpingjia 个人评价
        :param qiuzhiyixiang 求职意向
        """
        pass


class Job(MySQLBase):
    """
    职位
    """
    def add_job(self, user_id, title, zhiwei_yaoqius, xueli, age_qujian, sex, xinzhi, other_daiyus, company_name):
        """
        增加职位

        :param user_id 用户id
        :param title 职位名称
        :param zhiwei_yaoqius 职位要求数组
        :param xueli 学历
        :param age_qujian 年龄区间 [18, 30]
        :param sex 性别 1：男，2：女，3：男女
        :param xinzhi 薪资
        :param other_daiyus 其它待遇数组
        :param company_name 公司名称
        """
        pass