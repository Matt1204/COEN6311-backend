/*
 Navicat Premium Dump SQL

 Source Server         : localhost 3306 connection
 Source Server Type    : MySQL
 Source Server Version : 80036 (8.0.36)
 Source Host           : localhost:3306
 Source Schema         : coen6311

 Target Server Type    : MySQL
 Target Server Version : 80036 (8.0.36)
 File Encoding         : 65001

 Date: 02/12/2024 18:41:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for hospital
-- ----------------------------
DROP TABLE IF EXISTS `hospital`;
CREATE TABLE `hospital`  (
  `h_id` int NOT NULL AUTO_INCREMENT,
  `h_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `h_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `h_hotline` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`h_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hospital
-- ----------------------------
INSERT INTO `hospital` VALUES (1, 'Hospital A', '123 A Street', '111-222-3333', '2024-11-02 19:23:06', '2024-11-02 19:23:06');
INSERT INTO `hospital` VALUES (2, 'Hospital B', '456 B Avenue', '444-555-6666', '2024-11-02 19:23:06', '2024-11-02 19:23:06');
INSERT INTO `hospital` VALUES (3, 'Hospital C', '789 C Road', '777-888-9999', '2024-11-02 19:23:06', '2024-11-02 19:23:06');

-- ----------------------------
-- Table structure for master_schedule
-- ----------------------------
DROP TABLE IF EXISTS `master_schedule`;
CREATE TABLE `master_schedule`  (
  `shift_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int NOT NULL COMMENT 'foreign key to shift_request',
  `supervisor_id` int NOT NULL COMMENT 'foreign key to user (role=\"supervisor\")',
  `nurse_id` int NOT NULL COMMENT 'foreign key to user (role=\"nurse\")',
  `hospital_id` int NOT NULL COMMENT 'foreign key to hospital',
  `shift_date` date NOT NULL,
  PRIMARY KEY (`shift_id`) USING BTREE,
  INDEX `request_id`(`request_id` ASC) USING BTREE,
  INDEX `supervisor_id`(`supervisor_id` ASC) USING BTREE,
  INDEX `nurse_id`(`nurse_id` ASC) USING BTREE,
  INDEX `hospital_id`(`hospital_id` ASC) USING BTREE,
  CONSTRAINT `master_schedule_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `shift_request` (`request_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `master_schedule_ibfk_2` FOREIGN KEY (`supervisor_id`) REFERENCES `user` (`u_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `master_schedule_ibfk_3` FOREIGN KEY (`nurse_id`) REFERENCES `user` (`u_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `master_schedule_ibfk_4` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`h_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 181 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of master_schedule
-- ----------------------------
INSERT INTO `master_schedule` VALUES (1, 4, 42, 33, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (2, 4, 42, 37, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (3, 4, 42, 52, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (4, 4, 42, 31, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (5, 34, 42, 21, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (6, 34, 42, 39, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (7, 34, 42, 24, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (8, 24, 47, 15, 3, '2024-11-20');
INSERT INTO `master_schedule` VALUES (9, 24, 47, 52, 3, '2024-11-20');
INSERT INTO `master_schedule` VALUES (10, 24, 47, 28, 3, '2024-11-20');
INSERT INTO `master_schedule` VALUES (11, 24, 47, 30, 3, '2024-11-20');
INSERT INTO `master_schedule` VALUES (12, 26, 46, 54, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (13, 26, 46, 9, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (14, 23, 43, 16, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (15, 23, 43, 19, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (16, 23, 43, 22, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (17, 23, 43, 25, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (18, 23, 43, 10, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (19, 18, 47, 48, 3, '2024-11-19');
INSERT INTO `master_schedule` VALUES (20, 18, 47, 54, 3, '2024-11-19');
INSERT INTO `master_schedule` VALUES (21, 10, 42, 50, 1, '2024-11-19');
INSERT INTO `master_schedule` VALUES (22, 10, 42, 20, 1, '2024-11-19');
INSERT INTO `master_schedule` VALUES (23, 31, 53, 52, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (24, 31, 53, 37, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (25, 31, 53, 31, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (26, 16, 53, 48, 1, '2024-11-19');
INSERT INTO `master_schedule` VALUES (27, 16, 53, 9, 1, '2024-11-19');
INSERT INTO `master_schedule` VALUES (28, 60, 51, 35, 3, '2024-11-24');
INSERT INTO `master_schedule` VALUES (29, 60, 51, 36, 3, '2024-11-24');
INSERT INTO `master_schedule` VALUES (30, 50, 46, 16, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (31, 50, 46, 19, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (32, 50, 46, 25, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (33, 50, 46, 10, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (34, 45, 51, 18, 3, '2024-11-22');
INSERT INTO `master_schedule` VALUES (35, 45, 51, 23, 3, '2024-11-22');
INSERT INTO `master_schedule` VALUES (36, 45, 51, 21, 3, '2024-11-22');
INSERT INTO `master_schedule` VALUES (37, 45, 51, 39, 3, '2024-11-22');
INSERT INTO `master_schedule` VALUES (38, 11, 43, 34, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (39, 11, 43, 19, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (40, 11, 43, 22, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (41, 11, 43, 23, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (42, 30, 44, 17, 3, '2024-11-21');
INSERT INTO `master_schedule` VALUES (43, 30, 44, 38, 3, '2024-11-21');
INSERT INTO `master_schedule` VALUES (44, 38, 43, 24, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (45, 38, 43, 34, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (46, 38, 43, 11, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (47, 38, 43, 23, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (48, 51, 51, 32, 3, '2024-11-23');
INSERT INTO `master_schedule` VALUES (49, 51, 51, 35, 3, '2024-11-23');
INSERT INTO `master_schedule` VALUES (50, 51, 51, 28, 3, '2024-11-23');
INSERT INTO `master_schedule` VALUES (51, 51, 51, 30, 3, '2024-11-23');
INSERT INTO `master_schedule` VALUES (52, 33, 51, 16, 3, '2024-11-21');
INSERT INTO `master_schedule` VALUES (53, 33, 51, 19, 3, '2024-11-21');
INSERT INTO `master_schedule` VALUES (54, 33, 51, 22, 3, '2024-11-21');
INSERT INTO `master_schedule` VALUES (55, 52, 42, 18, 1, '2024-11-23');
INSERT INTO `master_schedule` VALUES (56, 52, 42, 21, 1, '2024-11-23');
INSERT INTO `master_schedule` VALUES (57, 52, 42, 27, 1, '2024-11-23');
INSERT INTO `master_schedule` VALUES (58, 14, 43, 14, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (59, 14, 43, 22, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (60, 14, 43, 28, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (61, 14, 43, 30, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (62, 14, 43, 31, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (63, 48, 47, 38, 3, '2024-11-23');
INSERT INTO `master_schedule` VALUES (64, 48, 47, 14, 3, '2024-11-23');
INSERT INTO `master_schedule` VALUES (65, 6, 44, 13, 3, '2024-11-18');
INSERT INTO `master_schedule` VALUES (66, 3, 47, 16, 3, '2024-11-18');
INSERT INTO `master_schedule` VALUES (67, 3, 47, 34, 3, '2024-11-18');
INSERT INTO `master_schedule` VALUES (68, 2, 46, 17, 2, '2024-11-18');
INSERT INTO `master_schedule` VALUES (69, 2, 46, 27, 2, '2024-11-18');
INSERT INTO `master_schedule` VALUES (70, 2, 46, 29, 2, '2024-11-18');
INSERT INTO `master_schedule` VALUES (71, 58, 45, 32, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (72, 58, 45, 35, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (73, 58, 45, 36, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (74, 58, 45, 55, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (75, 46, 53, 11, 1, '2024-11-23');
INSERT INTO `master_schedule` VALUES (76, 46, 53, 23, 1, '2024-11-23');
INSERT INTO `master_schedule` VALUES (77, 54, 44, 33, 3, '2024-11-23');
INSERT INTO `master_schedule` VALUES (78, 54, 44, 27, 3, '2024-11-23');
INSERT INTO `master_schedule` VALUES (79, 54, 44, 12, 3, '2024-11-23');
INSERT INTO `master_schedule` VALUES (80, 17, 46, 54, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (81, 17, 46, 9, 2, '2024-11-19');
INSERT INTO `master_schedule` VALUES (82, 42, 51, 13, 3, '2024-11-22');
INSERT INTO `master_schedule` VALUES (83, 42, 51, 28, 3, '2024-11-22');
INSERT INTO `master_schedule` VALUES (84, 47, 43, 2, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (85, 47, 43, 17, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (86, 47, 43, 50, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (87, 47, 43, 20, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (88, 47, 43, 29, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (89, 43, 53, 33, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (90, 43, 53, 12, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (91, 43, 53, 18, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (92, 43, 53, 27, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (93, 13, 53, 13, 1, '2024-11-19');
INSERT INTO `master_schedule` VALUES (94, 7, 42, 48, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (95, 7, 42, 12, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (96, 29, 46, 34, 2, '2024-11-21');
INSERT INTO `master_schedule` VALUES (97, 29, 46, 2, 2, '2024-11-21');
INSERT INTO `master_schedule` VALUES (98, 29, 46, 23, 2, '2024-11-21');
INSERT INTO `master_schedule` VALUES (99, 29, 46, 24, 2, '2024-11-21');
INSERT INTO `master_schedule` VALUES (100, 29, 46, 14, 2, '2024-11-21');
INSERT INTO `master_schedule` VALUES (101, 61, 42, 32, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (102, 61, 42, 35, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (103, 61, 42, 30, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (104, 40, 42, 52, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (105, 40, 42, 37, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (106, 40, 42, 25, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (107, 44, 43, 34, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (108, 44, 43, 39, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (109, 44, 43, 14, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (110, 44, 43, 24, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (111, 22, 42, 16, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (112, 22, 42, 19, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (113, 22, 42, 22, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (114, 22, 42, 25, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (115, 22, 42, 10, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (116, 36, 51, 15, 3, '2024-11-21');
INSERT INTO `master_schedule` VALUES (117, 36, 51, 48, 3, '2024-11-21');
INSERT INTO `master_schedule` VALUES (118, 36, 51, 54, 3, '2024-11-21');
INSERT INTO `master_schedule` VALUES (119, 53, 43, 33, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (120, 53, 43, 12, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (121, 53, 43, 15, 2, '2024-11-23');
INSERT INTO `master_schedule` VALUES (122, 15, 51, 52, 3, '2024-11-19');
INSERT INTO `master_schedule` VALUES (123, 15, 51, 37, 3, '2024-11-19');
INSERT INTO `master_schedule` VALUES (124, 15, 51, 28, 3, '2024-11-19');
INSERT INTO `master_schedule` VALUES (125, 32, 46, 13, 2, '2024-11-21');
INSERT INTO `master_schedule` VALUES (126, 21, 47, 20, 3, '2024-11-20');
INSERT INTO `master_schedule` VALUES (127, 9, 44, 39, 3, '2024-11-18');
INSERT INTO `master_schedule` VALUES (128, 9, 44, 15, 3, '2024-11-18');
INSERT INTO `master_schedule` VALUES (129, 9, 44, 18, 3, '2024-11-18');
INSERT INTO `master_schedule` VALUES (130, 9, 44, 21, 3, '2024-11-18');
INSERT INTO `master_schedule` VALUES (131, 9, 44, 27, 3, '2024-11-18');
INSERT INTO `master_schedule` VALUES (132, 49, 45, 37, 1, '2024-11-23');
INSERT INTO `master_schedule` VALUES (133, 49, 45, 31, 1, '2024-11-23');
INSERT INTO `master_schedule` VALUES (134, 55, 45, 32, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (135, 55, 45, 35, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (136, 55, 45, 36, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (137, 55, 45, 55, 1, '2024-11-24');
INSERT INTO `master_schedule` VALUES (138, 35, 43, 9, 2, '2024-11-21');
INSERT INTO `master_schedule` VALUES (139, 35, 43, 15, 2, '2024-11-21');
INSERT INTO `master_schedule` VALUES (140, 39, 51, 17, 3, '2024-11-22');
INSERT INTO `master_schedule` VALUES (141, 39, 51, 38, 3, '2024-11-22');
INSERT INTO `master_schedule` VALUES (142, 28, 53, 2, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (143, 28, 53, 11, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (144, 28, 53, 50, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (145, 28, 53, 26, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (146, 28, 53, 29, 1, '2024-11-21');
INSERT INTO `master_schedule` VALUES (147, 5, 43, 10, 2, '2024-11-18');
INSERT INTO `master_schedule` VALUES (148, 5, 43, 13, 2, '2024-11-18');
INSERT INTO `master_schedule` VALUES (149, 20, 43, 50, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (150, 20, 43, 2, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (151, 20, 43, 20, 2, '2024-11-20');
INSERT INTO `master_schedule` VALUES (152, 37, 53, 2, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (153, 37, 53, 26, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (154, 37, 53, 11, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (155, 37, 53, 14, 1, '2024-11-22');
INSERT INTO `master_schedule` VALUES (156, 12, 44, 17, 3, '2024-11-19');
INSERT INTO `master_schedule` VALUES (157, 12, 44, 38, 3, '2024-11-19');
INSERT INTO `master_schedule` VALUES (158, 12, 44, 26, 3, '2024-11-19');
INSERT INTO `master_schedule` VALUES (159, 27, 44, 33, 3, '2024-11-20');
INSERT INTO `master_schedule` VALUES (160, 27, 44, 12, 3, '2024-11-20');
INSERT INTO `master_schedule` VALUES (161, 25, 53, 39, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (162, 25, 53, 11, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (163, 25, 53, 18, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (164, 25, 53, 21, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (165, 25, 53, 24, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (166, 19, 53, 38, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (167, 19, 53, 26, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (168, 19, 53, 29, 1, '2024-11-20');
INSERT INTO `master_schedule` VALUES (169, 1, 42, 50, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (170, 1, 42, 20, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (171, 1, 42, 26, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (172, 1, 42, 29, 1, '2024-11-18');
INSERT INTO `master_schedule` VALUES (173, 8, 43, 48, 2, '2024-11-18');
INSERT INTO `master_schedule` VALUES (174, 8, 43, 54, 2, '2024-11-18');
INSERT INTO `master_schedule` VALUES (175, 8, 43, 9, 2, '2024-11-18');
INSERT INTO `master_schedule` VALUES (176, 41, 46, 32, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (177, 41, 46, 10, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (178, 41, 46, 25, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (179, 41, 46, 30, 2, '2024-11-22');
INSERT INTO `master_schedule` VALUES (180, 41, 46, 31, 2, '2024-11-22');

-- ----------------------------
-- Table structure for preference_template
-- ----------------------------
DROP TABLE IF EXISTS `preference_template`;
CREATE TABLE `preference_template`  (
  `template_id` int NOT NULL AUTO_INCREMENT,
  `nurse_id` int NOT NULL COMMENT 'foreign key to user',
  `time_of_day` enum('morning','afternoon','night') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '\'morning\',\'afternoon\',\'night\'',
  `hours_per_week` int NOT NULL DEFAULT 40 COMMENT 'default 40',
  `preferred_week_days` json NOT NULL COMMENT 'list of strings. [\"Monday\", \"Thursday\", \"Sunday\"]',
  `max_hours_per_shift` int NOT NULL DEFAULT 8 COMMENT 'default 8',
  `hospitals_ranking` json NOT NULL COMMENT 'list of integers (hospital id)',
  `template_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'name of template',
  PRIMARY KEY (`template_id`) USING BTREE,
  INDEX `nurse_id`(`nurse_id` ASC) USING BTREE,
  CONSTRAINT `preference_template_ibfk_1` FOREIGN KEY (`nurse_id`) REFERENCES `user` (`u_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of preference_template
-- ----------------------------
INSERT INTO `preference_template` VALUES (1, 13, 'morning', 24, '[\"Monday\", \"Tuesday\"]', 8, '[2, 1, 3]', '44-tempplate1');
INSERT INTO `preference_template` VALUES (2, 13, 'night', 60, '[\"Monday\"]', 8, '[1, 2, 3]', '13-tempplate-1915');
INSERT INTO `preference_template` VALUES (3, 43, 'night', 70, '[\"Friday\", \"Sunday\"]', 6, '[1, 2, 3]', '42-tempplate');
INSERT INTO `preference_template` VALUES (4, 13, 'night', 66, '[\"Sunday\"]', 8, '[1, 2, 3]', '44-tempplate-2056');
INSERT INTO `preference_template` VALUES (5, 13, 'afternoon', 33, '[\"Thursday\"]', 7, '[3, 2, 1]', '44-tempplate-2057');
INSERT INTO `preference_template` VALUES (6, 44, 'afternoon', 70, '[\"Thursday\"]', 8, '[3, 2, 1]', '44-tempplate-2003');
INSERT INTO `preference_template` VALUES (8, 44, 'night', 33, '[\"Tuesday\"]', 8, '[3, 2, 1]', '44-tempplate-2014');
INSERT INTO `preference_template` VALUES (9, 13, 'night', 8, '[\"Monday\", \"Wednesday\", \"Friday\", \"Saturday\"]', 8, '[3, 1, 2]', '13-demo-2022');
INSERT INTO `preference_template` VALUES (10, 13, 'morning', 44, '[\"Sunday\"]', 8, '[2, 3, 1]', 'demo-2046');
INSERT INTO `preference_template` VALUES (11, 13, 'afternoon', 76, '[\"Saturday\"]', 8, '[1, 2, 3]', '13demo20-51');
INSERT INTO `preference_template` VALUES (12, 13, 'night', 24, '[\"Monday\"]', 8, '[2, 1, 3]', 'demo-13-2052');
INSERT INTO `preference_template` VALUES (13, 13, 'night', 48, '[\"Wednesday\"]', 8, '[1, 2, 3]', 'demo2057');
INSERT INTO `preference_template` VALUES (14, 13, 'night', 44, '[\"Monday\", \"Sunday\", \"Saturday\"]', 8, '[2, 1, 3]', '13-2254updated');

-- ----------------------------
-- Table structure for shift_preference
-- ----------------------------
DROP TABLE IF EXISTS `shift_preference`;
CREATE TABLE `shift_preference`  (
  `preference_id` int NOT NULL AUTO_INCREMENT,
  `nurse_id` int NOT NULL,
  `time_of_day` enum('morning','afternoon','night') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '\'morning\',\'afternoon\',\'night\'',
  `start_date` date NOT NULL COMMENT 'starting date of the week',
  `end_date` date NOT NULL COMMENT 'ending date of the week',
  `hours_per_week` int NOT NULL DEFAULT 40 COMMENT 'default 40',
  `preferred_week_days` json NOT NULL COMMENT 'list of strings. [\"Monday\", \"Thursday\", \"Sunday\"]',
  `max_hours_per_shift` int NOT NULL DEFAULT 8 COMMENT 'default 8',
  `hospitals_ranking` json NOT NULL COMMENT 'list of integers (hospital id)',
  PRIMARY KEY (`preference_id`) USING BTREE,
  INDEX `nurse_id`(`nurse_id` ASC) USING BTREE,
  CONSTRAINT `shift_preference_ibfk_1` FOREIGN KEY (`nurse_id`) REFERENCES `user` (`u_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 66 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of shift_preference
-- ----------------------------
INSERT INTO `shift_preference` VALUES (1, 2, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 2, 3]');
INSERT INTO `shift_preference` VALUES (2, 9, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 2, 3]');
INSERT INTO `shift_preference` VALUES (3, 10, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 2, 1]');
INSERT INTO `shift_preference` VALUES (4, 11, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 3, 2]');
INSERT INTO `shift_preference` VALUES (5, 12, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 2, 3]');
INSERT INTO `shift_preference` VALUES (6, 13, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 1, 3]');
INSERT INTO `shift_preference` VALUES (7, 14, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 1, 3]');
INSERT INTO `shift_preference` VALUES (8, 15, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 2, 1]');
INSERT INTO `shift_preference` VALUES (9, 16, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 1, 2]');
INSERT INTO `shift_preference` VALUES (10, 17, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 3, 1]');
INSERT INTO `shift_preference` VALUES (11, 18, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 1, 2]');
INSERT INTO `shift_preference` VALUES (12, 19, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 3, 1]');
INSERT INTO `shift_preference` VALUES (13, 20, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 2, 3]');
INSERT INTO `shift_preference` VALUES (14, 21, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 3, 2]');
INSERT INTO `shift_preference` VALUES (15, 22, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 1, 3]');
INSERT INTO `shift_preference` VALUES (16, 23, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 1, 2]');
INSERT INTO `shift_preference` VALUES (17, 24, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 2, 1]');
INSERT INTO `shift_preference` VALUES (18, 25, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 3, 1]');
INSERT INTO `shift_preference` VALUES (19, 26, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 3, 2]');
INSERT INTO `shift_preference` VALUES (20, 27, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 3, 1]');
INSERT INTO `shift_preference` VALUES (21, 28, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 2, 1]');
INSERT INTO `shift_preference` VALUES (22, 29, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 1, 3]');
INSERT INTO `shift_preference` VALUES (23, 30, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 2, 3]');
INSERT INTO `shift_preference` VALUES (24, 31, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 1, 3]');
INSERT INTO `shift_preference` VALUES (25, 32, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 2, 3]');
INSERT INTO `shift_preference` VALUES (26, 33, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 2, 3]');
INSERT INTO `shift_preference` VALUES (27, 34, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 3, 1]');
INSERT INTO `shift_preference` VALUES (28, 35, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 1, 2]');
INSERT INTO `shift_preference` VALUES (29, 36, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 2, 1]');
INSERT INTO `shift_preference` VALUES (30, 37, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 3, 2]');
INSERT INTO `shift_preference` VALUES (31, 38, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 1, 2]');
INSERT INTO `shift_preference` VALUES (32, 39, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 3, 1]');
INSERT INTO `shift_preference` VALUES (33, 48, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 1, 2]');
INSERT INTO `shift_preference` VALUES (34, 50, 'night', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 1, 3]');
INSERT INTO `shift_preference` VALUES (35, 52, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[1, 3, 2]');
INSERT INTO `shift_preference` VALUES (36, 54, 'morning', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[3, 2, 1]');
INSERT INTO `shift_preference` VALUES (37, 55, 'afternoon', '2024-11-18', '2024-11-24', 40, '[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Friday\"]', 8, '[2, 3, 1]');
INSERT INTO `shift_preference` VALUES (64, 13, 'night', '2024-12-09', '2024-12-15', 44, '[\"Monday\", \"Sunday\", \"Saturday\"]', 8, '[2, 1, 3]');
INSERT INTO `shift_preference` VALUES (65, 13, 'night', '2024-12-16', '2024-12-22', 66, '[\"Sunday\"]', 8, '[1, 2, 3]');

-- ----------------------------
-- Table structure for shift_request
-- ----------------------------
DROP TABLE IF EXISTS `shift_request`;
CREATE TABLE `shift_request`  (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `hospital_id` int NOT NULL,
  `supervisor_id` int NOT NULL,
  `shift_type` enum('morning','afternoon','night') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '\'morning\',\'afternoon\',\'night\'',
  `hours_per_shift` int NOT NULL DEFAULT 8 COMMENT 'default 8',
  `nurse_number` int NOT NULL DEFAULT 6 COMMENT 'default 6',
  `min_seniority` int NOT NULL COMMENT 'min_seniority from 1to 10',
  `shift_date` date NOT NULL,
  `day_of_week` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`request_id`) USING BTREE,
  INDEX `hospital_id`(`hospital_id` ASC) USING BTREE,
  INDEX `supervisor_id`(`supervisor_id` ASC) USING BTREE,
  CONSTRAINT `shift_request_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`h_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `shift_request_ibfk_2` FOREIGN KEY (`supervisor_id`) REFERENCES `user` (`u_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `min_seniority_check` CHECK (`min_seniority` between 1 and 10)
) ENGINE = InnoDB AUTO_INCREMENT = 69 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of shift_request
-- ----------------------------
INSERT INTO `shift_request` VALUES (1, 1, 42, 'night', 8, 4, 7, '2024-11-18', 'Monday');
INSERT INTO `shift_request` VALUES (2, 2, 46, 'night', 8, 3, 5, '2024-11-18', 'Monday');
INSERT INTO `shift_request` VALUES (3, 3, 47, 'night', 8, 2, 3, '2024-11-18', 'Monday');
INSERT INTO `shift_request` VALUES (4, 1, 42, 'afternoon', 8, 4, 5, '2024-11-18', 'Monday');
INSERT INTO `shift_request` VALUES (5, 2, 43, 'afternoon', 8, 2, 2, '2024-11-18', 'Monday');
INSERT INTO `shift_request` VALUES (6, 3, 44, 'afternoon', 8, 4, 10, '2024-11-18', 'Monday');
INSERT INTO `shift_request` VALUES (7, 1, 42, 'morning', 8, 2, 7, '2024-11-18', 'Monday');
INSERT INTO `shift_request` VALUES (8, 2, 43, 'morning', 8, 5, 10, '2024-11-18', 'Monday');
INSERT INTO `shift_request` VALUES (9, 3, 44, 'morning', 8, 5, 4, '2024-11-18', 'Monday');
INSERT INTO `shift_request` VALUES (10, 1, 42, 'night', 8, 2, 8, '2024-11-19', 'Tuesday');
INSERT INTO `shift_request` VALUES (11, 2, 43, 'night', 8, 4, 3, '2024-11-19', 'Tuesday');
INSERT INTO `shift_request` VALUES (12, 3, 44, 'night', 8, 4, 6, '2024-11-19', 'Tuesday');
INSERT INTO `shift_request` VALUES (13, 1, 53, 'afternoon', 8, 4, 10, '2024-11-19', 'Tuesday');
INSERT INTO `shift_request` VALUES (14, 2, 43, 'afternoon', 8, 5, 6, '2024-11-19', 'Tuesday');
INSERT INTO `shift_request` VALUES (15, 3, 51, 'afternoon', 8, 3, 6, '2024-11-19', 'Tuesday');
INSERT INTO `shift_request` VALUES (16, 1, 53, 'morning', 8, 4, 9, '2024-11-19', 'Tuesday');
INSERT INTO `shift_request` VALUES (17, 2, 46, 'morning', 8, 3, 10, '2024-11-19', 'Tuesday');
INSERT INTO `shift_request` VALUES (18, 3, 47, 'morning', 8, 3, 9, '2024-11-19', 'Tuesday');
INSERT INTO `shift_request` VALUES (19, 1, 53, 'night', 8, 3, 5, '2024-11-20', 'Wednesday');
INSERT INTO `shift_request` VALUES (20, 2, 43, 'night', 8, 4, 9, '2024-11-20', 'Wednesday');
INSERT INTO `shift_request` VALUES (21, 3, 47, 'night', 8, 4, 10, '2024-11-20', 'Wednesday');
INSERT INTO `shift_request` VALUES (22, 1, 42, 'afternoon', 8, 5, 2, '2024-11-20', 'Wednesday');
INSERT INTO `shift_request` VALUES (23, 2, 43, 'afternoon', 8, 5, 2, '2024-11-20', 'Wednesday');
INSERT INTO `shift_request` VALUES (24, 3, 47, 'afternoon', 8, 4, 6, '2024-11-20', 'Wednesday');
INSERT INTO `shift_request` VALUES (25, 1, 53, 'morning', 8, 5, 2, '2024-11-20', 'Wednesday');
INSERT INTO `shift_request` VALUES (26, 2, 46, 'morning', 8, 3, 10, '2024-11-20', 'Wednesday');
INSERT INTO `shift_request` VALUES (27, 3, 44, 'morning', 8, 2, 5, '2024-11-20', 'Wednesday');
INSERT INTO `shift_request` VALUES (28, 1, 53, 'night', 8, 5, 6, '2024-11-21', 'Thursday');
INSERT INTO `shift_request` VALUES (29, 2, 46, 'night', 8, 5, 3, '2024-11-21', 'Thursday');
INSERT INTO `shift_request` VALUES (30, 3, 44, 'night', 8, 3, 6, '2024-11-21', 'Thursday');
INSERT INTO `shift_request` VALUES (31, 1, 53, 'afternoon', 8, 3, 6, '2024-11-21', 'Thursday');
INSERT INTO `shift_request` VALUES (32, 2, 46, 'afternoon', 8, 3, 9, '2024-11-21', 'Thursday');
INSERT INTO `shift_request` VALUES (33, 3, 51, 'afternoon', 8, 3, 1, '2024-11-21', 'Thursday');
INSERT INTO `shift_request` VALUES (34, 1, 42, 'morning', 8, 3, 1, '2024-11-21', 'Thursday');
INSERT INTO `shift_request` VALUES (35, 2, 43, 'morning', 8, 5, 10, '2024-11-21', 'Thursday');
INSERT INTO `shift_request` VALUES (36, 3, 51, 'morning', 8, 4, 10, '2024-11-21', 'Thursday');
INSERT INTO `shift_request` VALUES (37, 1, 53, 'night', 8, 4, 6, '2024-11-22', 'Friday');
INSERT INTO `shift_request` VALUES (38, 2, 43, 'night', 8, 4, 2, '2024-11-22', 'Friday');
INSERT INTO `shift_request` VALUES (39, 3, 51, 'night', 8, 2, 6, '2024-11-22', 'Friday');
INSERT INTO `shift_request` VALUES (40, 1, 42, 'afternoon', 8, 3, 4, '2024-11-22', 'Friday');
INSERT INTO `shift_request` VALUES (41, 2, 46, 'afternoon', 8, 5, 5, '2024-11-22', 'Friday');
INSERT INTO `shift_request` VALUES (42, 3, 51, 'afternoon', 8, 4, 8, '2024-11-22', 'Friday');
INSERT INTO `shift_request` VALUES (43, 1, 53, 'morning', 8, 4, 5, '2024-11-22', 'Friday');
INSERT INTO `shift_request` VALUES (44, 2, 43, 'morning', 8, 4, 2, '2024-11-22', 'Friday');
INSERT INTO `shift_request` VALUES (45, 3, 51, 'morning', 8, 4, 2, '2024-11-22', 'Friday');
INSERT INTO `shift_request` VALUES (46, 1, 53, 'night', 8, 2, 2, '2024-11-23', 'Saturday');
INSERT INTO `shift_request` VALUES (47, 2, 43, 'night', 8, 5, 7, '2024-11-23', 'Saturday');
INSERT INTO `shift_request` VALUES (48, 3, 47, 'night', 8, 4, 7, '2024-11-23', 'Saturday');
INSERT INTO `shift_request` VALUES (49, 1, 45, 'afternoon', 8, 2, 6, '2024-11-23', 'Saturday');
INSERT INTO `shift_request` VALUES (50, 2, 46, 'afternoon', 8, 4, 4, '2024-11-23', 'Saturday');
INSERT INTO `shift_request` VALUES (51, 3, 51, 'afternoon', 8, 4, 6, '2024-11-23', 'Saturday');
INSERT INTO `shift_request` VALUES (52, 1, 42, 'morning', 8, 3, 4, '2024-11-23', 'Saturday');
INSERT INTO `shift_request` VALUES (53, 2, 43, 'morning', 8, 5, 8, '2024-11-23', 'Saturday');
INSERT INTO `shift_request` VALUES (54, 3, 44, 'morning', 8, 3, 6, '2024-11-23', 'Saturday');
INSERT INTO `shift_request` VALUES (55, 1, 45, 'night', 8, 4, 6, '2024-11-24', 'Sunday');
INSERT INTO `shift_request` VALUES (56, 2, 46, 'night', 8, 5, 9, '2024-11-24', 'Sunday');
INSERT INTO `shift_request` VALUES (57, 3, 51, 'night', 8, 4, 9, '2024-11-24', 'Sunday');
INSERT INTO `shift_request` VALUES (58, 1, 45, 'afternoon', 8, 4, 6, '2024-11-24', 'Sunday');
INSERT INTO `shift_request` VALUES (59, 2, 43, 'afternoon', 8, 3, 10, '2024-11-24', 'Sunday');
INSERT INTO `shift_request` VALUES (60, 3, 51, 'afternoon', 8, 2, 7, '2024-11-24', 'Sunday');
INSERT INTO `shift_request` VALUES (61, 1, 42, 'morning', 8, 3, 8, '2024-11-24', 'Sunday');
INSERT INTO `shift_request` VALUES (62, 2, 46, 'morning', 8, 3, 10, '2024-11-24', 'Sunday');
INSERT INTO `shift_request` VALUES (63, 3, 47, 'morning', 8, 4, 9, '2024-11-24', 'Sunday');
INSERT INTO `shift_request` VALUES (64, 3, 44, 'night', 3, 3, 10, '2024-12-11', 'Wednesday');
INSERT INTO `shift_request` VALUES (65, 3, 44, 'morning', 6, 1, 5, '2024-12-09', 'Monday');
INSERT INTO `shift_request` VALUES (66, 3, 44, 'morning', 12, 23, 2, '2024-12-09', 'Monday');
INSERT INTO `shift_request` VALUES (67, 3, 44, 'morning', 8, 10, 5, '2024-12-17', 'Tuesday');
INSERT INTO `shift_request` VALUES (68, 3, 44, 'morning', 9, 1, 5, '2024-12-18', 'Wednesday');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `u_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone_number` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `birthday` date NULL DEFAULT NULL,
  `role` enum('nurse','supervisor','admin') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `seniority` int NULL DEFAULT NULL COMMENT 'Every nurse must have a \'seniority\' in type int, ranging from 1 to 10.\r\nOther roles must have \'seniority\' as NULL',
  `hospital_id` int NULL DEFAULT NULL COMMENT 'Every supervisor must have a \'hospitalId\' in type int, ranging from 1 to 10.\r\nOther roles must have \'hospitalId\' as NULL',
  `refresh_token` json NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`u_id`) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE,
  INDEX `hospital_id`(`hospital_id` ASC) USING BTREE,
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`h_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `hospital_check` CHECK (((`role` = _utf8mb4'supervisor') and (`hospital_id` is not null)) or ((`role` <> _utf8mb4'supervisor') and (`hospital_id` is null))),
  CONSTRAINT `seniority_check` CHECK (((`role` = _utf8mb4'nurse') and (`seniority` is not null) and (`seniority` between 1 and 10)) or ((`role` <> _utf8mb4'nurse') and (`seniority` is null)))
) ENGINE = InnoDB AUTO_INCREMENT = 56 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (2, 'nurse1nurse1', 'nurse1', 'nurse1@mail.com', '$2b$12$YS6YuOwLKpEIsI8ZRRSgGugJPAQPodE.ueCjZpJJaCg0k8iWocrtS', NULL, NULL, NULL, 'nurse', 1, NULL, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMUBtYWlsLmNvbSIsImV4cCI6MTczMDU5OTkxOH0.ket9v4Oe91L_yU4BLUZYtwBS1s7SXoSuPIHf2qEFys4\"]', '2024-11-02 19:11:53', '2024-11-02 21:35:49');
INSERT INTO `user` VALUES (9, 'nurse06_firstname_xxx', 'nurse06_lastname_x', 'nurse00@mail.com', '$2b$12$iuIhzgyUQg4qXTQGFegtQ.FTcfht3EPvKQTEYGrFrWrBwP4eTZq52', NULL, NULL, NULL, 'nurse', 1, NULL, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDBAbWFpbC5jb20iLCJleHAiOjE3MzA2MDExMTR9.LS7toe1OFOuiOsKF_3G-tdTAioGb2R7MLj1g6a1WYFI\"]', '2024-11-02 19:31:51', '2024-11-29 16:20:20');
INSERT INTO `user` VALUES (10, 'nurse01_firstname', 'nurse01_lastname', 'nurse01@mail.com', '$2b$12$qUob2AdDX5BXi3ZLf.tJC.PpiQPcORf8PwfXKMwqkDA8p/hlG0/TG', '123 Maple St', '555-0101', '1985-01-01', 'nurse', 5, NULL, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDFAbWFpbC5jb20iLCJleHAiOjE3MzA2MDIwMzF9.G3E30BROnqB_mVeJatC7__ddXm-n75u88SH3ZTB0LO8\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDFAbWFpbC5jb20iLCJleHAiOjE3MzA3Njc3Nzl9.vrJiO2gqQXMCUmu0VOjxvTUeRcjCAWP8xF8KGdFduwg\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDFAbWFpbC5jb20iLCJleHAiOjE3MzE2MjM2Mjh9.DXwvTy7S_VOZKgZI985B65TDKPQ-DtG27okongmvIMc\"]', '2024-11-02 19:46:35', '2024-11-14 14:33:48');
INSERT INTO `user` VALUES (11, 'nurse02_firstname', 'nurse02_lastname', 'nurse02@mail.com', '$2b$12$h9guUFsjHIcSTN7meCrAceact3NJCeELLI7Fax5W3jeAThfNILy/a', NULL, '555-0202', NULL, 'nurse', 2, NULL, NULL, '2024-11-02 19:49:22', '2024-11-02 21:35:51');
INSERT INTO `user` VALUES (12, 'nurse03_firstname', 'nurse03_lastname', 'nurse03@mail.com', '$2b$12$VdxfEICeZbxKBYK4i6RD4eJ7zXijbWldbUFUxmli9cNYNOU1uK.Fe', '456 Oak Ln', NULL, '1990-03-15', 'nurse', 8, NULL, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDNAbWFpbC5jb20iLCJleHAiOjE3MzA2MDIxODR9.Bltfx0yC8savjHzMlGi3ahiEoBeXVGZA86LqJxF11Bk\"]', '2024-11-02 19:49:22', '2024-11-05 13:08:00');
INSERT INTO `user` VALUES (13, 'nurse04_firstname', 'n04_lastname', 'nurse04@mail.com', '$2b$12$1nrMfifHwPIpfSsxvyozketNdyUGa5LLvLPdcrj/u2r3EqUfnNHle', 'a', '111', NULL, 'nurse', 10, NULL, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzA5NDE1MTN9.ji-Xi9eLNL7v9_RKaLMPIF0BpW4ucRK0YBdOME5gr_Q\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzA5NTE2NjB9.lNg83sRiMzgonuze-HNGNs3L2mEusaaTqLoHseR4zT4\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzA5NTc5OTF9.iqlsMxDIrt_K8HliopeTrVlro58RRqzaldHmsOAg3CI\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzEwMjYyOTJ9.h-3kvc5mCkFVnRvn-3Ck-jtszYNVkekngXtPYcXzLY8\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzEwNDI2ODZ9.SXuMCiYtEtwLVP7ryhel3BnlHoDkHFfL6lShn3c4doA\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzEwNTEwMjl9.rb8Vbd87G2AAwBzJbooG6J-sXpsTkkHcxtdSP4TO8ik\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzIwODE3NTV9.1X9B-Bc5Dp4uCew8_XCItOX082pRtbT3LWErhz85OGA\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzIwODIxNDd9.B5AeTpbKemY7PztBt7etiKmcqXbJg61QcM8KDsf-ypk\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzI2NDYzNDR9.nx6hK4MEwdWp3FiEbP0LfiAIuaDtjofR26xDku5dIbE\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzI2NTAwNTV9.rvBs2lB58NpOXLDS9zAI6KqkwEf4srQCl7aN1uOkBX4\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzMwMjc4MTJ9.mRZrDobtsUiAS2dl0vZQ16E9B4bmqFNkC0VUjh915gE\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzMwMzE0MzZ9.T6t1PBlG1LGGo8O3JEk5acsR79eZ90oKRN98m0VZB6A\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzMwMzYwNzN9.Y8FozTlhIaWsVwS_7FM74SsUTvEQNkSHQto6mF2eMTA\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzMxMDU1ODB9.ffsG-YnLdWBVsxcAYQNmXJGfy97MDrs595l2aCNIPjk\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzMxMTAyNzd9.wGrOab5SbRI8XMOjQjDJi4tNzI0NwDC3BhVlbEiovkc\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzMxMTczNDB9.TutWfVhpsLM1kWfctW6sVfQgL8BZg9zwxzr7Btr9G2c\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im51cnNlMDRAbWFpbC5jb20iLCJleHAiOjE3MzMxMjE4Mzh9.VhVjzdtGKLfpc6JvKiWKB7UC-YcCp8alo2XGRhGF8b8\"]', '2024-11-02 19:49:22', '2024-12-02 15:47:18');
INSERT INTO `user` VALUES (14, 'nurse05_firstname', 'nurse05_lastname', 'nurse05@mail.com', '$2b$12$dnU4wDqGdTCqEoWVJUWYRuOyxVOBt0NAapL97uKBznlL79iXGnGUi', '789 Pine Rd', '555-0505', '1988-07-22', 'nurse', 2, NULL, NULL, '2024-11-02 19:49:22', '2024-11-02 21:35:53');
INSERT INTO `user` VALUES (15, 'nurse30_firstname', 'nurse30_lastname', 'nurse30@mail.com', '$2b$12$xaNTA5f/IURNdlDC7Sd7qe3mXW5jrElGWoN/axWaPIVzVywS0RNP.', '321 Birch Blvd', '555-3030', '1992-12-31', 'nurse', 1, NULL, NULL, '2024-11-02 19:49:22', '2024-11-02 19:49:22');
INSERT INTO `user` VALUES (16, 'nurse07_firstname', 'nurse07_lastname', 'nurse07@mail.com', '$2b$12$LfHRkrCQ0WsGFRRan4rGdO.p/oqBoTKUrpxY9IGrd/EO16EvJlbte', '707 Seventh Ave', NULL, NULL, 'nurse', 4, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:35:54');
INSERT INTO `user` VALUES (17, 'nurse08_firstname', 'nurse08_lastname', 'nurse08@mail.com', '$2b$12$YBIHL4WcXGSVldtQTAio3e8qmNH1rXNz/nqRo2h15RnxjOc9c8nWq', NULL, '555-0808', '1980-08-08', 'nurse', 8, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (18, 'nurse06_firstname', 'nurse06_lastname', 'nurse06@mail.com', '$2b$12$W8vpHwGUj3IBDzU5emTM9efcIEyt37YPpIrCRA5JHvRZ/FaTN5Veq', NULL, '555-0606', '1979-06-06', 'nurse', 5, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:29:30');
INSERT INTO `user` VALUES (19, 'nurse09_firstname', 'nurse09_lastname', 'nurse09@mail.com', '$2b$12$b01GoQA4Nuz1FIdUZhcbnerHPz8IeD/JXukcwezT02zhN.1CPuISu', '909 Ninth St', NULL, NULL, 'nurse', 4, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:35:55');
INSERT INTO `user` VALUES (20, 'nurse10_firstname', 'nurse10_lastname', 'nurse10@mail.com', '$2b$12$pzitF0FeDOmO.cLB1yKIRu8l9/mowWlLPRyRz/gVgHG6qinQjdMCa', NULL, '555-1010', '1991-10-10', 'nurse', 10, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (21, 'nurse11_firstname', 'nurse11_lastname', 'nurse11@mail.com', '$2b$12$utWC3FG56inDS7kLkiPId.fRXVoMmQZ4yd2rCJGH6CfQ8GLXiRQ6e', '1111 Eleventh Ln', NULL, '1991-11-11', 'nurse', 4, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:35:57');
INSERT INTO `user` VALUES (22, 'nurse12_firstname', 'nurse12_lastname', 'nurse12@mail.com', '$2b$12$wRMh3Uq8PQqtUUtrF.dzUeT8LWoZ9/JwNFq.9APWhyhgmqVACNX4y', NULL, '555-1212', NULL, 'nurse', 4, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:35:56');
INSERT INTO `user` VALUES (23, 'nurse13_firstname', 'nurse13_lastname', 'nurse13@mail.com', '$2b$12$howWZrOZ0O6CeoyhwbIzV.VyCf1ju5AtJdYIgnX4Jx7iFVlSX/AQK', '1313 Thirteenth St', NULL, '1993-01-13', 'nurse', 3, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (24, 'nurse14_firstname', 'nurse14_lastname', 'nurse14@mail.com', '$2b$12$JXVcdM31OrZPuKjuJvwOcuylEXLC34HylPymQLAWMAoQD6.j2G8Pe', NULL, '555-1414', NULL, 'nurse', 3, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:35:58');
INSERT INTO `user` VALUES (25, 'nurse15_firstname', 'nurse15_lastname', 'nurse15@mail.com', '$2b$12$CeMRowVB.MgXHxZwTyrGeu8ywwByCeNBh.ymcB0PDm6y77Az3CX3i', '1515 Fifteenth Ave', NULL, '1995-03-15', 'nurse', 5, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:36:00');
INSERT INTO `user` VALUES (26, 'nurse16_firstname', 'nurse16_lastname', 'nurse16@mail.com', '$2b$12$l.fdU2vCcn453AkP4noxNu4eQabfzcrXgUMhx2xP8Yt7nkZiUTlLC', NULL, '555-1616', NULL, 'nurse', 8, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:36:02');
INSERT INTO `user` VALUES (27, 'nurse17_firstname', 'nurse17_lastname', 'nurse17@mail.com', '$2b$12$HjrOnpfuwknokHWnbWqcV.0.3FQ/ZXqE4H/CL7dVC1XGXPfU2xis.', '1717 Seventeenth St', NULL, '1997-04-17', 'nurse', 7, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (28, 'nurse18_firstname', 'nurse18_lastname', 'nurse18@mail.com', '$2b$12$cPBJrUg9xg2XbxixsOkYW.c6iquMFMWqtyxHOeo7uum/Lnrm1s5ia', NULL, '555-1818', NULL, 'nurse', 8, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:36:04');
INSERT INTO `user` VALUES (29, 'nurse19_firstname', 'nurse19_lastname', 'nurse19@mail.com', '$2b$12$xqp0xnbM5.8Jcglhb7aCsOBvMHAEj5L5FxerFF53lOVXcfzgs6LEK', '1919 Nineteenth Ln', NULL, '1999-05-19', 'nurse', 8, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:36:02');
INSERT INTO `user` VALUES (30, 'nurse20_firstname', 'nurse20_lastname', 'nurse20@mail.com', '$2b$12$Yd8v1OsY8aOEVyWLvracl.tS5FXplw4oWuuyeZ.e0mMggc01xSYFK', NULL, '555-2020', '2000-02-20', 'nurse', 2, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (31, 'nurse21_firstname', 'nurse21_lastname', 'nurse21@mail.com', '$2b$12$IchQngrtgCdMYBiVEDwDd.TPKsncrUXCCgeWrdrrbN3jAKsvIO5kK', '2121 Twenty-first St', NULL, NULL, 'nurse', 8, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:36:04');
INSERT INTO `user` VALUES (32, 'nurse22_firstname', 'nurse22_lastname', 'nurse22@mail.com', '$2b$12$AAKSE4KAIDNeP2rjTHHzZOkFLTcig7Pp0DXx58Ddwdg0hx3U4rcbK', NULL, '555-2222', '2002-02-22', 'nurse', 2, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (33, 'nurse23_firstname', 'nurse23_lastname', 'nurse23@mail.com', '$2b$12$p4daUxUQYqhyhzrJi1sut.l6N68mzqYilrIAJYlZ5U9s4jbd3QlAy', '2323 Twenty-third Ave', NULL, NULL, 'nurse', 8, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:36:05');
INSERT INTO `user` VALUES (34, 'nurse24_firstname', 'nurse24_lastname', 'nurse24@mail.com', '$2b$12$/Q1ed.jteUgOwkBA1Sv4MO74YRGpE2tkNSrtpJSSZ2CrbZvYkB43i', NULL, '555-2424', '2004-04-24', 'nurse', 4, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (35, 'nurse25_firstname', 'nurse25_lastname', 'nurse25@mail.com', '$2b$12$ffQvKTLHEjHYqQ4cMS6MTefHIG2q12ajgO49l3Kbi8VcJmW33a5tO', '2525 Twenty-fifth St', NULL, '2005-05-25', 'nurse', 1, NULL, '[]', '2024-11-02 19:53:30', '2024-11-25 16:48:12');
INSERT INTO `user` VALUES (36, 'nurse26_firstname', 'nurse26_lastname', 'nurse26@mail.com', '$2b$12$Q7yK0h3rz7J6gJyWzx1wq./a09e6ycbrUccUtCVaFzmkGIfX.N3um', NULL, '555-2626', NULL, 'nurse', 1, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 21:36:11');
INSERT INTO `user` VALUES (37, 'nurse27_firstname', 'nurse27_lastname', 'nurse27@mail.com', '$2b$12$qSfmjWN1GS8N/xKHCd8znetVKdd6Rss.B9eOQvo868n1Sqp3V7pdm', '2727 Twenty-seventh Ln', NULL, '2007-07-27', 'nurse', 7, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (38, 'nurse28_firstname', 'nurse28_lastname', 'nurse28@mail.com', '$2b$12$1loJfAyMbqeePRo.XhCLtuXsLoajRAlYh.XG1KluZoSWE5YxD3I6a', '2727 Twenty-seventh Ln', NULL, '2007-07-27', 'nurse', 7, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (39, 'nurse29_firstname', 'nurse29_lastname', 'nurse29@mail.com', '$2b$12$sVmxEgAss3LiZmZ6Fp43TOS7ZD7dds15OxPXxwLrR.pQ6tef78zsK', NULL, '555-2424', '2004-04-24', 'nurse', 4, NULL, NULL, '2024-11-02 19:53:30', '2024-11-02 19:53:30');
INSERT INTO `user` VALUES (40, 'admin_1', 'admin_111111111', 'admin1@mail.com', '$2b$12$PKCqR.Eu8Rk169dEMljq0.7IXzRuE8BfsDeGKDFQN9tpm/BL6XlZu', NULL, NULL, NULL, 'admin', NULL, NULL, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMDYwMjU5OX0.tkKH5KcIZkpKYdBQodyRUKpKXI2ttKCl5eVYxnYMFgE\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMDYwMzA2N30.wat_orS7x9XaR1JkMi7KNq7zotaxMsOAfCPGLXWvI5U\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMDYwNDY4N30.vDTIo_tx6vKO_LOZQBw606RX14nBPUFPIXqKqlba2FY\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMDYxMzQzNH0.-iWiKfmf5WIdTnOm191jayiJxnJAnTkZuHu8MCw7aL0\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMDYyMDU3Mn0.UGCSJCmirjuju8g-e8V1oIRHSM93TQTAyGURmfTmiRA\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMjg0NzM1MH0.hdbdStqfeYyh8Bp6s150pwvoCT1cuyuutBHi5stsD-k\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMjg1MjAwMX0._zv1LNMrkiqBQZYwS-zM9tBX63XztQJMcfB8ievXOdk\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMjg1NTk2N30.V-NP593r72-ttbnVtnYfK1CYdzmQl9ywI97DDLT2lC8\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMjg2MTI0Mn0.XlAXTA3ZItD_-UqOOL03_ltCUIYnxS_qW8jH5cdcQ0U\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMjkxOTEzNn0.l6E-4mYMH3atXJfvU6Q01lx_WAP6nWvlMdDkByclUb8\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMjkyNzA0MX0.TscD_O8PFV54PbAwIgrmlIsz-ouxa0fj4RXFpv9pa-0\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMUBtYWlsLmNvbSIsImV4cCI6MTczMjk0MjMxNn0.O-rLYkTGqQsNIyg2AvSz81G18ZZgv5v4hALV5PB0xyg\"]', '2024-11-02 19:56:38', '2024-11-29 20:51:56');
INSERT INTO `user` VALUES (41, 'zihan', 'ma', 'admin2@mail.com', '$2b$12$LOgREEDgMmmaFH9iwrfn5eRQB6OQNV0AuMxTZx4EA.MP.XUSpRcFK', NULL, NULL, NULL, 'admin', NULL, NULL, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMkBtYWlsLmNvbSIsImV4cCI6MTczMDYwMjYyMn0.uRjqBgLdtA3PjUTYW2knA4qD_GPUsWEgg5UbkE7KgLU\"]', '2024-11-02 19:57:01', '2024-11-02 19:57:33');
INSERT INTO `user` VALUES (42, 'supervisor01_firstname', 'supervisor01_lastname', 'supervisor01@mail.com', '$2b$12$9TraUSIWF0m2k3N0FnFV2e7qmPl8ry90QoWMuTPvSM0wDUGL/Esq.', NULL, NULL, NULL, 'supervisor', NULL, 1, '[]', '2024-11-02 20:01:43', '2024-11-02 20:04:03');
INSERT INTO `user` VALUES (43, 'supervisor02_firstname', 'supervisor02_lastname', 'supervisor02@mail.com', '$2b$12$HQtdexP4CvoaW2Ober/Q2uRXfNkh/JJNlSeGoqfEb.sJsQHAi4v2q', NULL, NULL, NULL, 'supervisor', NULL, 2, NULL, '2024-11-02 20:01:43', '2024-11-02 20:01:43');
INSERT INTO `user` VALUES (44, 'supervisor03_firstname', 'supervisor03_lastname', 'supervisor03@mail.com', '$2b$12$UioqLp7mgUV.jrElrbEBu.GsdHoFFKuPr/GQGuoSPOtBkWPSWQrq.', NULL, NULL, NULL, 'supervisor', NULL, 3, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN1cGVydmlzb3IwM0BtYWlsLmNvbSIsImV4cCI6MTczMjU4MjA5OX0.MpUZBMoiDfzmu6etl1AFVF9ZJWFSvt2HeGhzPL6VC-I\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN1cGVydmlzb3IwM0BtYWlsLmNvbSIsImV4cCI6MTczMjc2NTk3NX0.SoUrNzBP_UErTnG6Ka-Cs8fKeVPuUH4XNwpm0kexO_o\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN1cGVydmlzb3IwM0BtYWlsLmNvbSIsImV4cCI6MTczMjc2OTg3MX0.F1_vg0C5r7kut0pjp8kbuTI8eTssNltNNMJO_zj_DbM\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN1cGVydmlzb3IwM0BtYWlsLmNvbSIsImV4cCI6MTczMjc3NjU2Mn0.SH8wH8nxZeVuRna8-hTPtFNk_VJw6exalMqF-b3JmCo\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN1cGVydmlzb3IwM0BtYWlsLmNvbSIsImV4cCI6MTczMzE4MzI0NX0.BfSFuHbMNNkYnuWIpaByRLX2pTXFZEQIWmgZRGvt6wE\"]', '2024-11-02 20:01:43', '2024-12-02 15:47:25');
INSERT INTO `user` VALUES (45, 'sup04firstName...', 'su04_lastname', 'supervisor04@mail.com', '$2b$12$stnPu0Y52mtwdtDyxOvDWucmSqyPJ81/EvHUEFObb/wepYo7HqyEO', 'hahaha', '110', NULL, 'supervisor', NULL, 1, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN1cGVydmlzb3IwNEBtYWlsLmNvbSIsImV4cCI6MTczMDgzOTA3Nn0.17wTay5qaTcLjudn7CEp618y68gnY3KxT6lbQSwKIMw\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN1cGVydmlzb3IwNEBtYWlsLmNvbSIsImV4cCI6MTczMDkxNzkxMn0.wC_CA0wQBd0EtPxTdcLtbzsKaADkpseunh-nc9RulY4\"]', '2024-11-02 20:01:43', '2024-11-29 20:51:51');
INSERT INTO `user` VALUES (46, 'supervisor05_firstname', 'supervisor05_lastname', 'supervisor05@mail.com', '$2b$12$Hc0X5NXd1frzJaAxvwAFZ.BuywnHQ2zieANBBHa6gFzyE3Ng1S7C.', NULL, NULL, NULL, 'supervisor', NULL, 2, NULL, '2024-11-02 20:01:43', '2024-11-02 20:01:43');
INSERT INTO `user` VALUES (47, 'sup6...', 'supervisor06_lastname', 'supervisor06@mail.com', '$2b$12$226JkupTFmVgO.4goFd8w.YwG7BNymwENN8OPTrsVDjIU1n.oaVaG', 'asdgffgdsfgdfgsdfg', '12344321', NULL, 'supervisor', NULL, 3, NULL, '2024-11-02 20:01:43', '2024-11-02 21:50:50');
INSERT INTO `user` VALUES (48, 'sdaf', 'ffff', 'demo1@mail.com', '$2b$12$MbCY88q9Q/bqArbecQxKIOV3RLv9XKwna1pFIr1iGeA.En15OJj9G', NULL, NULL, NULL, 'nurse', 10, NULL, '[]', '2024-11-02 20:18:45', '2024-11-02 21:36:21');
INSERT INTO `user` VALUES (50, '11', '22', '1@mail.com', '$2b$12$5kDvfMC6pbXfiyKS5jvAkONNLuOc2W6o4AJqZC1zPj.yj7chDULRe', NULL, NULL, NULL, 'nurse', 9, NULL, NULL, '2024-11-06 15:07:30', '2024-11-06 15:07:30');
INSERT INTO `user` VALUES (51, '22', '11', '2@mail.com', '$2b$12$TcSnA/D3jovSjR7b4hxUjOiNCkvIfhy0KzDDXgZbFsKI/ZefgNa7y', NULL, NULL, NULL, 'supervisor', NULL, 3, NULL, '2024-11-06 15:07:51', '2024-11-06 15:07:51');
INSERT INTO `user` VALUES (52, '33', '44', '3@mail.com', '$2b$12$WNpuLxFRT0SpqWR/kVa.meFT1RTpa5ySjY3rgWMrgCjUKn4gE4l.K', NULL, NULL, NULL, 'nurse', 6, NULL, NULL, '2024-11-06 15:29:03', '2024-11-06 15:29:03');
INSERT INTO `user` VALUES (53, 'sbsbsbsbsbsb', 'sb last name', '4@mail.com', '$2b$12$s93pB/F9OrMXuSQahaXkfuxhD1BpJXUon52IGnXh9G2DlBHitlDxi', 'ccd', '110', NULL, 'supervisor', NULL, 1, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IjRAbWFpbC5jb20iLCJleHAiOjE3MzA5MzU3OTN9.TYk4bAlljxl9TgXUHUrC7u2-KYTmu4qR7v15d2e-abk\"]', '2024-11-06 15:29:30', '2024-11-06 16:14:55');
INSERT INTO `user` VALUES (54, 'zihan', 'ma', '1107@mail.com', '$2b$12$ermeJ6ccWkAzLqpiVIywreZNNnjR6lOZWvp/QYVc3iG8gMuF1J43u', NULL, NULL, NULL, 'nurse', 10, NULL, '[\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IjExMDdAbWFpbC5jb20iLCJleHAiOjE3MzEwMTYxNDN9._uXnTdrAeDNJLFFAYYpmfd2awVh9hZW8U7q_QIR58R8\"]', '2024-11-07 13:49:01', '2024-11-07 13:49:03');
INSERT INTO `user` VALUES (55, '2003', '3002', '2003@mail.com', '$2b$12$RX2RjTBV2A0dOWZVEs866ulsDGLAf/KjIj0a24dOq6J3VfWd32Qjm', NULL, NULL, NULL, 'nurse', 1, NULL, '[]', '2024-11-07 20:04:24', '2024-11-07 20:05:07');

SET FOREIGN_KEY_CHECKS = 1;
