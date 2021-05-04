CREATE DATABASE /*!32312 IF NOT EXISTS*/ `hss` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `hss`;
DROP TABLE IF EXISTS `subscribers`;
create table subscribers(
   id INT NOT NULL AUTO_INCREMENT,
   imsi VARCHAR(15) NOT NULL,
   opc VARCHAR(32) NOT NULL,
   k VARCHAR(32) NOT NULL,
   amf VARCHAR(4) NOT NULL,
   sqn VARCHAR(4) NOT NULL,
   ue_ambr_dl VARCHAR(32) NOT NULL,
   ue_ambr_ul VARCHAR(32) NOT NULL,
   submission_date DATE,
   PRIMARY KEY ( id )
);
insert into subscribers values( 1, '001010000013348', '00F0A5098A6C889FCD266882E404FE9F', 'FB2039670126856EB4EFD4DA916E8329', '8000', '2980', '1024000', '1024000', '2021-04-30');
DROP TABLE IF EXISTS `subscriber_apns`;
create table subscriber_apns(
   id INT NOT NULL AUTO_INCREMENT,
   imsi VARCHAR(15) NOT NULL,
   apn_id VARCHAR(32) NOT NULL,
   PRIMARY KEY ( id )
);
insert into subscriber_apns values('1', '001010000013348', '1');
create table apns(
   apn_id INT NOT NULL AUTO_INCREMENT,
   apn VARCHAR(32) NOT NULL,
   qci VARCHAR(32) NOT NULL,
   arp VARCHAR(32) NOT NULL,
   preemption_capability VARCHAR(32) NOT NULL,
   preemption_vunerability VARCHAR(32) NOT NULL,
   apn_ambr_dl VARCHAR(32) NOT NULL,
   apn_ambr_ul VARCHAR(32) NOT NULL,
   PRIMARY KEY ( apn_id )
);
insert into apns values ('1', 'default', '9', '8', 'Disabled', 'Disabled', '1024000', '1024000');
# DB access rights
CREATE user hss@localhost identified by 'hss';
grant delete,insert,select,update on hss.* to hss@localhost;
grant delete,insert,select,update on hss.* to hss@'192.168.%';
