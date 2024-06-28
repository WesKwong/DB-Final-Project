-- Active: 1714120691214@@127.0.0.1@3306@DB_Final
DROP TABLE IF EXISTS `PublishedPapers`;

DROP TABLE IF EXISTS `UndertakenProjects`;

DROP TABLE IF EXISTS `TaughtCourses`;

DROP TABLE IF EXISTS `Courses`;

DROP TABLE IF EXISTS `Teachers`;

DROP TABLE IF EXISTS `Papers`;

DROP TABLE IF EXISTS `Projects`;

CREATE TABLE IF NOT EXISTS `Teachers` (
    `TeacherID` VARCHAR(5) NOT NULL,
    `Name` VARCHAR(256) NOT NULL,
    `Gender` INTEGER NOT NULL,
    `Title` INTEGER NOT NULL,
    PRIMARY KEY (`TeacherID`)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `Courses` (
    `CourseID` VARCHAR(256) NOT NULL,
    `CourseName` VARCHAR(256) NOT NULL,
    `CreditHours` INTEGER NOT NULL,
    `CourseType` INTEGER NOT NULL,
    PRIMARY KEY (`CourseID`)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `Papers` (
    `PaperID` INTEGER NOT NULL,
    `PaperName` VARCHAR(256) NOT NULL,
    `PublicationSource` VARCHAR(256) NOT NULL,
    `PublicationYear` INTEGER NOT NULL,
    `Type` INTEGER NOT NULL,
    `Level` INTEGER NOT NULL,
    PRIMARY KEY (`PaperID`)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci AUTO_INCREMENT = 1;

CREATE TABLE IF NOT EXISTS `Projects` (
    `ProjectID` VARCHAR(256) NOT NULL,
    `ProjectName` VARCHAR(256) NOT NULL,
    `ProjectSource` VARCHAR(256) NOT NULL,
    `ProjectType` INTEGER NOT NULL,
    `TotalFunds` FLOAT NOT NULL,
    `StartDate` INTEGER NOT NULL,
    `EndDate` INTEGER NOT NULL,
    PRIMARY KEY (`ProjectID`)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `PublishedPapers` (
    `TeacherID` VARCHAR(5) NOT NULL,
    `PaperID` INTEGER NOT NULL,
    `Rank` INTEGER NOT NULL,
    `IsCorrespondingAuthor` BOOLEAN NOT NULL,
    FOREIGN KEY (`TeacherID`) REFERENCES `Teachers` (`TeacherID`) ON DELETE CASCADE,
    FOREIGN KEY (`PaperID`) REFERENCES `Papers` (`PaperID`) ON DELETE CASCADE,
    PRIMARY KEY (`TeacherID`, `PaperID`)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `UndertakenProjects` (
    `TeacherID` VARCHAR(5) NOT NULL,
    `ProjectID` VARCHAR(256) NOT NULL,
    `Rank` INTEGER NOT NULL,
    `FundsUndertaken` FLOAT NOT NULL,
    FOREIGN KEY (`TeacherID`) REFERENCES `Teachers` (`TeacherID`) ON DELETE CASCADE,
    FOREIGN KEY (`ProjectID`) REFERENCES `Projects` (`ProjectID`) ON DELETE CASCADE,
    PRIMARY KEY (`TeacherID`, `ProjectID`)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `TaughtCourses` (
    `TeacherID` VARCHAR(5) NOT NULL,
    `CourseID` VARCHAR(256) NOT NULL,
    `Year` INTEGER NOT NULL,
    `Semester` INTEGER NOT NULL,
    `HoursTaught` INTEGER NOT NULL,
    FOREIGN KEY (`TeacherID`) REFERENCES `Teachers` (`TeacherID`) ON DELETE CASCADE,
    FOREIGN KEY (`CourseID`) REFERENCES `Courses` (`CourseID`) ON DELETE CASCADE,
    PRIMARY KEY (`TeacherID`, `CourseID`, `Year`, `Semester`)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

/*
教师（
工号: Character(5) 主键
姓名: Character(256)
性别: Integer
职称: Integer
）
- 性别为整数, 1-男, 2-女
- 教师职称为整数:  1-博士后, 2-助教, 3-讲师, 4-副教授, 5-特任教授, 6-教授,
7-助理研究员, 8-特任副研究员, 9-副研究员, 10-特任研究员, 11-研究员。
课程（
课程号: Character(256) 主键
课程名: Character(256)
学时数: Integer
课程性质: Integer
）
- 课程性质为整数:  1-本科生课程, 2-研究生课程
论文（
序号: Integer 主键
论文名称: Character(256)
发表源: Character(256)
发表年份: Date
类型: Integer
级别: Integer
）
- 论文类型为整数:  1-full paper, 2-short paper,
3-poster paper, 4-demo paper。
- 论文级别为整数:  1-CCF-A, 2-CCF-B, 3-CCF-C,
4-中文 CCF-A, 5-中文 CCFB, 6-无级别。
项目（
项目号: Character(256) 主键
项目名称: Character(256)
项目来源: Character(256)
项目类型: Integer
总经费: Float
开始年份: Integer
结束年份: Integer
）
- 项目类型为整数:  1-国家级项目, 2-省部级项目, 3-市厅级项目,
4-企业合作项目, 5-其它类型项目。
发表论文（
工号: Character(5) 外键
序号: Integer 外键
排名: Integer
是否通讯作者: Boolean
）
承担项目（
工号: Character(5) 外键
项目号: Character(256) 外键
排名: Integer
承担经费: Float
）
- 发表论文和承担项目中的排名:  1-表示排名第一, 以此类推。
论文排名第一即为第一作者, 承担项目排名第一即为项目负责人。
主讲课程（
工号: Character(5) 外键
课程号: Character(256) 外键
年份: Integer
学期: Integer
承担学时: Integer
）
- 主讲课程中的学期取值为:  1-春季学期, 2-夏季学期, 3-秋季学期。
*/