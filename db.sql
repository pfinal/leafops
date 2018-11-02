
DROP DATABASE IF EXISTS deploy_py;
CREATE DATABASE IF NOT EXISTS deploy_py;
USE deploy_py;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL DEFAULT '' COMMENT '账号',
  `password` varchar(50) NOT NULL DEFAULT '密码',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '新增时间',
  PRIMARY KEY (`id`),
  KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8 COMMENT='用户';


DROP TABLE IF EXISTS token;
CREATE TABLE IF NOT EXISTS `token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` CHAR(32) NOT NULL COMMENT 'Token',
  `user_id` INT NOT NULL COMMENT 'UserId',
   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '新增时间',
   PRIMARY KEY (`id`),
   UNIQUE(`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Token';

DROP TABLE IF EXISTS machine;
CREATE TABLE `machine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL DEFAULT '' COMMENT '名称',
  `ip` varchar(50) NOT NULL DEFAULT '' COMMENT 'IP地址',
  `user` varchar(50) NOT NULL DEFAULT '' COMMENT '用户',
  `password` varchar(50) NOT NULL DEFAULT '' COMMENT '密码',
  `hardware` varchar(255) NOT NULL DEFAULT '' COMMENT '硬件配置',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '新增时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8 COMMENT='主机';

DROP TABLE IF EXISTS monitor;
CREATE TABLE `monitor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `machine_id` int(11) NOT NULL,
  `cpu` varchar(255) NOT NULL DEFAULT '',
  `memory` varchar(255) NOT NULL DEFAULT '',
  `disk` varchar(255) NOT NULL DEFAULT '',
  `net` varchar(255) NOT NULL DEFAULT '',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '新增时间',
  PRIMARY KEY (`id`),
  KEY(machine_id)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8 COMMENT='监控';



DROP TABLE IF EXISTS project;
CREATE TABLE `project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '项目名称',
  `repository` varchar(255) NOT NULL DEFAULT '' COMMENT '代码仓库',
  `machine_ids` varchar(255) NOT NULL DEFAULT '' COMMENT '发布主机 eg. [1,2,3]',
  `directory` varchar(255) NOT NULL DEFAULT '' COMMENT '发布目录',
  `pre_deploy` text COMMENT '前置任务',
  `post_release` text COMMENT '后置任务',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '新增时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8 COMMENT='项目';


DROP TABLE IF EXISTS task;
CREATE TABLE `task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL DEFAULT '0',
  `branch` varchar(255) NOT NULL,
  `version` varchar(255) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '1',
  `user_id` int(11) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '新增时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8 COMMENT='发布';


insert into user (username,password) values ('root',md5('root'));
insert into user (username,password) values ('dev',md5('dev'));

