-- 插入一名男性博士后教师
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0001', '张伟博', 1, 1);

-- 插入一名女性助教
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0002', '李娜', 2, 2);

-- 插入一名男性讲师
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0003', '王刚', 1, 3);

-- 插入一名女性副教授
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0004', '赵敏', 2, 4);

-- 插入一名男性特任教授
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0005', '周杰', 1, 5);

-- 插入一名女性教授
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0006', '钱丽丽', 2, 6);

-- 插入一名男性助理研究员
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0007', '孙强', 1, 7);

-- 插入一名女性特任副研究员
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0008', '吴芳', 2, 8);

-- 插入一名男性副研究员
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0009', '郑浩', 1, 9);

-- 插入一名女性特任研究员
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0010', '陈燕', 2, 10);

-- 插入一名男性研究员
INSERT INTO `Teachers`(`TeacherID`, `Name`, `Gender`, `Title`) VALUES ('T0011', '罗明', 1, 11);

-- 插入一门本科生课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('C001', '计算机科学导论', 3, 1);

-- 插入一门研究生课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('C002', '高级算法设计与分析', 4, 2);

-- 插入另一门本科生课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('C003', '数据库管理系统', 3, 1);

-- 插入一门研究生专业课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('C004', '机器学习理论', 3, 2);

-- 插入一门通识教育本科生课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('C005', '世界历史概览', 2, 1);

-- 插入一门研究生选修课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('C006', '量子计算入门', 2, 2);

-- 插入一门本科生基础科学课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('PHY101', '大学物理I', 4, 1);

-- 插入一门研究生研究方法课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('RSCH701', '学术研究与论文写作', 2, 2);

-- 插入一门本科生经济学课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('ECO202', '微观经济学原理', 3, 1);

-- 插入一门研究生工程项目管理课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('PMGT602', '高级项目管理', 3, 2);

-- 插入一门本科生艺术欣赏课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('ARTS310', '西方艺术史', 2, 1);

-- 插入一门研究生专题研讨课程
INSERT INTO `Courses`(`CourseID`, `CourseName`, `CreditHours`, `CourseType`) VALUES ('SEM899', '人工智能伦理与法律', 3, 2);