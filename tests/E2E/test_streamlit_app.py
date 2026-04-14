from pathlib import Path

import pytest


@pytest.mark.e2e
@pytest.mark.slow
def test_streamlit_user_can_upload_csv_and_start_analysis(page):
    sample_file = str(Path("tests/fixtures/sample_comments.csv").resolve())

    page.goto("http://127.0.0.1:8501", wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    checkbox = page.get_by_role("checkbox", name="استخدم ملف المشروع الموجود في Drive")
    checkbox.wait_for(timeout=60000)
    checkbox.uncheck()

    page.wait_for_timeout(1500)

    file_input = page.locator('input[type="file"]')
    file_input.set_input_files(sample_file)

    page.get_by_role("spinbutton", name="الحد الأدنى لتعليقات المنشور").fill("1")
    page.get_by_role("spinbutton", name="الحد الأدنى لحجم الموضوع").fill("5")

    page.wait_for_timeout(1000)

    page.get_by_role("button", name="تشغيل التحليل").click()

    result_header = page.get_by_text("الخلاصة التنفيذية")
    result_header.wait_for(timeout=120000)

    assert result_header.is_visible()
