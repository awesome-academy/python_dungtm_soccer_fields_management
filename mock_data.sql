-- PostgreSQL script to create mock data for Soccer Field Management System (in Vietnamese)
-- Run this script in psql or using the SQL query tool connected to your database

-- Disable foreign key constraints temporarily (if needed)
-- SET CONSTRAINTS ALL DEFERRED;

-- Create users (extending Django auth_user table with Vietnamese names)
INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
('pbkdf2_sha256$390000$xyzMockPasswordHash123456789$abcMockPasswordHash123456789', CURRENT_TIMESTAMP, FALSE, 'nguyen_van_a', 'Văn A', 'Nguyễn', 'nguyen.van.a@example.com', FALSE, TRUE, CURRENT_TIMESTAMP),
('pbkdf2_sha256$390000$xyzMockPasswordHash123456789$abcMockPasswordHash123456789', CURRENT_TIMESTAMP, FALSE, 'tran_thi_b', 'Thị B', 'Trần', 'tran.thi.b@example.com', FALSE, TRUE, CURRENT_TIMESTAMP),
('pbkdf2_sha256$390000$xyzMockPasswordHash123456789$abcMockPasswordHash123456789', CURRENT_TIMESTAMP, FALSE, 'le_van_c', 'Văn C', 'Lê', 'le.van.c@example.com', FALSE, TRUE, CURRENT_TIMESTAMP),
('pbkdf2_sha256$390000$xyzMockPasswordHash123456789$abcMockPasswordHash123456789', CURRENT_TIMESTAMP, FALSE, 'pham_thi_d', 'Thị D', 'Phạm', 'pham.thi.d@example.com', FALSE, TRUE, CURRENT_TIMESTAMP),
('pbkdf2_sha256$390000$xyzMockPasswordHash123456789$abcMockPasswordHash123456789', CURRENT_TIMESTAMP, FALSE, 'hoang_van_e', 'Văn E', 'Hoàng', 'hoang.van.e@example.com', FALSE, TRUE, CURRENT_TIMESTAMP),
('pbkdf2_sha256$390000$xyzMockPasswordHash123456789$abcMockPasswordHash123456789', CURRENT_TIMESTAMP, TRUE, 'admin_user', 'Quản Trị', 'Viên', 'admin@example.com', TRUE, TRUE, CURRENT_TIMESTAMP);

