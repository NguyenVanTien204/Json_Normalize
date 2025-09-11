1. Chức năng cốt lõi (core functions)

    1. Flatten object lồng sâu

        - Biến {"a": {"b": {"c": 1}}} → {"a.b.c": 1} hoặc dạng bảng.

        - Cho phép config: phân tách bằng ".", "_" hay custom.

    2. Xử lý mảng (list/array)

        - Array primitive: {"tags": ["a", "b"]} → bảng tags (1-n).

        - Array of objects: {"orders": [{"id": 1}, {"id": 2}]} → bảng orders.

        - Nested array: {"matrix": [[1,2],[3,4]]} → cần config để flatten hay lưu raw.

    3. Sinh bảng quan hệ (relationship mapping)

        - 1–N: tách bảng con và thêm FK.

        - N–N: nếu array of objects chứa references, tạo bảng junction.

    4. Null & missing field handling

        - Chuẩn hóa null → None.

        - Bổ sung cột cho key thiếu (đặt None mặc định).

    5. Type casting

        - Ép kiểu: "123" → int(123) nếu schema yêu cầu.

        - Cho phép custom rules.

    6. Duplicate handling

        - Loại bỏ phần tử trùng trong array.

        - Loại bỏ bản ghi trùng khi map sang bảng con.

    7. Schema-driven transformation (optional)

        - Input: JSON.

        - Input thêm: schema mapping (dict) → quyết định cột nào sang bảng nào.

        - Output: dict các bảng (dạng list[dict] hoặc DataFrame).

2. Chức năng tiện ích (helper / optional)

    1. Configurable key naming

        - Chuyển key sang snake_case, camelCase, hoặc giữ nguyên.

        - Xử lý ký tự đặc biệt (-, space, unicode).

    2. Explode arrays

        - Chọn explode array thành nhiều dòng (như pandas) hoặc giữ nguyên JSON string.

    3. Validation

        - Kiểm tra kiểu dữ liệu khớp schema.

        - Báo lỗi rõ ràng khi mismatch.

    4. Deduplication with rule

        - Loại trùng theo toàn bộ record hoặc chỉ theo key nào đó (ví dụ id).

    5. Error handling & logging

        - Cảnh báo khi không thể ép kiểu, khi gặp JSON quá sâu, hoặc khi schema không khớp.

    6. Output format

        - Python dict (bảng → list record).

        - Pandas DataFrame.

        - SQLAlchemy Table/ORM model (nếu muốn load trực tiếp).

3. Các trường hợp (edge cases) cần cover

A. Object / Dict

- {} (empty object).

- {"key": "value"} (flat).

- Nested sâu: {"a": {"b": {"c": {"d": 1}}}}.

B. Array

- Empty array: [].

- Primitive array: ["a","b","c"].

- Array of objects: [{"id":1},{"id":2}].

- Nested arrays: [[1,2],[3,4]].

- Mixed types: [1,"a",null].

C. Null / Missing

- Explicit null: {"x": null}.

- Missing field: object A có key x, object B không có key x.

D. Type mismatch

- {"age": "25"} trong khi schema yêu cầu int.

- {"price": "12.3"} trong khi schema yêu cầu float.

E. Duplicate

- Duplicate object trong cùng một array.

- Duplicate key-value ở nhiều cấp (ex: {"a": {"x":1}, "a.x":2}).

F. Relationship

- 1–N: {"user": 1, "orders": [...]}.

- N–N: {"student": 1, "courses": [1,2,3]} → bảng junction student_course.

G. Special cases

- Mixed object vs primitive: [{"id":1}, 2, 3].

- Keys chứa ký tự đặc biệt: {"user-id": 1, "email@domain": "x"}.

- Very deep nesting (100+ levels).

4. Chức năng nâng cao (nếu muốn mở rộng sau)

- Schema inference: tự động đoán schema quan hệ từ nhiều JSON record.

- Incremental load: xử lý JSON stream (Kafka, log).

- Parallel processing: normalize JSON theo batch.

- Integration: output trực tiếp sang Postgres/MySQL bằng SQLAlchemy.
