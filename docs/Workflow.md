🛠 Quy trình phát triển module normalize JSON → relational
Giai đoạn 1 – Core tối thiểu (MVP)

👉 Mục tiêu: có cái chạy được, đúng cho 70% trường hợp.

Flatten object lồng → hàm flatten_dict(obj, sep=".").

Xử lý array primitive → explode thành nhiều dòng hoặc giữ nguyên.

Xử lý null & missing → chuẩn hóa None.

Output đơn giản → list[dict] hoặc pandas.DataFrame.

✅ Kết quả: bạn có thể normalize JSON phẳng và array cơ bản sang bảng chính.

Giai đoạn 2 – Array of Objects (1–N)

👉 Mục tiêu: tách bảng con cơ bản.

Viết hàm extract_child_table(parent, field, fk_name) → bảng con + foreign key.

Hỗ trợ array of objects nhiều cấp.

Xử lý duplicate trong array.

✅ Kết quả: JSON có array object sẽ tách thành bảng con liên kết.

Giai đoạn 3 – N–N & nested arrays

👉 Mục tiêu: xử lý quan hệ phức tạp.

Hỗ trợ array chứa references (ex: student.courses).

Sinh bảng junction student_course.

Nested array (list trong list) → flatten theo config.

✅ Kết quả: bạn đã map được cả 1–N và N–N.

Giai đoạn 4 – Schema & type handling

👉 Mục tiêu: dữ liệu sạch, đúng schema.

Input schema (dict hoặc Pydantic model).

Type casting (string → int/float/datetime).

Chuẩn hóa key (snake_case, remove special chars).

✅ Kết quả: dữ liệu output đồng nhất, có schema chuẩn.

Giai đoạn 5 – Helper & tiện ích

👉 Mục tiêu: dễ debug và dễ dùng.

Error handling (log khi mismatch, deep nesting).

Dedup rules (global vs per-table).

Configurable options (sep, explode arrays, keep_raw).

Unit test cho tất cả edge case.

✅ Kết quả: module ổn định, ít bug, dễ mở rộng.

Giai đoạn 6 – Advanced (nếu cần mở rộng)

👉 Mục tiêu: biến module thành mini-framework.

Schema inference tự động từ nhiều JSON record.

Streaming mode (Kafka, log).

SQLAlchemy integration (tự sinh bảng + insert).

Parallel processing (multi-core).

✅ Kết quả: module đủ sức chạy trong production pipeline.