-- Create soccer fields with Vietnamese names and addresses (20 fields)
INSERT INTO soccer_soccerfield (name, address, phone, email, type, image, price_per_hour, status, description, deleted_at)
VALUES
('Sân bóng đá Thống Nhất', 'Số 7 Đường Tôn Đức Thắng, Phường Bến Nghé, Quận 1, TP Hồ Chí Minh', '0901234567', 'thongnhat@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 600000, 'active', 'Sân bóng đá lớn nhất khu vực trung tâm thành phố, có khán đài và hệ thống ánh sáng hiện đại.', NULL),

('Sân Bóng Đá Mini Phú Nhuận', '123 Phan Đình Phùng, Phường 17, Quận Phú Nhuận, TP Hồ Chí Minh', '0912345678', 'phunhuan@example.com', 'indoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 300000, 'active', 'Sân bóng đá mini 5 người với mặt cỏ nhân tạo cao cấp, có mái che.', NULL),

('Sân Vận Động Mỹ Đình', 'Đường Lê Đức Thọ, Phường Mỹ Đình, Quận Nam Từ Liêm, Hà Nội', '0923456789', 'mydinh@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 900000, 'maintenance', 'Sân vận động quốc gia, đạt tiêu chuẩn thi đấu quốc tế, có sức chứa lớn.', NULL),

('Sân Bóng Đá Hòa Xuân', '15 Trường Sa, Phường Hòa Xuân, Quận Cẩm Lệ, TP Đà Nẵng', '0934567890', 'hoaxuan@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 400000, 'active', 'Sân bóng đá 7 người với mặt cỏ nhân tạo, có hệ thống đèn chiếu sáng ban đêm.', NULL),

('Sân Bóng Đá Mini Cộng Hòa', '55 Cộng Hòa, Phường 12, Quận Tân Bình, TP Hồ Chí Minh', '0945678901', 'conghoa@example.com', 'indoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 350000, 'active', 'Hệ thống 3 sân bóng đá mini liền kề, thích hợp cho giải đấu mini.', NULL),

('Sân Bóng Đá Thanh Xuân', '100 Nguyễn Tuân, Phường Thanh Xuân Trung, Quận Thanh Xuân, Hà Nội', '0956789012', 'thanhxuan@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 500000, 'inactive', 'Sân bóng đá 11 người, có khu vực khán đài và dịch vụ đồ uống.', NULL),

('Sân Bóng Đá Sao Vàng', '234 Nguyễn Văn Linh, Phường Tân Phú, Quận 7, TP Hồ Chí Minh', '0967890123', 'saovang@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 550000, 'active', 'Sân bóng đá 11 người, được xây dựng theo tiêu chuẩn FIFA, có dịch vụ cho thuê trang phục.', NULL),

('Sân Bóng Đá Mini Láng Hạ', '45 Láng Hạ, Phường Láng Hạ, Quận Đống Đa, Hà Nội', '0978901234', 'langha@example.com', 'indoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 320000, 'active', 'Sân bóng đá mini 5 người, có hệ thống làm mát và quạt công nghiệp.', NULL),

('Sân Vận Động Cần Thơ', '30 Lê Lợi, Phường Cái Khế, Quận Ninh Kiều, TP Cần Thơ', '0989012345', 'cantho@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 450000, 'active', 'Sân vận động lớn nhất khu vực Đồng bằng Sông Cửu Long, có sức chứa 25.000 người.', NULL),

('Sân Bóng Đá Phố Núi', '77 Lê Duẩn, Phường Ea Tam, TP Buôn Ma Thuột, Đắk Lắk', '0990123456', 'phonui@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 280000, 'active', 'Sân bóng đá dành cho cộng đồng vùng Tây Nguyên, có view đẹp nhìn ra đồi núi.', NULL),

('Sân Bóng Đá Mini Lạch Tray', '10 Lạch Tray, Phường Lạch Tray, Quận Ngô Quyền, TP Hải Phòng', '0801234567', 'lachtray@example.com', 'indoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 300000, 'maintenance', 'Sân bóng đá mini 7 người, có hệ thống âm thanh và quầy nước giải khát.', NULL),

('Sân Bóng Đá Thái Nguyên', '99 Hoàng Văn Thụ, Phường Trưng Vương, TP Thái Nguyên', '0812345678', 'thainguyen@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 350000, 'active', 'Sân bóng đá tiêu chuẩn, được bảo trì thường xuyên, có khu vực khán giả riêng.', NULL),

('Sân Bóng Đá Mini Huế', '25 Nguyễn Huệ, Phường Vĩnh Ninh, TP Huế', '0823456789', 'hue@example.com', 'indoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 250000, 'active', 'Sân bóng đá mini trong nhà, có hệ thống điều hòa, thích hợp cho ngày mưa.', NULL),

('Sân Bóng Đá Bãi Biển Nha Trang', '2 Trần Phú, Phường Lộc Thọ, TP Nha Trang, Khánh Hòa', '0834567890', 'nhatrang@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 400000, 'active', 'Sân bóng đá cát duy nhất tại Nha Trang, view nhìn ra biển tuyệt đẹp.', NULL),

('Sân Bóng Đá Đại học Quốc Gia', '144 Xuân Thủy, Phường Dịch Vọng, Quận Cầu Giấy, Hà Nội', '0845678901', 'dhqg@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 420000, 'active', 'Sân bóng đá trong khuôn viên trường đại học, thích hợp cho sinh viên và giải đấu học sinh.', NULL),

('Sân Bóng Đá Mini Bắc Ninh', '88 Trần Hưng Đạo, Phường Đại Phúc, TP Bắc Ninh', '0856789012', 'bacninh@example.com', 'indoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 280000, 'active', 'Sân bóng đá mini chất lượng cao, có dịch vụ ghi hình trận đấu và phân tích chiến thuật.', NULL),

('Sân Bóng Đá Thủ Đức', '55 Võ Văn Ngân, Phường Linh Chiểu, TP Thủ Đức, TP Hồ Chí Minh', '0867890123', 'thuduc@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 380000, 'active', 'Sân bóng đá 7 người, mặt cỏ nhân tạo cao cấp, có hệ thống đèn LED hiện đại.', NULL),

('Sân Bóng Đá Mini Bình Thạnh', '66 Điện Biên Phủ, Phường 22, Quận Bình Thạnh, TP Hồ Chí Minh', '0878901234', 'binhthanh@example.com', 'indoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 330000, 'active', 'Hệ thống 2 sân bóng đá mini liền kề, có phòng thay đồ riêng và dịch vụ giặt đồ.', NULL),

('Sân Bóng Đá Long Biên', '111 Nguyễn Văn Cừ, Phường Gia Thụy, Quận Long Biên, Hà Nội', '0889012345', 'longbien@example.com', 'outdoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 450000, 'maintenance', 'Sân bóng đá chuẩn FIFA, có khán đài hai bên và hệ thống đèn chiếu sáng chuyên nghiệp.', NULL),

('Sân Bóng Đá Mini Đà Lạt', '200 Phan Đình Phùng, Phường 2, TP Đà Lạt, Lâm Đồng', '0890123456', 'dalat@example.com', 'indoor', 'https://static.vecteezy.com/system/resources/previews/005/961/253/non_2x/top-view-of-green-football-pitch-or-soccer-field-vector.jpg', 300000, 'active', 'Sân bóng đá mini trong nhà, không bị ảnh hưởng bởi thời tiết mưa nhiều của Đà Lạt.', NULL);

-- Create vouchers with Vietnamese descriptions (20 vouchers)
INSERT INTO soccer_voucher (code, description, discount_percent, valid_from, valid_to, min_price, max_discount_amount, rest_quantity, deleted_at)
VALUES
('CHAOHE2025', 'Ưu đãi chào hè 2025, giảm 15% cho mọi đặt sân', 15, '2025-06-01 00:00:00', '2025-08-31 23:59:59', 200000, 300000, 100, NULL),

('CUOITUAN', 'Giảm giá 10% cho các đặt sân vào cuối tuần', 10, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 0, 200000, 200, NULL),

('SV2025', 'Ưu đãi dành cho sinh viên, giảm 20% khi đặt sân giờ thấp điểm', 20, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 150000, 250000, 50, NULL),

('THANHVIEN', 'Ưu đãi cho thành viên thân thiết, giảm 25% cho mọi đặt sân', 25, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 500000, 500000, 20, NULL),

('TET2025', 'Chúc mừng năm mới 2025, giảm 30% cho đặt sân dịp Tết', 30, '2025-01-15 00:00:00', '2025-02-15 23:59:59', 300000, 600000, 30, '2025-02-16 00:00:00'),

('GIOTRE', 'Ưu đãi giờ sáng sớm (6h-8h), giảm 25% cho mọi đặt sân', 25, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 0, 400000, 150, NULL),

('QUOCTHANH', 'Giảm 20% nhân dịp Quốc Khánh 2/9', 20, '2025-08-25 00:00:00', '2025-09-05 23:59:59', 200000, 350000, 50, NULL),

('DOIHINHKHACH', 'Giảm 15% khi mang theo đội hình đối thủ', 15, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 400000, 300000, 100, NULL),

('THANGLONG', 'Ưu đãi kỷ niệm 1015 năm Thăng Long - Hà Nội, giảm 10.15%', 10, '2025-10-01 00:00:00', '2025-10-15 23:59:59', 0, 200000, 1015, NULL),

('GIOITRE2025', 'Giảm 15% cho khách hàng dưới 25 tuổi', 15, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 200000, 250000, 200, NULL),

('THUEBA', 'Giảm 18% cho đặt sân vào thứ ba hàng tuần', 18, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 0, 300000, 100, NULL),

('COMBO4', 'Giảm 30% khi đặt 4 giờ liên tiếp', 30, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 1200000, 800000, 50, NULL),

('THANHVIEN5SAO', 'Giảm 35% cho thành viên VIP', 35, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 600000, 700000, 20, NULL),

('LANCUOI2025', 'Giảm 40% cho lần đặt sân cuối cùng trong năm 2025', 40, '2025-12-20 00:00:00', '2025-12-31 23:59:59', 400000, 600000, 30, NULL),

('GIOIHANVU', 'Giảm 20% vào mùa đông (tháng 11-1)', 20, '2025-11-01 00:00:00', '2026-01-31 23:59:59', 200000, 400000, 200, NULL),

('GIAIDAU2025', 'Giảm 25% cho đặt sân tổ chức giải đấu', 25, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 800000, 1000000, 20, NULL),

('THANG9', 'Giảm 10% mừng tựu trường, áp dụng tháng 9/2025', 10, '2025-09-01 00:00:00', '2025-09-30 23:59:59', 100000, 200000, 100, NULL),

('PHUCDOAN', 'Giảm 12% cho nhóm đặt sân từ 12 người trở lên', 12, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 300000, 250000, 120, NULL),

('SINHNHAT', 'Giảm 30% vào ngày sinh nhật của khách hàng', 30, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 200000, 500000, 365, NULL),

('30THANG4', 'Giảm 20% nhân dịp lễ 30/4 và 1/5', 20, '2025-04-25 00:00:00', '2025-05-05 23:59:59', 200000, 400000, 100, NULL);

-- Enable foreign key constraints if you disabled them
-- SET CONSTRAINTS ALL IMMEDIATE;

-- Verification queries (optional, comment these out if not needed)
-- SELECT COUNT(*) FROM auth_user;
-- SELECT COUNT(*) FROM soccer_soccerfield;
-- SELECT COUNT(*) FROM soccer_voucher;

-- Enable foreign key constraints if you disabled them
-- SET CONSTRAINTS ALL IMMEDIATE;

-- Verification queries (optional, comment these out if not needed)
-- SELECT COUNT(*) FROM auth_user;
-- SELECT COUNT(*) FROM soccer_soccerfield;
-- SELECT COUNT(*) FROM soccer_voucher;
-- SELECT COUNT(*) FROM soccer_order;
-- SELECT COUNT(*) FROM soccer_review;
-- SELECT COUNT(*) FROM soccer_fieldrequest;
